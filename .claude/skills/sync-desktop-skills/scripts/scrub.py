#!/usr/bin/env python3
"""
Deterministic PII scrubber for sync-desktop-skills.

Two modes:
  scrub:   copy SOURCE/<skill>/ -> TARGET/<skill>/, applying regex scrubs along the way.
  verify:  grep-based audit on TARGET; non-zero exit if any disallowed pattern remains.

Handles only the deterministic categories (Notion IDs, emails, phones, Calendly links).
Person/company names + judgment calls are still left to agents.

Usage:
  scrub.py scrub  --source ~/agents/skills --target <repo> --skills crm,outreach,...
  scrub.py verify --target <repo>
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

# --- Allowlists ---------------------------------------------------------------

EMAIL_ALLOWLIST = {
    "shaw@aibuilder.academy",
    "shawhintalebi@gmail.com",
    "notifications@calendly.com",
}
# Domain-level allowlist for system / no-reply senders.
EMAIL_DOMAIN_ALLOW_SUFFIXES = (
    "@anthropic.com",  # Co-Authored-By lines, etc.
)
EMAIL_LOCALPART_ALLOW = ("noreply", "no-reply", "do-not-reply")

# --- Regex patterns -----------------------------------------------------------

# 32-char hex Notion IDs (page or database, dashless form). Word boundary on both sides.
RE_NOTION_HEX = re.compile(r"(?<![a-f0-9])[a-f0-9]{32}(?![a-f0-9])")

# UUID form (with dashes) — used for both Notion IDs and other UUIDs. Treat as Notion ID.
RE_UUID = re.compile(
    r"(?<![a-f0-9])[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}(?![a-f0-9])"
)

# Email — broad. Filter via allowlist after match.
RE_EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

# Phone — North-American-leaning. Avoid matching obvious non-phone numeric runs.
RE_PHONE = re.compile(
    r"(?<!\d)(?:\+?1[\s.\-]?)?\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}(?!\d)"
)

# Calendly booking URLs (keep notifications@ email handled separately above).
RE_CALENDLY = re.compile(r"https?://(?:www\.)?calendly\.com/[^\s)>\]\"']+", re.IGNORECASE)

# --- Core scrubbing -----------------------------------------------------------


def email_is_allowed(addr: str) -> bool:
    addr_l = addr.lower()
    if addr_l in EMAIL_ALLOWLIST:
        return True
    if any(addr_l.endswith(s) for s in EMAIL_DOMAIN_ALLOW_SUFFIXES):
        return True
    local = addr_l.split("@", 1)[0]
    if any(local.startswith(p) for p in EMAIL_LOCALPART_ALLOW):
        return True
    return False


def notion_id_replacement(text: str, match: re.Match) -> str:
    """Pick [database-id] vs [page-id] based on a small left-context window."""
    start = match.start()
    window = text[max(0, start - 60) : start].lower()
    if "database" in window or "data_source" in window or "datasource" in window:
        return "[database-id]"
    return "[page-id]"


def scrub_text(text: str, rel_path: str, log: list[tuple[str, str, str, str]]) -> str:
    """Apply regex scrubs. Append (rel_path, category, original, replacement) to log."""

    def sub_notion_hex(m: re.Match) -> str:
        repl = notion_id_replacement(text, m)
        log.append((rel_path, "notion_hex_id", m.group(0), repl))
        return repl

    def sub_uuid(m: re.Match) -> str:
        repl = notion_id_replacement(text, m)
        log.append((rel_path, "uuid", m.group(0), repl))
        return repl

    def sub_email(m: re.Match) -> str:
        addr = m.group(0)
        if email_is_allowed(addr):
            return addr
        log.append((rel_path, "email", addr, "[email]"))
        return "[email]"

    def sub_phone(m: re.Match) -> str:
        log.append((rel_path, "phone", m.group(0), "[phone]"))
        return "[phone]"

    def sub_calendly(m: re.Match) -> str:
        url = m.group(0)
        # Keep the system notifications email path; only URLs are scrubbed here.
        log.append((rel_path, "calendly_link", url, "[calendar-link]"))
        return "[calendar-link]"

    out = RE_NOTION_HEX.sub(sub_notion_hex, text)
    out = RE_UUID.sub(sub_uuid, out)
    out = RE_EMAIL.sub(sub_email, out)
    out = RE_PHONE.sub(sub_phone, out)
    out = RE_CALENDLY.sub(sub_calendly, out)
    return out


# Files we apply text scrubs to. Everything else is copied byte-for-byte.
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".py",
    ".js",
    ".ts",
    ".json",
    ".yaml",
    ".yml",
    ".html",
    ".css",
    ".sh",
    ".toml",
}


def is_text_file(p: Path) -> bool:
    return p.suffix.lower() in TEXT_SUFFIXES


# --- Scrub command ------------------------------------------------------------


def cmd_scrub(args: argparse.Namespace) -> int:
    source_root = Path(args.source).expanduser().resolve()
    target_root = Path(args.target).expanduser().resolve()
    skills = [s.strip() for s in args.skills.split(",") if s.strip()]

    if not source_root.is_dir():
        print(f"source not found: {source_root}", file=sys.stderr)
        return 2
    if not target_root.is_dir():
        print(f"target not found: {target_root}", file=sys.stderr)
        return 2

    log: list[tuple[str, str, str, str]] = []
    files_written = 0
    files_skipped_binary = 0

    for skill in skills:
        src = source_root / skill
        dst = target_root / skill
        if not src.is_dir():
            print(f"[skip] source missing: {src}", file=sys.stderr)
            continue

        if dst.exists():
            if args.overwrite:
                shutil.rmtree(dst)
            else:
                print(f"[skip] target exists (pass --overwrite): {dst}", file=sys.stderr)
                continue

        for sp in src.rglob("*"):
            if sp.is_dir():
                continue
            rel = sp.relative_to(src)
            tp = dst / rel
            tp.parent.mkdir(parents=True, exist_ok=True)
            rel_path_str = f"{skill}/{rel}"

            if is_text_file(sp):
                try:
                    content = sp.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    shutil.copy2(sp, tp)
                    files_skipped_binary += 1
                    continue
                scrubbed = scrub_text(content, rel_path_str, log)
                tp.write_text(scrubbed, encoding="utf-8")
                files_written += 1
            else:
                shutil.copy2(sp, tp)
                files_skipped_binary += 1

    # --- Report --------------------------------------------------------------
    by_cat: Counter[str] = Counter()
    by_file_cat: dict[str, Counter[str]] = defaultdict(Counter)
    examples: dict[str, list[str]] = defaultdict(list)
    for rel_path, cat, orig, _ in log:
        by_cat[cat] += 1
        by_file_cat[rel_path][cat] += 1
        if len(examples[cat]) < 3:
            examples[cat].append(orig)

    print("=" * 60)
    print(f"Scrub report: {len(skills)} skills, {files_written} text files written, "
          f"{files_skipped_binary} non-text copied")
    print("=" * 60)
    print("Replacements by category:")
    for cat, n in sorted(by_cat.items(), key=lambda x: -x[1]):
        ex = ", ".join(repr(e) for e in examples[cat])
        print(f"  {cat:20s} {n:5d}   examples: {ex}")
    print()
    print("Top files by replacement count:")
    top = sorted(by_file_cat.items(), key=lambda x: -sum(x[1].values()))[:15]
    for rel_path, cats in top:
        breakdown = ", ".join(f"{c}={n}" for c, n in cats.items())
        print(f"  {sum(cats.values()):4d}  {rel_path}  ({breakdown})")

    if args.log:
        log_path = Path(args.log).expanduser().resolve()
        with log_path.open("w", encoding="utf-8") as fh:
            for rel_path, cat, orig, repl in log:
                fh.write(f"{rel_path}\t{cat}\t{orig}\t{repl}\n")
        print(f"\nFull log: {log_path}")

    return 0


# --- Verify command -----------------------------------------------------------


def cmd_verify(args: argparse.Namespace) -> int:
    target_root = Path(args.target).expanduser().resolve()
    if not target_root.is_dir():
        print(f"target not found: {target_root}", file=sys.stderr)
        return 2

    findings: list[tuple[str, str, int, str]] = []  # (category, path, lineno, line)

    for path in target_root.rglob("*"):
        if not path.is_file() or not is_text_file(path):
            continue
        # Skip the scrubber itself and the skill SKILL.md (contains rule examples).
        rel = path.relative_to(target_root).as_posix()
        if rel.startswith(".claude/skills/sync-desktop-skills/"):
            continue
        if rel.startswith(".git/"):
            continue
        try:
            for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if RE_NOTION_HEX.search(line):
                    findings.append(("notion_hex_id", rel, i, line.strip()))
                if RE_UUID.search(line):
                    findings.append(("uuid", rel, i, line.strip()))
                for m in RE_EMAIL.finditer(line):
                    if not email_is_allowed(m.group(0)):
                        findings.append(("email", rel, i, line.strip()))
                        break
                if RE_PHONE.search(line):
                    findings.append(("phone", rel, i, line.strip()))
                if RE_CALENDLY.search(line):
                    findings.append(("calendly_link", rel, i, line.strip()))
        except UnicodeDecodeError:
            continue

    if not findings:
        print("verify: clean (no deterministic-PII patterns found)")
        return 0

    by_cat: Counter[str] = Counter(f[0] for f in findings)
    print(f"verify: {len(findings)} hits across {len(by_cat)} categories")
    for cat, n in by_cat.most_common():
        print(f"  {cat}: {n}")
    print()
    for cat, rel, i, line in findings[: args.max_show]:
        snippet = line if len(line) <= 160 else line[:157] + "..."
        print(f"  [{cat}] {rel}:{i}  {snippet}")
    if len(findings) > args.max_show:
        print(f"  ... ({len(findings) - args.max_show} more)")
    return 1


# --- Entry --------------------------------------------------------------------


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("scrub", help="copy + scrub source skills into target")
    sp.add_argument("--source", required=True, help="canonical skills root (e.g. ~/agents/skills)")
    sp.add_argument("--target", required=True, help="repo root")
    sp.add_argument("--skills", required=True, help="comma-separated skill names")
    sp.add_argument("--overwrite", action="store_true", help="replace existing target dirs")
    sp.add_argument("--log", help="write full replacement log to this path (TSV)")
    sp.set_defaults(func=cmd_scrub)

    vp = sub.add_parser("verify", help="grep target tree for any remaining deterministic PII")
    vp.add_argument("--target", required=True)
    vp.add_argument("--max-show", type=int, default=40)
    vp.set_defaults(func=cmd_verify)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
