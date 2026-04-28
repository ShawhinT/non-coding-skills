---
name: sync-desktop-skills
description: Import or update skills in this public repo from Shaw's canonical skills repo at ~/agents/skills. Use whenever Shaw says "sync skills", "update the non-coding skills", "pull <skill> from canonical", "add these skills to the repo", or otherwise references moving his private canonical skills into this public repo. Handles PII scrubbing via parallel sub-agents, README table maintenance, and produces a clean commit. Do NOT use for creating skills from scratch (→ skill-creator) or one-off edits to a single already-imported skill.
---

# Sync Desktop Skills

Workflow for bringing skills from Shaw's canonical skills repo into this public GitHub repo. The hard parts are (1) scrubbing PII without over-scrubbing brand references, and (2) keeping the README table sorted and accurate.

> **Naming note:** This skill is named `sync-desktop-skills` for historical reasons — the canonical source was originally the Claude Desktop skills-plugin cache. It has since moved to a dedicated git repo at `~/agents/skills/`. The skill name is preserved; the workflow below reflects the current source.

## When to use

- Shaw names specific skills to import ("add conversion-copy and sales-letter-writer from canonical")
- Shaw wants a refresh of already-imported skills after canonical-side edits
- Shaw asks for a bulk sync / comparison between canonical and repo

## When NOT to use

