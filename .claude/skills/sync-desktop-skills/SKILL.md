---
name: sync-desktop-skills
description: Import or update skills in this public repo from Shaw's three private sources — the canonical repo at ~/agents/shaws-skills/skills (rsynced from Claude Desktop), the Code-native skills in ~/.claude/skills, and the aba-skills plugin clone — scrubbing PII on the way in. Use whenever Shaw says "sync skills", "update the non-coding skills", "pull <skill> from canonical", "add these skills to the repo", or otherwise references moving his private canonical skills into this public repo. Handles the deterministic scrub script, parallel sub-agent judgment passes, README table maintenance, and a clean commit. Do NOT use for creating skills from scratch (→ skill-creator) or one-off edits to a single already-imported skill.
---

# Sync Desktop Skills

Workflow for bringing skills from Shaw's canonical skills repo into this public GitHub repo. The hard parts are (1) scrubbing PII without over-scrubbing brand references, and (2) keeping the README table sorted and accurate.

> **Naming note:** This skill is named `sync-desktop-skills` for historical reasons — the canonical source was originally the Claude Desktop skills-plugin cache. It then moved to `~/agents/skills/`, and in Sep 2026 to the plugin-structured repo `~/agents/shaws-skills/skills/` (Claude Desktop remains the source of truth; that repo is rsynced from it hourly — see the `skill-pipeline` skill). The skill name is preserved; the workflow below reflects the current sources.

## When to use

- Shaw names specific skills to import ("add conversion-copy and sales-letter-writer from canonical")
- Shaw wants a refresh of already-imported skills after canonical-side edits
- Shaw asks for a bulk sync / comparison between canonical and repo

## When NOT to use

- Creating a skill from scratch → skill-creator
- Editing one file inside a single already-imported skill → just edit it directly

Note: a full sync draws from **three** sources (details under "Source location"): the canonical repo, the Code-native skills in `~/.claude/skills/` (animation-builder, client-docs, graphic-builder, keynote, video-editor), and the public `aba-skills` plugin (cost-optimizer, skill-helper, skill-updater) from its local `aba-plugins` clone. All are in scope for this skill. (History: July 2026 `infographic-builder` → `graphic-builder`; Oct 2026 `pre-call-research` → `meeting-prep`, `referrals` + `testimonials` → `reviews-referrals`, `training-proposal` + `proposal-deck-creator` → `client-docs`, and `skill-sync` + `night-transcript-linker` were deleted upstream.)

## Source location

The canonical skills repo lives at:

```
~/agents/shaws-skills/skills/
```

It's a plugin-structured git repo (`plugin.json` + `skills/<name>/`), rsynced from Claude Desktop hourly by `~/agents/skills-sync/sync.sh` — never edit it; it is derived state. `plugin.json` carries the last-synced version. List contents with:

```bash
ls ~/agents/shaws-skills/skills/
```

If that path is missing, do NOT guess: read `~/.claude/skills/skill-pipeline/SKILL.md` and `~/agents/skills-sync/sync.sh`, which are the authority on where the canonical copy currently lives.

Target is always this repo's root (the directory this `.claude/skills/` dir lives in).

### Second and third sources — Code-native skills and the aba-skills plugin

Shaw maintains **three** skill sources, and a full sync covers all of them:

