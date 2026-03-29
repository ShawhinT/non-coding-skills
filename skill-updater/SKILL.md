---
name: skill-updater
description: Update and improve existing skills based on conversation feedback. Use when the user asks to update a skill, improve a skill, or reflect on what was learned in a conversation to improve a skill. Also use when the user says things like "update the skill", "the skill should know about this", or "add this to the skill."
---

# Skill Updater

Improve existing skills by extracting principles from real usage — corrections, edits, and patterns that emerged during a conversation.

## Philosophy

Skills should be **minimal and principle-based**. A good skill explains *how* and *why*, not a checklist of dos and don'ts. The model using the skill is smart — give it understanding and it will handle edge cases it's never seen. Give it rigid rules and it will follow them blindly or break in novel situations.

## Workflow

### 1. Reflect on what happened

Read the conversation and identify:
- **User corrections** — where the user said "no, not that" or fixed something
- **User edits** — changes the user made directly to files that differed from your output
- **New patterns** — structural or formatting patterns that the skill doesn't currently cover
- **Wasted effort** — things the skill made you do that weren't useful

### 2. Categorize each learning

Not everything belongs in the skill. Route each insight to the right place:

| Belongs in... | Examples |
|---|---|
| **Skill** | Formatting conventions, structural patterns, workflow steps, new capabilities |
| **Reference example** | A new completed artifact showing a pattern the skill doesn't have an example of |
| **Memory** | User preferences about Claude's behavior, project context, who/what/when |
| **Nowhere** | One-off decisions, things already derivable from code/examples |

### 3. Frame updates as principles

Transform specific corrections into general principles. The test: would this help with a *different* client/project, or does it only make sense for this one case?

**Bad (rule):** "Don't ask the user about discounts"
**Good (principle):** "When a discount applies, list sessions at full price and add a discount row in green"

**Bad (rule):** "Always check the investment table after editing session titles"
**Good (principle):** "Content that appears in multiple sections (titles, durations, structural terms) must stay consistent — when one instance changes, check all others including payment terms"

Each principle should convey the *why* so the model can reason about analogous situations. If you find yourself writing ALWAYS or NEVER in caps, reframe as an explanation instead.

### 4. Make targeted edits

- Read the current SKILL.md before changing anything
- Make surgical additions — don't rewrite sections that are working fine
- When a new artifact shows a different structural pattern, copy it to `references/` as an additional example rather than trying to describe every variation in prose
- Remove instructions that caused unproductive work (check run transcripts or conversation history for evidence)

### 5. Verify

- Re-read the updated SKILL.md to confirm coherence
- Check that new reference examples match the final version of the artifact
- Ensure no duplication with existing instructions

## Anti-patterns

- **Encoding one-off decisions as permanent rules** — if it only applied to this specific client or situation, it probably doesn't belong in the skill
- **Bloating with edge cases** — if you need more than a sentence to describe a variation, add a reference example instead
- **Adding rules the user didn't ask for** — only update based on actual feedback or observed problems, not hypothetical improvements
- **Rewriting working sections** — if the user didn't have issues with a section, leave it alone
