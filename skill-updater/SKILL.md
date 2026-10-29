---
name: skill-updater
description: Improve, audit, or simplify an existing skill from feedback and observed results. Owns every change to a saved skill; skill-creator authors new ones. Use when the user asks to update, fix, prune, slim down, or add a learning to a skill, however casually phrased ("let's update the skill", "the skill should know about this", "add this to the skill"), or to review skills after a model or platform change.
metadata:
  author: Shaw Talebi (aibuilder.academy)
  source: https://github.com/ShawhinT/aba-plugins
---

# Skill Updater

Improve existing skills through proposals first, then approved changes. Favor reusable principles over accumulated exceptions.

Every change runs the same four steps. What varies is the evidence and the scope: a one-line fix reads the section it touches and scans the rest for the same idea; a full audit reads every file in the package.

## 1. Diagnose

Evidence comes from two sources, and each has its own lens.

**Conversational evidence** is what a session surfaced: user corrections, edited artifacts, execution traces that differed from what the skill produced, and steps the transcript shows caused unnecessary work. Read the trace, not just the outcome. Use it to distinguish missing guidance from instructions that conflict, overreach, are outdated, or were correct but not followed. An execution failure does not necessarily require a skill edit; recommend no change when no durable improvement is justified.

Work backward from the observed failure through successive causes until reaching the deepest cause the evidence supports. Center the proposal on repairing that cause first, then trace its effects forward: omit fixes for downstream symptoms that the root repair would resolve. Keep additional edits only for independent causes; a well-framed symptom fix is still bloat once the root is repaired. Do not invent a deeper cause to make the explanation tidy. Prioritize the user's complaint over self-observed friction.

**Structural evidence** is the skill's own text read against the current model and platform. When there is no conversation to draw on, only the skill and the world it now runs in, that is an audit: read the whole package. Prune concrete redundancy and verified stale guidance. Verify platform and tool claims against the current environment or an authoritative source, and point to a live source where one exists. The test for everything else is derivability, not obviousness: would the current model do this correctly given only the goal and the durable facts? A newer model or confidence that guidance is "obvious" does not establish that it is dispensable. A framework or decision criterion is a choice, not a capability gap; a smarter model does not make it removable. A constraint you cannot derive may guard an incident you cannot see: cutting its explanation loses nothing, cutting the constraint loses something unrecoverable, so name what it protects when proposing to remove it. The goal is removing content that no longer earns its place, not a shorter file; a long skill with nothing stale passes unchanged.

Both lenses apply to every change. Stale content noticed while making a targeted edit goes into the proposal as a recommended item, separate from the requested change, rather than being removed silently or ignored.

## 2. Design the revision

Consider deletion, replacement, clarification, and consolidation before adding instructions. Repair a contradiction at its source rather than layering on an exception. Change the specific sentences that need changing and leave the rest untouched; regenerating a whole file loses working rules and drifts toward the generic. When broader simplification is requested, consolidate the structure while preserving useful procedures, decision criteria, examples, and constraints.

Frame revisions as reusable principles: explain the objective, why it matters, and the judgment that applies across situations. Prefer a governing principle to a growing checklist of case-specific dos, don'ts, and if/then rules. Keep concrete requirements when they express an explicit user preference, a necessary procedure, or an operational boundary. Generalize only as far as the evidence supports; omit one-off case details.

Route each learning to where it belongs. Once a skill triggers, its whole body is loaded into every later turn, so long examples and scripts used only sometimes belong in a reference file that SKILL.md links to directly:

| Belongs in | Use for |
|---|---|
| **SKILL.md** | Reusable task guidance needed on every run: conventions, workflow steps, decision criteria |
| **Supporting file** | Substantial examples, scripts, templates, or assets that only Claude needs |
| **External record** | Shared or independently changing information with an authoritative source outside the skill, which the skill points to and pulls at run time |
| **Memory** | User preferences and project context, when the surface has memory |
| **Nowhere** | One-off decisions, incident history, anything derivable from the code or examples |

## 3. Review

Always show a concrete proposal before changing a saved skill or delivering an installable replacement: what changes, where, why, and any material tradeoff. A general request to improve or fix a skill does not approve edits the user has not seen; approved means the user has seen the concrete edit, and a request that pins the exact text and leaves no judgment call is its own approval. Once specific changes are approved, proceed without asking again. A preview shown for review is not an update; an installable file or a savable card is a commit and sits behind approval.

Use the current authoritative version and compare before and after. Check for unintended changes, contradictions, duplication, broken references, and loss of useful guidance. The routing description is its own artifact: third person, what the skill does and when to use it, plus what distinguishes it from sibling skills, within 1,024 characters (over the cap, the skill fails to load).

Where the skill has an eval or verifier, run it before and after and accept only changes that do not regress what already worked. Reading the edited text and judging it sound is not evidence the skill performs better. Say which one you did.

## 4. Deliver

Check in this order:

- **Plugin-owned skill:** use the plugin's own update process. A personal copy shadows the plugin's copy and never reaches its other users.
- **Writable in place (e.g., Claude Code):** edit the saved files directly and verify the result.
- **Everywhere else:** copy the whole skill directory, apply every approved edit, and ZIP it as `<name>.skill`. Package even when a one-click write or review-card call exists: those calls churn between releases and replace SKILL.md alone, dropping references and assets. Use one only when the user names it, and pass the routing description verbatim in whatever field the call labels as the description, because that field lands on the saved frontmatter.

Build from the latest approved content, not the installed cache, which does not refresh after a write; re-apply same-session edits before zipping. For full-file replacements, edit a copy on disk and diff it before sending, since nothing echoes back what landed. Never substitute SKILL.md alone, pasted text, or assembly instructions for the package, and never report a partial update as complete.