1. `~/agents/shaws-skills/skills/` — the canonical repo above. The "portable" skills (run on any surface / Chat / Cowork). The `scrub.py` script targets this source.
2. `~/.claude/skills/` — his live Claude Code skills. This is the ONLY source for the **Code-native** skills that have no canonical copy: `animation-builder`, `client-docs`, `graphic-builder`, `keynote`, `video-editor`. (It also contains Code-only skills that are intentionally NOT published — e.g. `fasthtml`, `playwright-mcp-guidance`, `claude-trace-helper`, `generate-video-ideas`, `coding-standards`, `audit-code`, `pages`, `skill-pipeline` — and a `synced/<uuid>/` tree that is claude.ai's copy of the canonical set. Don't add the Code-only ones without Shaw's say-so; never source from `synced/`.)
3. `~/Documents/_code/_stv/_repos/aba-plugins/plugins/aba-skills/skills/` — the local clone of the public `aba-skills` plugin (`ShawhinT/aba-plugins`): `cost-optimizer`, `skill-helper`, `skill-updater`. Confirm the clone is at the same commit as `~/.claude/plugins/marketplaces/aba` before copying (`git log -1` in both). Plain `rsync -a --delete` with the junk excludes; these have historically needed zero PII edits.

For the canonical set, compare against source 1. For the Code-native and plugin skills, compare against sources 2 and 3. To tell which truly changed (vs. PII-scrub noise), scrub a temp copy of the source and diff *that* against the repo.

**iCloud conflict copies.** This repo lives under `~/Documents`, which is iCloud-synced. A bulk copy can make Finder spawn `<name> 2.md` duplicates of files being written, and `git rm` may first complain about phantom "local modifications" (a `git status` refresh clears it). Before auditing or committing: `find . -name '* 2.*' -not -path './.git/*'` and delete every hit — they exist in no source.

**Syncing Code-native and plugin skills (`scrub.py` does NOT handle these — it copies only from the canonical source):**

- Use `rsync -a --delete` per skill so upstream *deletions* propagate (e.g. video-editor dropped `analyze.py`/`propose_edits.py`). **Pass each `--exclude` as its own argument inline** — do NOT collect them in a shell variable and expand it: zsh does not word-split unquoted variables, so `$EXC` arrives as one bogus pattern and every exclude silently no-ops (this leaked full `.venv` trees and a real `.env` in one run). 
- **Exclude junk/secrets/generated:** `.DS_Store __pycache__ *.pyc .venv *.egg-info build dist wheels .env uv.lock output transcripts claude-edits .gitkeep`. (`uv.lock`/`.python-version`: don't churn them — restore whatever the repo already committed with `git checkout`; the repo's footprint is deliberate and you can't run `uv` to regen a lock.)
- **Protect repo adaptations from `--delete`** by also `--exclude`-ing them (so they're neither overwritten nor removed), then reconcile by hand:
  - `keynote/` — repo renamed `shaw-style-guide.md` → `style-guide.md` and de-personalizes the whole SKILL.md to **zero "Shaw" mentions** ("When Shaw asks" → "When asked", `"author": "Shaw Talebi"` → `"Your Name"`, "hand the step back to Shaw" → "to the user", etc.). Exclude `shaw-style-guide.md`, `style-guide.md` and `assets/logos` from the rsync (the logo PNGs are deliberately not published; `rmdir keynote/assets` afterwards), port new style-guide bullets into the renamed file, and fix the SKILL.md reference to `style-guide.md`. The upstream "verified-good logo cache" paragraphs assume the shipped `assets/logos/` folder — replace them with the committed version's "verified-good sources" wording (pull it from `git show HEAD:keynote/SKILL.md`) rather than describing a folder that isn't there. (The `shawhintalebi@gmail.com` curl-UA contact is KEEP — allowlisted + matches the committed graphic-builder precedent.)
  - `video-editor/` — keep the sanitized `.env.example`, `README.md`, `.gitignore`; never copy the real `.env`.
  - `client-docs/` (Oct 2026 successor to `training-proposal` + `proposal-deck-creator`) — keep `scripts/LOGO-README.md` (placeholder for the excluded `logo-square.png`); exclude `.venv`, `uv.lock`, `evals/` and the real logo binary. Upstream SKILL.md, `references/*-format-reference.md` and `deck/*.md` embed **real client names** (filename examples, "freshest proposal" anecdotes, even the frontmatter description) and point at Shaw's local proposals/SOW folders — scrub names to `[Company]`/fictional placeholders and genericize personal absolute paths (`/Users/shaw/...` → `~/...` or "your proposals directory"); also strip the `shawhintalebi.com` `<a>` wrappers around the header/footer logos in `scripts/md-to-pdf.py`. Grep case-insensitively: one run missed a CamelCase client name by grepping lowercase.
  - `graphic-builder/` (renamed from `infographic-builder` in July 2026) — `@shawhintalebi` footer handle, `shawhintalebi@gmail.com` curl-UA, and `aibuilder.academy` are KEEP (public). Genericize personal folder paths (`/Users/shaw/...` → `~/...`). The `billing@acme-invoices.net` in the prompt-injection example graphic is fictional payload — allowlisted in scrub.py.

**Heads-up — prior-pass misses surface here.** Earlier syncs left some PII in the *committed* repo (e.g. `crm/workflows/workflow-4-link-calls.md` and `workflow-1-sync.md` had real lead/company names; `pre-call-research/SKILL.md` (now `meeting-prep`) had a private Google Sheets ID; `crm/SKILL.md` had a bare first-name example). Re-scan the whole file even when a name appears unchanged vs HEAD, and scrub for consistency. The `report-pii` mode + the private denylist exist to catch exactly these — run it after every sync. Note: the deterministic overwrite *reintroduces* real names where the committed repo had placeholders — check each name against the committed version and restore its placeholder.

**Google Drive / Forms IDs:** `scrub.py` only catches Notion 32-hex/UUID. Google Form/Sheet/Doc IDs (43-char mixed-case with `-`/`_`) and `forms.gle` / `docs.google.com/.../d/<id>` URLs must be scrubbed by hand → `[form-id]`/`[sheet-id]`/`[page-id]`. EXCEPTION: `google-drive-helper`'s "Known Folders" table IDs are load-bearing and KEEP (committed precedent — folder IDs aren't access grants).

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
- `linkedin-voice/references/*.md` (hook-bank, hook-craft, explanation-moves) — public creators and public figures (Karpathy, Hamel Husain, Justin Welsh, etc.) and real post metrics stay; they are the point of the reference. Scrub only non-public individuals (clients, leads).
- `email-helper/references/three-way-intros.md` — the consultant roster must become a template + stubbed placeholder entries (`[Consultant 1]`, `[Consultant 2]`, …). Never commit real contact details.
- `linkedin-post-analytics/scripts/*.js` — keep scraping logic, generic selectors, and public LinkedIn URL paths intact. Scrub only Shaw-specific identifiers (his LinkedIn user ID, cookies, auth tokens, hardcoded profile URLs).
- `crm/workflows/*.md` — historically the densest source of Notion page/database IDs. Scrub aggressively.

### 3. Deterministic scrub pass (script)

Before spawning agents, run the regex scrubber at `scripts/scrub.py`. It copies source → target while replacing the deterministic categories: Notion IDs (32-char hex + UUID), emails (with allowlist for `shaw@aibuilder.academy`, `notifications@calendly.com`, placeholder/system addresses), phone numbers, Calendly + Google Doc/Sheet URLs, and `forms.gle` links. This handles the bulk of replacements (~70+ per full sync) with no agent tokens.

It also applies the **private name/company denylist** at `pii-denylist.local.json` (gitignored, never committed). Known real names/companies/IDs are auto-replaced (longest-match-first, possessive-safe); `risky: true` entries (bare first names) are report-only. An entry can carry `allow_in: ["path/prefix", ...]` — paths where that name is deliberately public and `report-pii` won't flag it (e.g. `Toyota` is allowed in the aba-brand-system "Ex-Toyota Data Scientist" bio line and proposal-deck-creator's Toyota/A3-methodology reference; `Matt` is allowed in `sfc-helper/SKILL.md` where it's public creator Matt Gray). Use `allow_in` instead of deleting an entry when a name is KEEP in some files but PII elsewhere. Keep-verbatim prefixes in `scrub.py` (`KEEP_VERBATIM_PREFIXES`) are copied without scrubbing; the list is currently empty — add a prefix only for a file that must ship byte-identical. When you scrub a NEW name by hand during a sync, **add it to the denylist** so it's caught automatically next time. Full-name entries don't catch bare-first-name uses of the same person (a `First Last` entry sailed right past a bare `First` in another file) — add distinctive bare names as separate entries. **Keep `risky` entries to distinctive names.** A risky entry for a first name that is also a common word (Mark, Will, Grace, Jane) fires on every ordinary use of the word and makes the "no leaks" gate unreachable — one run added ~20 of these and had to prune them all. For a public figure or a bio line where a name is legitimately present, use `allow_in` rather than deleting the entry.

```bash
# Copy + scrub
python3 .claude/skills/sync-desktop-skills/scripts/scrub.py scrub \
  --source ~/agents/shaws-skills/skills \
  --target . \
  --skills "$(ls ~/agents/shaws-skills/skills | paste -sd, -)" \
  --overwrite \
  --log <scratchpad>/sync-scrub.tsv

# Audit 1 — deterministic regex (should be clean except gitignored .claude/settings.local.json)
python3 .claude/skills/sync-desktop-skills/scripts/scrub.py verify --target .

# Audit 2 — judgment layer: denylist LEAKS (real names that slipped through) + proper-noun
# CANDIDATES for review. Exit non-zero if any leak. Run this after the agent pass too.
python3 .claude/skills/sync-desktop-skills/scripts/scrub.py report-pii --target .
```

Notion-ID replacement uses a small left-context heuristic: `[database-id]` if the word "database"/"data_source" appears within 60 chars to the left, else `[page-id]`. Spot-check the log; agents can fix mis-classifications during their pass. The 32-hex regex also matches public API constants embedded in scripts (e.g. LinkedIn GraphQL `queryId` hashes in `linkedin-audience` and `linkedin-post-analytics`), which breaks the script when replaced. Those live in `HEX_ALLOWLIST` in `scrub.py`; when a `[page-id]` lands inside a `.js`/`.py` file, check whether it was an API constant, restore it, and add it to the allowlist.

### 4. Parallel sub-agents (judgment-only)

After the script runs, spawn ~3 `general-purpose` sub-agents in parallel for judgment-only categories: real person names, company names, dollar amounts tied to real engagements, LinkedIn profile URLs of non-public-figures, and the carve-out files. The script has already handled deterministic patterns — agents must NOT re-do that work.

Typical batches (rough volume balance):
- **Batch A — Notion-heavy:** crm, outreach, notion-helper, executive-briefing, sop-helper, engagements, reviews-referrals, stripe-helper, calendar-helper, meeting-prep, slack-helper, convo-mining, campaign-retrospective, call-follow-up (most names live here; calendar-helper's title-composition examples and slack-helper's channel table are dense with bare first names, company slugs and Slack IDs)
- **Batch B — voice + people-heavy:** email-helper (three-way-intros template carve-out; expert-network-replies and SKILL.md "based on a real send (Name, date)" examples), client-support, sfc-helper (built from client-call research — read every line), google-drive-helper, event-finder, linkedin-audience, text-helper, social-replies, upwork, medium-helper, aba-plugin-updater, business-strategy
- **Batch C — copy-heavy + Code-native + plugin:** conversion-copy, linkedin-voice, linkedin-post-analytics, sales-letter-writer, newsletter-writer, workshop-use-case-researcher, youtube-strategy, aba-brand-system, skimmable-summary, tactical-negotiation, extract-chatgpt-transcript, plus animation-builder, graphic-builder, keynote, video-editor, client-docs, cost-optimizer, skill-helper, skill-updater (historically near-zero edits — but freshly synced upstream prose DOES reintroduce real client names in client-docs, so still read everything)

Write the shared rules (inputs, scrub/keep lists, carve-outs, boundaries, report format) to ONE brief file in the scratchpad and point all three agents at it; also drop `git show HEAD:<path>` copies of every modified file under `<scratchpad>/head/` so agents can reuse the placeholder the last public version chose. Agents must NOT edit the denylist themselves (concurrent writes) — they report new names and the orchestrator adds them.

Each sub-agent prompt must include:
1. Repo root (target only — script already did the copy)
2. Exact skill list for the batch
3. The judgment-only scrub categories + KEEP-AS-IS list
4. Per-skill carve-outs relevant to the batch (esp. linkedin-voice public-figure rule and email-helper/three-way-intros.md template-stub)
5. Report format: per-skill replacement counts by category (zero is valid), examples, judgment calls flagged
6. Hard boundary: do NOT commit, do NOT touch files outside assigned skill dirs, do NOT re-scrub deterministic patterns

### 5. Consolidation audit

After all agents return:
- Run the same PII greps across the whole repo (not just touched skills) to catch cross-skill inconsistencies
- Surface **disagreements** between agents — one agent may keep a pattern another scrubbed. If the committed public version (`git show HEAD:<path>`) already took a position on that name, follow it and apply uniformly; ask Shaw only on genuinely new items.
- Flag any stale files in target that don't exist in source (likely renamed upstream). Ask Shaw before deleting.

### 6. README maintenance

The Skills table is ordered **simplest/most portable at top, heaviest deps at bottom**. Tier order:

1. `Any` surface + `None` deps
2. `Any` + `Web search`
3. `Any` + single MCP (Notion, Gmail, Slack, …)
4. `Any` + multiple MCPs / mixed deps
5. `Claude Chat or Cowork`
6. `Claude Code or Cowork` + `Chrome tool`
7. `Claude Code or Cowork` + native/Python deps
8. `Claude Code` only — runtime-specific deps that break in Cowork (macOS-only apps like Keynote, ffmpeg-based pipelines, PDF tooling, etc.)

Alphabetize within each tier. Within tier 4, order by number of deps ascending, then alphabetical.

**Surface labels (use exactly these strings):**
- `Any`
- `Claude Chat or Cowork` — runs anywhere with the chat UI but not the CLI
- `Claude Code or Cowork` — needs CLI tooling but works in either
- `Claude Code` — CLI only; Cowork environment can't satisfy the deps

For each new skill, add a row. For deleted skills, remove the row. Update install-example URLs at the bottom if they point to a skill that no longer exists.

### 7. Pre-commit checklist

- `git diff --stat` — sanity check file counts
- No `.DS_Store`, no `.env`, no files outside intended skill dirs
- **`scrub.py report-pii --target .` → "Denylist leaks: none". This is the gate.** Eyeball the candidate list for any real name/company not yet in the denylist; scrub it and add it to the denylist.
- `scrub.py verify --target .` → clean (deterministic patterns)
- Repo-wide grep: `grep -rnE "[a-f0-9]{32}" --include="*.md"` → should be empty
- Repo-wide grep: `grep -rnE "[a-z0-9._-]+@[a-z0-9.-]+\.(com|net|org|io|ai)"` → should only show `shaw@aibuilder.academy`-adjacent hits and known system addresses
- Confirm `pii-denylist.local.json` is gitignored and NOT staged (`git check-ignore` it)
- Confirm stale files were handled (deleted or preserved per Shaw's call)

### 8. Commit + push

Commit with a summary of what changed. Example:

```
Sync canonical skills: add X, update Y, remove Z

- Added: conversion-copy, sales-letter-writer, ...
- Updated: crm, email-helper, ...
- Removed: 3-way-intro (folded into email-helper)
- README table resorted by complexity

Co-Authored-By: <the attribution line from this session's system reminder>
```

**Never push without explicit approval from Shaw.**

## Notes / precedent

- Past session established that most content-heavy skills (`conversion-copy`, `sales-letter-writer`, most single-file skills) need **zero scrubs** — the PII concentrates in Notion-integrated skills and email examples.
- `workflow-1-review.md` was an example of upstream rename (→ `workflow-1-sync.md`) that left a stale file in target. Watch for similar renames. Whole-skill renames/merges happen too (Oct 2026: 7 repo skills gone upstream, 15 new) — trace them with `git log --diff-filter=D -- skills/<name>` and `-- <name>` (pre-restructure path) in the canonical repo, then confirm the successor by reading its description, and repoint README rows and cross-references.
- Baseline volumes for a full sync (Oct 2026, 45 skills): ~330 deterministic replacements (128 denylist, 106 UUID, 68 Notion hex, 20 emails), then a 3-agent judgment pass that scrubbed ~150 person names and ~40 companies. Earlier, smaller syncs ran ~50–60 Notion IDs and ~15–20 names. A big jump beyond these numbers usually means the denylist is missing a batch of new names, not that the scrubber broke.
