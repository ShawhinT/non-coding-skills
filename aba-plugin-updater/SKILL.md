---
name: "aba-plugin-updater"
description: "Prepare a change to Shaw's aba-plugins marketplace repo (the public plugin clients install via /plugin install aba-skills@aba) as a handoff doc for Claude Code, which executes it natively in the repo. Use whenever he wants to edit, fix, or improve one of the plugin's skills (skill-helper, skill-updater, cost-optimizer), repackage dist/, validate the manifests, or land a commit there. Triggers: \"update the plugin\", \"push a change to aba-plugins\", \"repackage dist\", \"cut a plugin release\", \"add this to the aba-skills plugin\". Also fire whenever one of those three skill names comes up as something to change, even without the word \"plugin\" — they are forks living in git, so the edit is NOT save_skill and NOT skills-sync. Cowork composes and verifies the change but never edits the repo directly (sandbox git writes strand lock files; the push needs Shaw's credentials). Do NOT use for personal Claude Desktop skills or for authoring brand-new skills (skill-creator)."
---

# ABA Plugin Updater

Prepares changes to the `aba-plugins` marketplace repo — the public plugin clients install with `/plugin install aba-skills@aba` — as a **handoff doc for Claude Code**, which executes the change natively in the repo on Shaw's machine.

## Why a handoff, not a direct edit

The final step (git push) always needs Shaw's credentials, so a Cowork session could never ship end-to-end. Worse, sandbox git writes leave damage even when they succeed: the mount blocks deletes, so every commit strands `.git` lock files (`index.lock`, `HEAD.lock`, tmp objects) that break the next git write until Shaw clears them by hand (observed 8/19/26). Since a human step is unavoidable either way, the reliable split is: Cowork owns the thinking, Claude Code owns the repo.

## Which skills this covers

The plugin ships three skills, at `plugins/aba-skills/skills/`: `skill-helper`, `skill-updater`, `cost-optimizer`.

These are **forks** of Shaw's personal copies, carrying universalizing edits (the acme examples, surface fallbacks, cost-optimizer's billing-surface branch — don't blind-copy personal copies over them). A change to one of these routes here — not `save_skill`, which writes a personal skill that would shadow the plugin's copy rather than update it, and not `skills-sync`, whose pipeline carries his personal skills out from Claude Desktop to his own runtimes and never touches a plugin. If a request names one of these three, it lands here.

## Workflow

1. **Compose the change.** When exact current file text is needed for anchored edits, mount the repo read-only (`request_cowork_directory` with `~/Documents/_code/_stv/_repos/aba-plugins`) and read — never write to the mount. Frontmatter `description` fields stay ≤1024 characters (over the cap = skill fails to load); check the length while composing, since Claude Code will apply the text verbatim.
2. **Write the handoff doc** to outputs as `aba-plugins-handoff-<topic>.md` and present it. Tell Shaw to point Claude Code at it from the repo root.

## What the handoff doc carries

Claude Code has the repo and its gitignored `CLAUDE.md` (the canonical workflow), so the doc carries the *change*, not a re-taught process:

- The goal in one line, plus the rationale worth preserving in the commit message.
- The exact edits: for each file, anchored old→new blocks (or full replacement content for a new or short file), composed against the repo's current text — not memory.
- The step order, deferring to `CLAUDE.md` for the canonical details: apply edits → repackage `dist/` for the changed skills only → verify each rebuilt zip against its source (`unzip -p dist/<name>.skill <name>/SKILL.md | diff - plugins/aba-skills/skills/<name>/SKILL.md`) → `claude plugin validate .` and `claude plugin validate plugins/aba-skills` → commit → push.
- The verification commands whose output proves the change landed.
- Only the universalizing rules this edit actually touches: the shared metadata block, no absolute paths to any machine, no Shaw-specific skill names as domain examples (`acme-brand-system`, not `aba-brand-system`), fallback sentences for surface-dependent features.
- An explicit line that the version stays put — bumping `plugin.json` is the release switch and is Shaw's call; content lands on main at the current version unless he says he's cutting a release.
