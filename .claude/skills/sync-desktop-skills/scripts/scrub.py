#!/usr/bin/env python3
"""
PII scrubber for sync-desktop-skills.

Modes:
  scrub:       copy SOURCE/<skill>/ -> TARGET/<skill>/, applying regex + denylist scrubs.
  verify:      grep-based audit on TARGET; non-zero exit if deterministic PII remains.
  report-pii:  judgment-layer audit on TARGET; flags denylist "leaks" (real names that
               should already be scrubbed) and unknown proper-noun candidates for review.

Deterministic categories (regex): Notion IDs, emails, phones, Calendly + Google Doc/Sheet
URLs, forms.gle links. Person/company names come from a PRIVATE denylist that is NOT
committed (see DEFAULT_DENYLIST). Genuinely-new names still need human/agent review — that's
what report-pii surfaces.

Usage:
  scrub.py scrub      --source ~/agents/skills --target <repo> --skills crm,outreach,...
  scrub.py verify     --target <repo>
  scrub.py report-pii --target <repo>
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

# --- Allowlists (PUBLIC — safe to commit) -------------------------------------

EMAIL_ALLOWLIST = {
    "shaw@aibuilder.academy",
    "shawhintalebi@gmail.com",
    "notifications@calendly.com",
    "billing@acme-invoices.net",  # fictional payload inside graphic-builder's prompt-injection example
}
# Domain-level allowlist for system / no-reply senders.
EMAIL_DOMAIN_ALLOW_SUFFIXES = (
    "@anthropic.com",  # Co-Authored-By lines, etc.
)
EMAIL_LOCALPART_ALLOW = ("noreply", "no-reply", "do-not-reply")
EMAIL_PLACEHOLDER_LOCALPART = ("you", "name", "user", "your")  # you@example.com, etc.
EMAIL_PLACEHOLDER_DOMAINS = ("example.com", "example.org", "domain.com")

# Capitalized words that are SAFE on their own. A proper-noun candidate made entirely of
# safe words (e.g. "Active Leads", "Discovery Call") is suppressed from the report.
# PUBLIC: only generic / public-figure / brand terms here — never a real client/lead name.
SAFE_WORDS = {
    # Brand / people that are public
    "Shaw", "Shawhin", "Talebi", "Hormozi", "Karpathy", "Hamel", "Husain",
    "AI", "ABA", "ABB", "Builder", "Academy", "Bootcamp", "Cowork", "Claude",
    # Tools / vendors / proper-noun product terms
    "Notion", "Google", "Gmail", "Drive", "Calendar", "Calendly", "Stripe", "Docs",
    "Sheets", "Slides", "Meet", "Microsoft", "Apple", "Keynote", "Wikimedia",
    "Heroicons", "Playwright", "Final", "Cut", "Kit", "LinkedIn", "YouTube", "Zoom",
    "Chrome", "Codex", "MCP", "Otter", "Fathom",
    # Common header / field / UI words that pair up into false positives
    "Active", "Leads", "Lead", "Clients", "Client", "Nurture", "Form", "Forms",
    "Submitted", "Discovery", "Call", "Calls", "Past", "Data", "Source", "Follow",
    "Up", "This", "Next", "Last", "Week", "For", "Example", "Entrepreneurs", "New",
    "Title", "Only", "Transcripts", "Transcript", "Known", "Folders", "Folder", "Wrap",
    "Check", "In", "Coffee", "Chat", "Skill", "Skills", "Building", "Main", "Databases",
    "Database", "Event", "Type", "Quick", "Reference", "Executive", "Briefing", "Pre",
    "Standard", "Operating", "Step", "North", "America", "Name", "First", "Notes",
    "Reserve", "Outline", "Sent", "Booked", "Pending", "Archived", "Homepage", "Contact",
    "Sales", "Pipeline", "Stage", "Stages", "Attend", "Send", "Book", "Move", "Link",
    "Onboard", "Workshop", "Workshops", "Intensive", "Session", "Sessions", "Variant",
    "Revision", "History", "Helpful", "Links", "Format", "Conventions", "Purpose",
    "Updated", "Library", "Tidy", "Walking", "Through", "Core", "Workflow", "Workflows",
    "When", "If", "Preserve", "Managing", "Director", "Hey", "Hi", "Hello", "Dear",
    "Team", "Teams", "Business", "Post", "Series", "Page", "Body", "Win", "Loss",
    "Reason", "Deal", "Size", "Close", "Date", "Rich", "Text", "Single", "Multi",
    "Select", "Field", "Fields", "Schema", "Cheat", "Sheet", "Status", "Email",
    "Subject", "Draft", "Drafts", "Approved", "Published", "Declined", "Asked",
    "Permission", "Impact", "Worth", "Before", "After", "Thinking", "Partner",
}

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

# Google Docs/Sheets/Slides/Drive URLs with a /d/<id> path — scrub the ID portion only.
RE_GOOGLE_DOC_URL = re.compile(
    r"(?P<pre>https?://(?:docs|drive|sheets)\.google\.com/[a-z]*/?d/)"
    r"(?P<id>[A-Za-z0-9_\-]{20,})"
)
# Google Forms short links.
RE_FORMS_GLE = re.compile(r"https?://forms\.gle/[A-Za-z0-9_\-]+", re.IGNORECASE)

# Candidate proper-noun shapes for the report (NOT auto-scrubbed).
RE_PROPER_PAIR = re.compile(r"\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b")
RE_GREETING_NAME = re.compile(r"\b(?:Hi|Hey|Hello|Dear)\s+([A-Z][a-z]{2,})\b")

# --- Denylist (PRIVATE — gitignored, never committed) -------------------------

# Lives in the skill folder next to this script; excluded via .gitignore.
DEFAULT_DENYLIST = Path(__file__).resolve().parent.parent / "pii-denylist.local.json"


def load_denylist(path: Path) -> list[dict]:
    """Load the private name/company denylist. Returns [] if absent (graceful)."""
    if not path.exists():
        print(
            f"[denylist] not found at {path} — skipping name scrub. "
            f"(Create it to enable auto-scrubbing of known names/companies.)",
            file=sys.stderr,
        )
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"[denylist] failed to parse {path}: {e}", file=sys.stderr)
        return []
    entries = data if isinstance(data, list) else data.get("entities", [])
    # Longest match first so "Justin Schaffer" beats bare "Justin".
    entries.sort(key=lambda e: len(e.get("match", "")), reverse=True)
    for e in entries:
        flags = re.IGNORECASE if e.get("case_insensitive") else 0
        if e.get("word_boundary", True):
            # \b...\b — leaves a trailing possessive ('s) intact: "Justin's" -> "[Name]'s".
            e["_re"] = re.compile(r"\b" + re.escape(e["match"]) + r"\b", flags)
        else:
            e["_re"] = re.compile(re.escape(e["match"]), flags)
    return entries


def email_is_allowed(addr: str) -> bool:
    addr_l = addr.lower()
    if addr_l in EMAIL_ALLOWLIST:
        return True
    if any(addr_l.endswith(s) for s in EMAIL_DOMAIN_ALLOW_SUFFIXES):
        return True
    local, _, domain = addr_l.partition("@")
    if any(local.startswith(p) for p in EMAIL_LOCALPART_ALLOW):
        return True
    if local in EMAIL_PLACEHOLDER_LOCALPART or domain in EMAIL_PLACEHOLDER_DOMAINS:
        return True
    return False


def notion_id_replacement(text: str, match: re.Match) -> str:
    """Pick [database-id] vs [page-id] based on a small left-context window."""
    start = match.start()
    window = text[max(0, start - 60) : start].lower()
    if "database" in window or "data_source" in window or "datasource" in window:
        return "[database-id]"
    return "[page-id]"


def google_doc_replacement(text: str, match: re.Match) -> str:
    """Pick [sheet-id] vs [doc-id] from the URL host/path."""
    pre = match.group("pre").lower()
    return "[sheet-id]" if "sheets" in pre or "spreadsheets" in pre else "[doc-id]"


def scrub_text(
    text: str,
    rel_path: str,
    log: list[tuple[str, str, str, str]],
    denylist: list[dict] | None = None,
) -> str:
    """Apply regex + denylist scrubs. Append (rel_path, category, original, repl) to log."""

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
        log.append((rel_path, "calendly_link", m.group(0), "[calendar-link]"))
        return "[calendar-link]"

    def sub_google_doc(m: re.Match) -> str:
        repl_id = google_doc_replacement(text, m)
        log.append((rel_path, "google_doc_id", m.group("id"), repl_id))
        return m.group("pre") + repl_id

    def sub_forms_gle(m: re.Match) -> str:
        log.append((rel_path, "forms_gle", m.group(0), "[form-url]"))
        return "[form-url]"

    out = RE_NOTION_HEX.sub(sub_notion_hex, text)
    out = RE_UUID.sub(sub_uuid, out)
    out = RE_GOOGLE_DOC_URL.sub(sub_google_doc, out)
    out = RE_FORMS_GLE.sub(sub_forms_gle, out)
    out = RE_EMAIL.sub(sub_email, out)
    out = RE_PHONE.sub(sub_phone, out)
    out = RE_CALENDLY.sub(sub_calendly, out)

    # Denylist names/companies — only non-risky entries auto-apply (longest-first).
    for entry in denylist or []:
        if entry.get("risky"):
            continue  # report-only; bare first names etc.
        # allow_in: path prefixes where this term is public/permitted (e.g. a public
        # homepage logo marquee). Skip scrubbing it there.
        if any(rel_path.startswith(pre) for pre in entry.get("allow_in", [])):
            continue
        repl = entry["replace"]

        def _sub(m: re.Match, _repl=repl, _match=entry["match"]) -> str:
            log.append((rel_path, "denylist", m.group(0), _repl))
            return _repl

        out = entry["_re"].sub(_sub, out)
    return out


# Files we apply text scrubs to. Everything else is copied byte-for-byte.
TEXT_SUFFIXES = {
    ".md", ".txt", ".py", ".js", ".ts", ".json", ".yaml", ".yml",
    ".html", ".css", ".sh", ".toml", ".applescript",
}


def is_text_file(p: Path) -> bool:
    return p.suffix.lower() in TEXT_SUFFIXES


# Carve-out files copied byte-for-byte (no scrubbing): public posts whose public-figure
# names + metrics are load-bearing. See SKILL.md "Per-skill carve-outs".
KEEP_VERBATIM_PREFIXES = (
    "linkedin-post-writer/references/examples-",
)


def is_keep_verbatim(rel_path: str) -> bool:
    return any(rel_path.startswith(pre) for pre in KEEP_VERBATIM_PREFIXES)


def iter_target_text_files(target_root: Path):
    """Yield (path, rel_posix) for scannable text files, skipping git + the sync skill."""
    for path in target_root.rglob("*"):
        if not path.is_file() or not is_text_file(path):
            continue
        rel = path.relative_to(target_root).as_posix()
        if rel.startswith(".git/") or rel.startswith(".claude/skills/sync-desktop-skills/"):
            continue
        if is_keep_verbatim(rel):
            continue
        yield path, rel


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

    denylist = load_denylist(Path(args.denylist).expanduser() if args.denylist else DEFAULT_DENYLIST)
    if denylist:
        print(f"[denylist] loaded {len(denylist)} entries "
              f"({sum(1 for e in denylist if e.get('risky'))} risky/report-only)")

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

            if is_text_file(sp) and not is_keep_verbatim(rel_path_str):
                try:
                    content = sp.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    shutil.copy2(sp, tp)
                    files_skipped_binary += 1
                    continue
                scrubbed = scrub_text(content, rel_path_str, log, denylist)
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


# --- Verify command (deterministic regex audit) -------------------------------


def cmd_verify(args: argparse.Namespace) -> int:
    target_root = Path(args.target).expanduser().resolve()
    if not target_root.is_dir():
        print(f"target not found: {target_root}", file=sys.stderr)
        return 2

    findings: list[tuple[str, str, int, str]] = []

    for path, rel in iter_target_text_files(target_root):
        try:
            for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if RE_NOTION_HEX.search(line):
                    findings.append(("notion_hex_id", rel, i, line.strip()))
                if RE_UUID.search(line):
                    findings.append(("uuid", rel, i, line.strip()))
                if RE_GOOGLE_DOC_URL.search(line):
                    findings.append(("google_doc_id", rel, i, line.strip()))
                if RE_FORMS_GLE.search(line):
                    findings.append(("forms_gle", rel, i, line.strip()))
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


# --- report-pii command (judgment-layer audit) --------------------------------


def cmd_report_pii(args: argparse.Namespace) -> int:
    target_root = Path(args.target).expanduser().resolve()
    if not target_root.is_dir():
        print(f"target not found: {target_root}", file=sys.stderr)
        return 2

    denylist = load_denylist(Path(args.denylist).expanduser() if args.denylist else DEFAULT_DENYLIST)

    leaks: list[tuple[str, str, int, str]] = []          # denylist match present = LEAK
    candidates: Counter[str] = Counter()                 # unknown proper noun -> count
    candidate_loc: dict[str, tuple[str, int]] = {}       # first location seen

    for path, rel in iter_target_text_files(target_root):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for i, line in enumerate(lines, 1):
            # 1. denylist leaks (both risky + non-risky — any real name present is a problem)
            for entry in denylist:
                if any(rel.startswith(pre) for pre in entry.get("allow_in", [])):
                    continue  # permitted in this public-surface context
                if entry["_re"].search(line):
                    leaks.append((entry["match"], rel, i, line.strip()))
            # 2. unknown proper-noun candidates
            for w1, w2 in RE_PROPER_PAIR.findall(line):
                if w1 in SAFE_WORDS and w2 in SAFE_WORDS:
                    continue
                cand = f"{w1} {w2}"
                candidates[cand] += 1
                candidate_loc.setdefault(cand, (rel, i))
            for nm in RE_GREETING_NAME.findall(line):
                if nm in SAFE_WORDS:
                    continue
                cand = f"(greeting) {nm}"
                candidates[cand] += 1
                candidate_loc.setdefault(cand, (rel, i))

    print("=" * 60)
    print("report-pii")
    print("=" * 60)

    if leaks:
        print(f"\n!!! {len(leaks)} DENYLIST LEAK(S) — real names present in target (should be scrubbed):")
        for match, rel, i, line in leaks[: args.max_show]:
            snippet = line if len(line) <= 140 else line[:137] + "..."
            print(f"  [{match}] {rel}:{i}  {snippet}")
    else:
        print("\nDenylist leaks: none ✓")

    if candidates:
        print(f"\n{len(candidates)} proper-noun CANDIDATE(S) for review "
              f"(not in denylist or SAFE_WORDS — eyeball, add real ones to the denylist):")
        for cand, n in candidates.most_common(args.max_candidates):
            rel, i = candidate_loc[cand]
            print(f"  {n:3d}x  {cand:32s}  first: {rel}:{i}")
        if len(candidates) > args.max_candidates:
            print(f"  ... ({len(candidates) - args.max_candidates} more distinct candidates)")
    else:
        print("\nProper-noun candidates: none")

    return 1 if leaks else 0


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
    sp.add_argument("--denylist", help=f"private name denylist (default: {DEFAULT_DENYLIST.name})")
    sp.set_defaults(func=cmd_scrub)

    vp = sub.add_parser("verify", help="grep target tree for any remaining deterministic PII")
    vp.add_argument("--target", required=True)
    vp.add_argument("--max-show", type=int, default=40)
    vp.set_defaults(func=cmd_verify)

    rp = sub.add_parser("report-pii", help="audit target for denylist leaks + proper-noun candidates")
    rp.add_argument("--target", required=True)
    rp.add_argument("--denylist", help=f"private name denylist (default: {DEFAULT_DENYLIST.name})")
    rp.add_argument("--max-show", type=int, default=60)
    rp.add_argument("--max-candidates", type=int, default=80)
    rp.set_defaults(func=cmd_report_pii)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
