---
name: sfc-helper
description: Strategy-aware LinkedIn content ideation for Shaw's SFC pipeline. Works from a pre-mined Q&A file (the workhorse 'mine-file' mode), a single existing SFC page, or a proven post being repurposed to another channel: audits the idea against the backlog, turns it into hooks on request, and on approval stages it as an SFC database page. Use whenever Shaw wants LinkedIn post ideas, asks 'what should I post', wants to plan or fill his content calendar, wants hooks for a specific post idea, wants a painful post drafted from the qa_pairs file, or wants to turn strategy/analytics findings into scheduled posts. Trigger even when he doesn't say 'SFC' (e.g. 'brainstorm posts', 'plan my week of content', 'what's worth posting', 'how many hooks for this idea'). Do NOT use for drafting the full text of one post (use linkedin-voice) or analyzing past performance (use linkedin-post-analytics); this is the ideation and scheduling layer between them.
---

# SFC Helper

Turn Shaw's strategy, pre-mined call material, and post analytics into staged LinkedIn content — ending in SFC database pages he can act on. This is the ideation layer: it decides *what* to post and *why*, maps it to the strategy, and stages it. It does not write the finished post copy and it does not pull analytics — it composes with two sibling skills for those.

## How this skill composes with others

- **`linkedin-post-analytics`** produces the numbers (the top/bottom split analysis, what's working). Pull its latest findings as an input; don't recompute them here.
- **`sfc-helper`** (this skill) takes the raw material (a pre-mined Q&A file, an existing SFC page, or a proven post) → audits it against the backlog → (optionally) turns it into hooks → stages it as an SFC page.
- **`linkedin-voice`** drafts the full post text in Shaw's voice. This skill stops at *briefings* (the angle and key points), not finished drafts. When Shaw wants a post written out, hand off to `linkedin-voice`.

Keeping these boundaries clean is the point: the SFC page holds a brief, and the draft gets written later (often the morning of) so it's fresh.

## Three modes: mine-file, single page, and repurpose

The skill runs in one of three modes depending on the raw material Shaw brings. **Mine-file mode** is the workhorse — a painful post straight from a pre-mined Q&A file — and has its own self-contained procedure in `references/transcript-posts.md` (audit first, pick for pain, anchor on the verbatim quote, close the edit loop). The other two are below.

### Single-page mode: developing one existing SFC page

Shaw often points at **one existing SFC page** and wants to develop just that post — "how many hooks for this idea?", "give me hooks for this", "draft this one":

- Fetch the page, work from the briefing already on it, and stay scoped to that one idea.
- **The page title is the hook direction; the body is the payoff.** Anchor hooks to the title's framing and make sure they pay off into the options/points already briefed on the page (this is `linkedin-voice`'s hook rule — read it). If the page has no hooks yet, answer the literal question plainly ("zero so far") before offering to add some.
- **When Shaw brings his own hook, sharpen it — don't replace it with a from-scratch menu.** If he proposes a direction ("a bold statement that AI-native businesses outperform"), your job is to refine and pressure-test *his* angle: offer 2–3 tight variations of it and name the one risk it carries (e.g. an analogy whose real-world timescale undercuts the urgency he's going for), so he can choose with eyes open. The generated menu is for when he asks "give me hooks," not when he already has one.
- **When Shaw asks for a hook menu, run `linkedin-voice`'s Hook process rather than improvising a shorter one.** That process owns the format (10 candidates, split 5 in Shaw's voice / 5 in named creators' voices, presented as two labeled sections) as well as the craft. Read it and generate against it — a menu of generic, concept-led restatements of the nugget is worse than none. These hooks are a **menu of directions**, not finished copy; when he picks one, hand it back to `linkedin-voice` for the full draft. `linkedin-voice` owns hook craft — read it, don't duplicate it here.
- **On approval, draft and write it in.** When he picks a hook and says draft it, hand off to `linkedin-voice`, then append the chosen hook + full draft to the page body *below* the existing briefing (use `insert_content` at the end, don't replace) and keep the ⬜ icon. A single-page draft can live on the page as a labeled `## Draft`.

### Repurpose mode: re-running a proven post on another channel

Sometimes the input is neither a mined Q&A file nor an existing page — it's **post analytics**. Shaw picks his best-performing posts (via `linkedin-post-analytics`) and wants them staged to run again on another channel, usually **YT Community**. This mode inverts the skill's usual output: the deliverable is the *exact original copy*, not a briefing, because the post already proved itself and only needs re-placing.

- **The selection is analytics-driven**, so there's no ideation to do — just re-place proven copy. Still dedupe against the backlog (see `references/sfc-database.md`), and still propose the lineup and wait for approval before creating pages.
- **Set `Channel` to the target** (e.g. `YT Community`), not the default LinkedIn — here the channel switch is the whole point.
- **Carry over the verbatim copy.** Pull each post's exact text from LinkedIn via the `linkedin-post-analytics` feed API (the `commentary.text.text` field) and put it on the page in a fenced code block, so line breaks survive and it's one-click copyable. A briefing can't recreate a post that won on its specific wording.
- **Flag the media.** Copy alone isn't the whole post — check each source post's `content` for an `imageComponent` (or video/document) and pin a prominent note on the pages that have one (`> 📷 Includes an image — pull it from the original before publishing`). Text-only posts get no note; skipping this silently strips the post's visual.
- **Dates follow whatever cadence Shaw names** (e.g. MWF starting today).

## Strategy is the backbone

Every idea has to serve Shaw's actual go-to-market. Read `references/strategy.md` for the distilled version (avatar, the barbell model, the comment habit).

**Whenever the task involves laying out or rescheduling a week — not just picking ideas — also read `references/scheduling-principles.md`.** It governs volume, reach/engagement alternation, tee-up spacing, merge/split, format, and CTA handling, and it supersedes any cadence advice found elsewhere.

Also read the live source of truth before proposing — it evolves:

- **LinkedIn Strategy** page (Notion): `[page-id]`
- **Current quarter avatar** (Q2 2026 strategy): `[page-id]`

If those pages have shifted since `references/strategy.md` was written, trust the pages and flag the drift.

The backlog cross-reference — read a row's status from its Date, dedupe against the upcoming-Sunday backlog plus the last ~4 weeks, and check hook freshness before committing — is canonical in `references/sfc-database.md` and inlined into the mine-file procedure in `references/transcript-posts.md`. Run it in every mode before creating or rescheduling a page.

## Principles

- **Anonymize client material.** Never name a client or individual in a post idea. "a cybersecurity CEO," "a VC firm's CFO," "a policy director" — never the real name or company.
- **Verify numbers before they go in a brief.** The big lesson from past sessions: a quantified claim has to be a real, attributable before/after, and you must distinguish a *manual baseline → AI* result from *first-AI-run → refined-skill*. If the manual baseline wasn't captured, say so and frame the number honestly (e.g., "~1 hour, her estimate"), or flag it to confirm. Don't inflate or conflate.
- **Briefings, not drafts.** By default an SFC page gets the angle, audience, key points, and source — enough that the post can be written later; writing the full copy is `linkedin-voice`'s job. The exceptions are the modes where Shaw explicitly asks to draft *this* post now (single-page and mine-file) and repurpose mode, whose page holds verbatim proven copy rather than a briefing.
- **Build on Shaw's angle, don't override it.** When Shaw arrives with his own hook or framing, refine and stress-test it rather than substituting your own idea-led menu. Pressure-testing means naming the one real weakness (a shaky analogy, an over-claimed number, a buried payoff) and offering tighter variants of *his* direction — he keeps authorship, you sharpen the edge.
- **Lead with ore, not packaging.** Surface what people actually said and realized — quoted pains, aha moments, vivid specifics, honest numbers — not finished post packages with audience labels. Shaw tells the story; your job is to hand him the genuinely valuable raw material.
- **One post, one role.** Each idea targets the sponsor or the champion, not both. Posts that try to serve everyone serve no one (that's the dead "abstract analogy" middle).
- **Propose first, create on approval.** Present the idea or lineup and wait for Shaw's go-ahead before creating or rescheduling any SFC page. This is a propose-first skill.
