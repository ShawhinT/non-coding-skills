---
name: linkedin-post-writer
description: Draft LinkedIn posts in Shaw's personal writing style. Use this skill whenever Shaw asks to write, draft, brainstorm, or edit a LinkedIn post — including phrases like "write a post about", "help me draft a LinkedIn update", "turn this into a LinkedIn post", "post idea", or any reference to writing for LinkedIn. Also trigger when Shaw shares a topic, milestone, or idea and asks to "make it a post" or "write this up." Even casual requests like "can you LinkedIn-ify this" or "help me announce X" should trigger this skill.
---

# LinkedIn Post Writer

Write LinkedIn posts that match Shaw's voice and content philosophy. The examples are the primary guide — read them, internalize the feel, and let them shape your drafts more than any rule in this document.

## How to Use Examples

Examples are split by post type in the `references/` folder:

- `examples-educational.md` — Builder's Logs, frameworks, tech stacks, how-I-do-X
- `examples-thesis.md` — Opinion posts, trend analysis, bigger ideas
- `examples-video-bridge.md` — Posts that bridge to a YouTube video or blog
- `examples-promo.md` — Event promos, resource promos, milestone announcements

**After choosing a post direction, read the matching example file(s).** If the post bridges to a video, also read `examples-video-bridge.md`. Pick 2-3 specific examples as your reference points while drafting.

After drafting, compare your draft to those examples. Does it feel like them in density, weight, and tone? If the examples wouldn't include a section you wrote, that section is probably scaffolding. Cut it.

## Hard Rules

These are guardrails, not construction instructions. They catch mistakes — they don't tell you what to build.

- **Em dash limit.** At most one em dash ("—") per post. Prefer zero.
- **No clichés or hype.** No metaphors, idioms, or business jargon. Forbidden: "game-changer," "move the needle," "raise the bar," "secret sauce," "level up," "hit the ground running," "low-hanging fruit," "unlock" (figurative), "double down," "win-win," "take it to the next level," "circle back," "think outside the box."
- **No motivational CTAs.** Forbidden: "What inspires you?", "What's your best lesson?", "What motivates you?", "Never give up", "It compounds."
- **No tricolons with negation.** Forbidden pattern: "No X, no Y—just Z."
- **Authenticity.** Never fabricate Shaw's experiences, results, or opinions. Only reference what Shaw provides, what appears in past posts, or established facts.
- **No unverifiable scale claims.** No "infinite," "limitless," "no ceiling." Bounded ranges ("10x, 100x") are fine.

## Writing Principles

These explain *why* Shaw's writing works. Internalize them rather than treating them as a checklist to comply with.

**The examples are the source of truth.** When a principle and an example seem to conflict, follow the example. The examples show what Shaw actually publishes. The principles are approximations.

**Show, don't scaffold.** If the content demonstrates a concept, don't define it first. A 4-step process that creates Skills *shows* what Skills are — a preceding paragraph explaining "what are Skills" is redundant. Before including any setup or definition, ask: would the post still make sense without this? If yes, cut it.

**Lean by default.** Every element — descriptions, closers, conceptual bridges, jargon definitions — must earn its place. If the reader could infer it, cut it. List items that are self-explanatory don't need descriptions. A body that naturally leads into the video bridge doesn't need a separate closer. Shaw's best posts feel like every word is load-bearing.

**Generous peer, not thought leader.** Shaw shares what he's found, in case it's useful. The energy is "here's what I found" not "here's what you should know." Light self-deprecation (😅, :P, 😬) undercuts anything that might read as bragging — but only in posts with an emotional register (milestones, personal stories). Educational and promotional posts don't need it; inserting personal asides can dilute the focus.

**Specificity is credibility.** Concrete numbers, tool names, dollar amounts, real outcomes. Never generic observations anyone could make. Don't write "I see this in my work and in the teams I train." Write "Claude Code writes ~99.9% of my code."

**One idea, one post.** Never cover two topics. If you can't state the post's single idea in one sentence, it's too broad.

**Technology is personal.** Never discuss tech in the abstract. Ground it in Shaw's specific experience — what he pays, what he uses, what broke, what clicked.

**Parentheticals add texture.** Shaw uses parenthetical asides naturally — "(and it is)", "(which is the fun part)", "(huge)". They add qualifiers and real-time context without breaking flow. Don't force them in, but notice that Shaw's posts usually have a few.

**Every line moves forward.** If a line restates the hook or echoes an earlier point, cut it. The reader should learn something new from every sentence.

## Formatting

Mobile-first LinkedIn consumption. These are sensible defaults, not mandates.

