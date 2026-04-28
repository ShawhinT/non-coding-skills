---
name: skill-sync
description: Run Shaw's skills-sync tool to publish user-created skills from Claude Desktop to the canonical git repo, Codex, and Claude Code. Use whenever Shaw asks to sync skills, run skills-sync, publish a new skill, push a skill to Codex or Claude Code, mirror skills across runtimes, check skills-sync status, see what's in the canonical repo, or remove a skill from canonical/targets. Triggers include "sync my skills", "run skills-sync", "push this skill out", "publish my new skill", "mirror skills", "skills-sync status", "what's in my canonical skills repo", "how did the last sync go", "remove X from codex", "drop X from canonical". Even casual mentions like "push that skill" or "update codex with my new skill" should trigger this skill. Do NOT use for creating or editing skills — that's skill-creator / skill-updater. This skill only runs the sync tool.
---

# skill-sync

Shaw's `skills-sync` is a Python CLI at `/Users/shaw/agents/skills-sync` that publishes user-created skills from **Claude Desktop** (source of truth) to three destinations:

- **Canonical repo:** `/Users/shaw/agents/skills` — git-tracked; successful syncs auto-commit.
- **Codex:** `/Users/shaw/.codex/skills`
- **Claude Code:** `/Users/shaw/.claude/skills`

A LaunchAgent runs the tool on a schedule, but Shaw sometimes needs to trigger it manually — right after authoring a new skill, when debugging, or when verifying what's live. This skill is the wrapper for those manual runs.

## How to invoke the tool

Every command runs from the tool directory via `uv`. Use the Bash tool:

```bash
cd /Users/shaw/agents/skills-sync && uv run main.py <command>
```

## Three operations

### 1. status — read-only, no confirmation

Trigger phrases: "status", "what's synced", "what's in canonical", "list skills across endpoints".

```bash
cd /Users/shaw/agents/skills-sync && uv run main.py status
```

Show the raw output. It prints each endpoint (`canonical`, `codex`, `claude_code`, `claude`) with skill count, file count, and the full skill list. If counts differ across endpoints, that's a signal a sync is needed — point that out.

### 2. sync — always dry-run first, then confirm, then apply

Trigger phrases: "sync", "publish my skill", "push to codex", "run skills-sync", "mirror skills".

The tool is idempotent and well-logged, but Shaw wants the safety of seeing the plan before it happens. Follow this three-step flow:

**Step 1 — dry-run:**

```bash
cd /Users/shaw/agents/skills-sync && uv run main.py sync --dry-run
```

**Step 2 — show the plan and interpret it.** Output is a list of:

- `COPY claude -> canonical: <skill>/` — skill will be written to the canonical repo from Claude Desktop
- `COPY claude -> codex: <skill>/` — mirrored to Codex
- `COPY claude -> claude_code: <skill>/` — mirrored to Claude Code
- `DELETE <endpoint>: <skill>` — skill was removed from Claude Desktop; tool will remove it downstream too
- `CONFLICT <path>: changed in a, b` — same file diverged across endpoints (rare)

If the output says **"No changes to sync"**, stop. Tell Shaw nothing needs doing.

If there are **conflicts**, flag them prominently. The tool writes `*.<endpoint>-conflict.*` files into canonical and **skips the git commit**. Shaw needs to manually reconcile; don't try to auto-resolve.

**Step 3 — confirm and apply.** Something like: *"Dry-run shows N copies and M deletes. Want me to apply?"* Wait for his OK, then:

```bash
cd /Users/shaw/agents/skills-sync && uv run main.py sync
```

Show the result. On success you'll usually see `Committed canonical skills repo: Sync skills` — mention the commit happened. If Shaw wants to inspect canonical changes before committing, add `--no-commit`.

### 3. remove — always dry-run first, then confirm, then apply

Trigger phrases: "remove X from codex", "drop X from canonical", "get rid of skill X in the targets".

**Step 1 — dry-run:**

```bash
cd /Users/shaw/agents/skills-sync && uv run main.py remove <skill-name> --dry-run
```

**Step 2 — show where it'll be removed from.** Output lists each endpoint holding the skill.

**Step 3 — confirm and apply.**

```bash
cd /Users/shaw/agents/skills-sync && uv run main.py remove <skill-name>
```

**Important caveat to surface to Shaw:** `remove` only touches canonical + targets. It does **not** delete the skill from Claude Desktop. If Shaw wants to retire a skill permanently, he needs to delete it in Claude Desktop first — otherwise the next scheduled sync will restore it everywhere.

## Flags worth knowing

- `--dry-run` — preview mode, already baked into the flows above.
- `--no-commit` — on `sync` or `remove`, skip the canonical git commit so Shaw can inspect changes before committing.

## Reading common outputs

| Output line | Meaning |
|---|---|
| `No changes to sync. N files unchanged.` | Everything is in lockstep. Done. |
| `Committed canonical skills repo: Sync skills` | Plan applied and canonical git commit landed. |
| `No canonical Git changes to commit.` | Targets updated, but canonical was already current (e.g., only codex was behind). |
| `Skipping commit because conflicts were created.` | Conflicts exist. Commit deliberately skipped. Shaw must resolve. |
| `Lock exists: ...` | A prior run didn't clean up. See troubleshooting below. |

## Troubleshooting

- **`Lock exists: /Users/shaw/agents/skills-sync/skills-sync.lock`** — check if another sync is running (`ps aux | grep skills-sync`). If nothing's running, the lock is stale; remove the file and retry.
- **`Warning: manifest not found for claude: ...`** — the Claude Desktop `manifest.json` path in `config.toml` is stale (session IDs rotate). Shaw needs to update `[claude].path` and `[claude].manifest_path` in `/Users/shaw/agents/skills-sync/config.toml`. Don't try to auto-fix.
- **Conflicts written to canonical** — surface them clearly and stop. The tool intentionally doesn't resolve these; Shaw decides which version wins.

## Logs

Every run appends to `/Users/shaw/agents/skills-sync/.logs/skills-sync.log`. If Shaw asks "what happened last time" or "did the scheduled sync run", check there first:

```bash
tail -n 30 /Users/shaw/agents/skills-sync/.logs/skills-sync.log
```

## What this skill does NOT do

- Create or edit skills → use `skill-creator` / `skill-updater`.
- Filter sync to a single skill → the tool is all-or-nothing by design; don't try to finesse it.
- Touch Claude Desktop's skill folder directly → Claude Desktop is authoritative; the only way skills enter the pipeline is through it.