- Creating a skill from scratch → skill-creator
- Editing one file inside a single already-imported skill → just edit it directly
- Anything touching skills that live only in Claude Code or Cowork (those already live in this repo and aren't in the canonical source)

## Source location

The canonical skills repo lives at:

```
/Users/shaw/agents/skills/
```

It's a regular git repo — one directory per skill, no session/instance hunting needed. List contents with:

```bash
ls /Users/shaw/agents/skills/
```

Target is always this repo's root: `/Users/shaw/Documents/_code/_stv/_repos/non-coding-skills/`.

## Workflow

### 1. Intake

- List source skills: `ls <source>/skills/`
- List target repo skills: `ls <repo-root>`
- For each skill Shaw requested, classify: **NEW** (not in repo), **OVERWRITE** (exists, refresh), or **SKIP**.
- Diff overlapping skills to confirm the source is actually newer before overwriting.

Present the plan to Shaw **before** writing anything. Include:
- List of NEW vs OVERWRITE skills
- Stale files in target that don't exist in source (candidates for deletion — ask before deleting)
- Confirmation of the scrub ruleset (see below)

### 2. PII scrub ruleset

**KEEP AS-IS (public brand / load-bearing):**
- "Shaw", "Shawhin", "@ShawhinTalebi"
- "AI Builder Academy", "ABA", "ABB", "Bootcamp"
- `shaw@aibuilder.academy` (public business email — load-bearing in CRM workflow files)
- YouTube channel references, public positioning language
- Generic / illustrative dollar amounts (e.g., "$5K workshop" as example pricing)
- Generic Notion database *names* (e.g., "ABA Calls", "CRM", "Tasks", "SOPs") — useful for structure, not sensitive
- `notifications@calendly.com` and similar system addresses
- Generic LinkedIn URLs, DOM selectors, public analytics paths (in scripts)

**SCRUB → bracketed placeholder:**
- Email addresses like `name@domain.com` → `[email]`
- Real third-party person names → `[Person]` / `[Lead Name]` / `[Client Name]` / `[Consultant Name]` (pick the most fitting)
- Real third-party company names → `[Company]`
- **Notion page and database IDs (32-char hex or UUID form, anywhere they appear — URLs, `<mention-page>` tags, code blocks)** → `[page-id]` / `[database-id]`
- Phone numbers → `[phone]`
- Personal booking links with tokens → `[calendar-link]`
- URLs to private Google Docs / Notion pages → strip the identifier portion
- LinkedIn profile URLs of non-public-figure leads → `[linkedin-url]`
- Auth tokens, cookies, session IDs, hardcoded usernames in scripts → `[token]`
- Dollar figures tied to a real named engagement (e.g., "$40K deal with AcmeCo") → `$[amount]`

**Rule of thumb:** if uncertain whether something is real-person PII vs. illustrative, SCRUB. Err on the side of scrubbing.

**Per-skill carve-outs:**
- `linkedin-post-writer/references/examples-*.md` — **keep verbatim**. These are Shaw's public LinkedIn posts; public-figure names (Karpathy, Hamel Husain, etc.) and real metrics stay.
- `email-writer/references/three-way-intros.md` — the consultant roster must become a template + stubbed placeholder entries (`[Consultant 1]`, `[Consultant 2]`, …). Never commit real contact details.
- `linkedin-post-analytics/scripts/*.js` — keep scraping logic, generic selectors, and public LinkedIn URL paths intact. Scrub only Shaw-specific identifiers (his LinkedIn user ID, cookies, auth tokens, hardcoded profile URLs).
- `crm/workflows/*.md` — historically the densest source of Notion page/database IDs. Scrub aggressively.

### 3. Deterministic scrub pass (script)

Before spawning agents, run the regex scrubber at `scripts/scrub.py`. It copies source → target while replacing the deterministic categories: Notion IDs (32-char hex + UUID), emails (with allowlist for `shaw@aibuilder.academy`, `notifications@calendly.com`, system addresses), phone numbers, and Calendly URLs. This handles the bulk of replacements (~70+ per full sync) with no agent tokens.

```bash
# Copy + scrub
python3 .claude/skills/sync-desktop-skills/scripts/scrub.py scrub \
  --source ~/agents/skills \
  --target . \
  --skills crm,outreach,notion-helper,...  \
  --overwrite \
  --log /tmp/sync-scrub.tsv

# Audit (should be clean except for gitignored .claude/settings.local.json)
python3 .claude/skills/sync-desktop-skills/scripts/scrub.py verify --target .
```

Notion-ID replacement uses a small left-context heuristic: `[database-id]` if the word "database"/"data_source" appears within 60 chars to the left, else `[page-id]`. Spot-check the log; agents can fix mis-classifications during their pass.

### 4. Parallel sub-agents (judgment-only)

After the script runs, spawn ~3 `general-purpose` sub-agents in parallel for judgment-only categories: real person names, company names, dollar amounts tied to real engagements, LinkedIn profile URLs of non-public-figures, and the carve-out files. The script has already handled deterministic patterns — agents must NOT re-do that work.

Typical batches (rough volume balance):
- **Batch A — Notion-heavy:** crm, outreach, notion-helper, executive-briefing, sop-helper (most names live here)
- **Batch B — voice + people-heavy:** email-writer (three-way-intros template carve-out), calendar-helper, pre-call-research
- **Batch C — copy-heavy:** business-strategy, conversion-copy, four-rs-framework, hormozi-content-framework, linkedin-post-writer, linkedin-post-analytics, sales-letter-writer, workshop-use-case-researcher, skill-sync (historically zero edits)

Each sub-agent prompt must include:
1. Repo root (target only — script already did the copy)
2. Exact skill list for the batch
3. The judgment-only scrub categories + KEEP-AS-IS list
4. Per-skill carve-outs relevant to the batch (esp. linkedin-post-writer/examples-*.md keep-verbatim and email-writer/three-way-intros.md template-stub)
5. Report format: per-skill replacement counts by category (zero is valid), examples, judgment calls flagged
6. Hard boundary: do NOT commit, do NOT touch files outside assigned skill dirs, do NOT re-scrub deterministic patterns

### 4. Consolidation audit

After all agents return:
- Run the same PII greps across the whole repo (not just touched skills) to catch cross-skill inconsistencies
- Surface **disagreements** between agents — one agent may keep a pattern another scrubbed. Get Shaw's call on the inconsistent item and apply uniformly.
- Flag any stale files in target that don't exist in source (likely renamed upstream). Ask Shaw before deleting.

### 5. README maintenance

The Skills table is ordered **simplest/most portable at top, heaviest deps at bottom**. Tier order:

1. `Any` surface + `None` deps
2. `Any` + `Web search`
3. `Any` + single MCP (Gmail or Notion)
4. `Any` + multiple MCPs / mixed deps
5. `Claude Chat or Cowork`
6. `Claude Code or Cowork` + `Chrome tool`
7. `Claude Code or Cowork` + native/Python deps (skills-sync CLI, etc.)
8. `Claude Code` only — runtime-specific deps that break in Cowork (macOS-only apps like Keynote, ffmpeg-based pipelines, PDF tooling, etc.)

Alphabetize within each tier. Within tier 4, order by number of deps ascending, then alphabetical.

**Surface labels (use exactly these strings):**
- `Any`
- `Claude Chat or Cowork` — runs anywhere with the chat UI but not the CLI
- `Claude Code or Cowork` — needs CLI tooling but works in either
- `Claude Code` — CLI only; Cowork environment can't satisfy the deps

For each new skill, add a row. For deleted skills, remove the row. Update install-example URLs at the bottom if they point to a skill that no longer exists.

### 6. Pre-commit checklist

- `git diff --stat` — sanity check file counts
- No `.DS_Store`, no `.env`, no files outside intended skill dirs
- Repo-wide grep: `grep -rnE "[a-f0-9]{32}" --include="*.md"` → should be empty
- Repo-wide grep: `grep -rnE "[a-z0-9._-]+@[a-z0-9.-]+\.(com|net|org|io|ai)"` → should only show `shaw@aibuilder.academy`-adjacent hits and known system addresses
- Confirm stale files were handled (deleted or preserved per Shaw's call)

### 7. Commit + push

Commit with a summary of what changed. Example:

```
Sync canonical skills: add X, update Y, remove Z

- Added: conversion-copy, sales-letter-writer, ...
- Updated: crm, email-writer, ...
- Removed: 3-way-intro (folded into email-writer)
- README table resorted by complexity

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**Never push without explicit approval from Shaw.**

## Notes / precedent

- Past session established that most content-heavy skills (`conversion-copy`, `sales-letter-writer`, most single-file skills) need **zero scrubs** — the PII concentrates in Notion-integrated skills and email examples.
- Typical scrub volumes to expect per full sync: ~50–60 Notion IDs, ~15–20 person names, ~5–10 emails, ~5–10 company names.
- `workflow-1-review.md` was an example of upstream rename (→ `workflow-1-sync.md`) that left a stale file in target. Watch for similar renames.