- **One sentence per line.** Treat line breaks like punctuation.
- **Numbered lists for steps and ranked items.** Keep list items short — cut sub-clauses and qualifiers into prose before or after the list.
- **Bullets sparingly.** For quick lists within a narrative, never as the entire post structure.
- **Emoji as functional punctuation.** 👇 = scroll down, 👉 = CTA/link, 😅 = self-deprecation, 🥳 = celebration. Max 2-3 per post. Never decorative.
- **One link in the body.** Extras go in comments after posting.
- **Footer CTAs are optional.** If using, separate with `--` and keep to 1-2 lines.

## Post Types

These are loose shapes, not rigid templates. The examples show how they actually play out — read the relevant example file to see the shape in practice.

**Builder's Log** — Process, tech stack, how-I-do-X. Walk through tools or steps. Practical, no fluff. Can carry 6-8 short items. (See `examples-educational.md`)

**Thesis Post** — Opinion, trend, bigger idea. Build a narrative arc: status quo → tension → resolution. 2-3 conceptual moves max. Include a "so what" connecting to broader stakes. (See `examples-thesis.md`)

**Framework Post** — Educational breakdown of a model or mental framework. Define levels, stages, or categories. Each one earns its place with a concrete example or one-line explanation. (See `examples-educational.md`)

**Milestone/Announcement** — Where you were → what was hard → what you learned. Anchor to specific numbers and timelines. (See `examples-promo.md`)

**Video/Blog Bridge** — The post makes people *care* about the topic (the why). The video teaches it (the how). Don't mirror the tutorial's structure — that makes the post redundant. The post should stand alone as valuable even if nobody clicks. Frame the bridge naturally: "In a recent YouTube video, I walk through the full framework with concrete examples." (See `examples-video-bridge.md`)

**Promo/Resource** — Event promos, free resource shares. Value-first framing: what the reader gets, not what Shaw is selling. Soft CTAs woven into narrative, never the main event. (See `examples-promo.md`)

## Writing Process

### Step 0: Direction check

Before drafting, present Shaw with 2-3 possible directions using AskUserQuestion. Each direction: one-line angle, who it speaks to, likely post type. Directions should vary meaningfully — not three versions of the same angle.

### Step 1: Read examples

After Shaw picks a direction, read the matching example file(s) from `references/`. Pick 2-3 specific examples as reference points for this draft.

### Step 2: Clarify purpose

State in one line each:
- **Purpose:** What is this post communicating?
- **Audience:** Who benefits?
- **Post type:** Which shape?
- **Reference examples:** Which 2-3 examples are guiding this draft?

### Step 3: Write the body

Write the body first. This is the substance. Ground every claim in Shaw's actual experience. Let the reference examples guide density and weight — if your body is twice as long or twice as dense as the examples, something is off.

### Step 4: Brainstorm hooks

This is the most important step. Spend real effort here.

Write 3-5 hook directions. For each, write why it could work and what risk it carries. Consider the hook's *promise* — "here's why" promises reasoning (Thesis Post), "here's how" promises process (Builder's Log). The hook determines the post structure.

Then pick the strongest and write the full 1-2 line hook.

Hook archetypes that work for Shaw:
- **Contrarian claim:** "Here is something I believe (that people will disagree with)."
- **Milestone/confession:** "15 months ago, I launched X. Today, I'm closing it down."
- **Bold framing:** "If there's a single technique responsible for modern AI agents, it's this…"
- **Numbered promise:** "Why I pay $160/mo for AI tools…(and how I use them)"
- **Challenge/countdown:** "I have 29 days to ship an AI app."
- **Problem/solution:** Start with the problem the reader faces.
- **Result/number:** Lead with a specific outcome.

Hooks are two-line systems. The second line pulls the reader forward — ellipsis, "And", "But", or playful punctuation (:P, 😅) can all create momentum past the "see more" fold. There's no single right technique. Study how the reference examples open and match the energy.

### Step 5: Write the CTA

One clear, specific question. No "or" / "and" splitting attention. Answerable in one sentence but invites real thought.

### Step 6: Assemble and compare

Put together hook + body + CTA. Then compare the full draft to your reference examples:
- Does it feel like the same person wrote both?
- Is it the same density and weight?
- Would the example posts include every section you wrote?

If something feels like scaffolding the examples wouldn't have, cut it.

### Step 7: Present the draft

Show Shaw the completed post. Note which examples guided the draft.

## Post Length

Most posts: 150-300 words. Listicles can run longer. Thesis posts up to 400 if the argument requires it. Never pad for length.
