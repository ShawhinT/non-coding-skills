---
name: skill-updater
description: Update and repackage existing skills. Use this skill whenever the user asks to edit, update, revise, or improve an existing skill — including phrases like "update the skill", "fix the skill", "improve the skill", "change the skill", "tweak the skill", or any reference to modifying a skill that already exists. Also trigger when the user provides feedback on a skill's output and wants the skill itself changed. This is specifically for editing existing skills, not creating new ones from scratch (use skill-creator for that).
---

# Skill Updater

A lightweight workflow for editing and repackaging existing skills. This exists because installed skills live on a read-only filesystem, so edits require a specific copy-edit-package sequence.

## Why this skill exists

Skill directories under `mnt/.claude/skills/` are read-only. Attempting to edit them in place will fail with `EROFS` or `EACCES` errors. The packaging script (`package_skill.py`) lives inside the skill-creator skill directory and must be run from there. This skill captures the correct workflow so you don't rediscover it each time.

## Philosophy

### Principles over rules

The model using a skill is smart. Explain *how* and *why* — don't write a checklist of dos and don'ts. A principle helps the model reason about situations it's never seen; a rigid rule only patches the one failure that prompted it. When turning a correction into a skill update, ask: is this a transferable insight or a one-off patch? If you're writing ALWAYS or NEVER in caps, reframe as an explanation instead.

### Less is more

Every update is a two-part job: add what's needed, then look for what to cut. Scan for overlapping or redundant instructions, merge duplicates, and remove patches that the skill's structure now handles naturally. If the skill has grown noticeably, flag candidates for trimming alongside your additions. The habit: leave every skill at least as lean as you found it.

### Single source of truth

Don't duplicate instructions across skills. When the same guidance applies to multiple skills, pick one canonical home — the skill where the concept most naturally lives — and have other skills reference it (e.g., "see [skill-name] for how to handle X"). This matters because duplicated instructions drift apart over time: you fix one copy, forget the other, and eventually they contradict each other. During every update, proactively scan other skills in the directory for overlapping content and propose consolidation.

## When to use skill-creator instead

This skill is for focused, surgical edits — changing a few lines, adding a principle, fixing a behavior. If the update is substantial enough that you'd want to run test cases against the new version, benchmark before/after, or do a full eval cycle, use skill-creator's iteration workflow instead. It has subagent-based testing, a benchmark viewer, and a structured feedback loop designed for that kind of deep revision.

## Workflow

### Step 0: Summarize proposed changes before editing

After reading the conversation and identifying what to change, do three things:

1. **Proposed additions/modifications** — Summarize each change for the user to review. Present them individually so the user can approve, adjust, or reject each one.
2. **Proposed removals** — Look at the existing skill with fresh eyes and identify anything that's redundant, obsolete, or made unnecessary by the new changes. Propose these cuts alongside the additions. If nothing jumps out, say so — but actively look.
3. **Cross-skill scan** — Read through the other skills in the `mnt/.claude/skills/` directory and look for instructions that overlap with or duplicate content in the target skill (or with each other). Flag any redundancies found, recommend which skill is the canonical home for each piece of shared guidance, and propose consolidating. This is the single-source-of-truth principle in action.

Only proceed to Step 1 after the user confirms.

### Step 1: Copy to a writable location

Copy the entire skill directory to the session's writable working directory. Then fix permissions — the copy inherits the read-only permissions from the source.

```bash
cp -r /sessions/<session>/mnt/.claude/skills/<skill-name> /sessions/<session>/<skill-name>-updated
chmod -R u+w /sessions/<session>/<skill-name>-updated/
```

### Step 2: Read before editing

Read the copied SKILL.md (and any relevant reference files) before making edits. The Edit tool requires a prior Read on the same path. Read the copy, not the original.

### Step 3: Make edits

Apply all changes to the copy. If there are multiple edits, make them in sequence — each Edit call needs a unique `old_string` match.

### Step 4: Verify

Read the final file to confirm all edits landed cleanly and nothing was corrupted by overlapping edit targets.

### Step 5: Package as .skill file

The packaging script is in the skill-creator directory. Run it from there, passing the updated skill path and the outputs directory as positional arguments (not flags).

```bash
cd /sessions/<session>/mnt/.claude/skills/skill-creator && \
python -m scripts.package_skill \
  /sessions/<session>/<skill-name>-updated \
  /sessions/<session>/mnt/outputs/
```

The script takes two positional args: `<skill-path>` and `<output-directory>`. Do not use `--output` — it's not a flag, it's a positional argument, and the script will misinterpret it as a directory name.

### Step 6: Rename if needed

The script names the output after the directory, so if you used a `-updated` suffix, rename to the clean skill name:

```bash
mv /sessions/<session>/mnt/outputs/<skill-name>-updated.skill \
   /sessions/<session>/mnt/outputs/<skill-name>.skill
```

### Step 7: Share with user

Provide the computer:// link so the user can access the .skill file.

## Common mistakes to avoid

- **Editing the original path** — Will fail. Always copy first.
- **Forgetting chmod** — The copy inherits read-only permissions. Always `chmod -R u+w` after copying.
- **Using `--output` flag with package_skill.py** — The second argument is positional, not a flag. `--output` gets interpreted as a directory name and the script tries to create it in the read-only skill-creator directory.
- **Forgetting to Read the copy** — The Edit tool requires a Read on the exact file path you're editing. Reading the original at `mnt/.claude/skills/...` doesn't satisfy the requirement for the copy at `/sessions/.../`.
- **Running package_skill.py from the wrong directory** — It must be run from the skill-creator directory (`cd` into it first) because it uses relative module imports (`scripts.package_skill`).
