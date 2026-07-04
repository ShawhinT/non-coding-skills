---
name: sfc-helper
description: Strategy-aware LinkedIn content ideation for Shaw's SFC pipeline. Researches recent client call transcripts, the CRM, and post analytics, surfaces the concrete raw material (quoted pains, aha moments, honest numbers), turns it into hooks on request, proposes a week's lineup, and on approval creates SFC database pages as briefings. Also works a single existing SFC page end-to-end: count or develop its hooks, then draft into it. Use whenever Shaw wants LinkedIn post ideas, asks 'what should I post', wants to plan or fill his content calendar, wants hooks for a specific post idea, or wants to turn strategy/analytics findings into scheduled posts. Trigger even when he doesn't say 'SFC' (e.g. 'brainstorm posts', 'plan my week of content', 'what's worth posting', 'how many hooks for this idea'). Do NOT use for drafting the full text of one post (use linkedin-post-writer) or analyzing past performance (use linkedin-post-analytics); this is the ideation and scheduling layer between them.
---

# SFC Helper

Turn Shaw's strategy, recent client conversations, and post analytics into a planned week of LinkedIn content — ending in SFC database pages he can act on. This is the ideation layer: it decides *what* to post and *why*, maps it to the strategy, and stages it. It does not write the finished post copy and it does not pull analytics — it composes with two sibling skills for those.

## How this skill composes with others

- **`linkedin-post-analytics`** produces the numbers (the top/bottom split analysis, what's working). Pull its latest findings as an input; don't recompute them here.
- **`sfc-helper`** (this skill) does research → surface the raw material → (optionally) turn it into hooks → propose a week → create SFC briefing pages.
- **`linkedin-post-writer`** drafts the full post text in Shaw's voice. This skill stops at *briefings* (the angle and key points), not finished drafts. When Shaw wants a post written out, hand off to `linkedin-post-writer`.

Keeping these boundaries clean is the point: the SFC page holds a brief, and the draft gets written later (often the morning of) so it's fresh.

## Three modes: the week, the single page, and the repurpose

The full Workflow below plans a *week* from client research. But Shaw often points at **one existing SFC page** and wants to develop just that post — "how many hooks for this idea?", "give me hooks for this", "draft this one". When that's the ask, run the lighter path and skip the week machinery:

- **Skip Steps 1–2** (client research, analytics). Fetch the page, work from the briefing already on it, and stay scoped to that one idea. Don't spin up subagents for a single-page request.
- **The page title is the hook direction; the body is the payoff.** Anchor hooks to the title's framing and make sure they pay off into the options/points already briefed on the page (this is `linkedin-post-writer` Step 4's rule — read it). If the page has no hooks yet, answer the literal question plainly ("zero so far") before offering to add some.
- **When Shaw brings his own hook, sharpen it — don't replace it with a from-scratch menu.** If he proposes a direction ("a bold statement that AI-native businesses outperform"), your job is to refine and pressure-test *his* angle: offer 2–3 tight variations of it and name the one risk it carries (e.g. an analogy whose real-world timescale undercuts the urgency he's going for), so he can choose with eyes open. The generated menu is for when he asks "give me hooks," not when he already has one.
- **On approval, draft and write it in.** When he picks a hook and says draft it, hand off to `linkedin-post-writer`, then append the chosen hook + full draft to the page body *below* the existing briefing (use `insert_content` at the end, don't replace) and keep the ⬜ icon. A single-page draft can live on the page as a labeled `## Draft` even though the week-planning path stops at briefings.

### Repurpose mode: re-running a proven post on another channel

Sometimes the input is neither client research nor an existing page — it's **post analytics**. Shaw picks his best-performing posts (via `linkedin-post-analytics`) and wants them staged to run again on another channel, usually **YT Community**. This mode inverts the skill's usual output: the deliverable is the *exact original copy*, not a briefing, because the post already proved itself and only needs re-placing.

- **Skip the week machinery (Steps 1–3, 5).** The selection is analytics-driven, so there's no research or sequencing to do. Still dedupe against the backlog (Step 4), and still propose the lineup and wait for approval before creating pages.
- **Set `Channel` to the target** (e.g. `YT Community`), not the default LinkedIn — here the channel switch is the whole point.
- **Carry over the verbatim copy.** Pull each post's exact text from LinkedIn via the `linkedin-post-analytics` feed API (the `commentary.text.text` field) and put it on the page in a fenced code block, so line breaks survive and it's one-click copyable. A briefing can't recreate a post that won on its specific wording.
- **Flag the media.** Copy alone isn't the whole post — check each source post's `content` for an `imageComponent` (or video/document) and pin a prominent note on the pages that have one (`> 📷 Includes an image — pull it from the original before publishing`). Text-only posts get no note; skipping this silently strips the post's visual.
- **Dates follow whatever cadence Shaw names** (e.g. MWF starting today); the reach-early sequencing logic doesn't apply to a repurpose run.

## Strategy is the backbone

Every idea has to serve Shaw's actual go-to-market. Read `references/strategy.md` for the distilled version (avatar, the barbell model, the comment habit, cadence). Also read the live source of truth before proposing — it evolves:

- **LinkedIn Strategy** page (Notion): `[page-id]`
- **Current quarter avatar** (Q2 2026 strategy): `[page-id]`

If those pages have shifted since `references/strategy.md` was written, trust the pages and flag the drift.

## Workflow

### Step 0: Load strategy
Read `references/strategy.md` and the two live pages above. Hold the avatar (50–200-person tech companies; the sponsor + champion buying committee; governance as the universal gate) and the barbell in mind for everything that follows.

### Step 1: Research recent client signal
The strongest, least-generic ideas come from what clients actually said. Pull the last ~2 weeks of client conversations and mine them for content.

- Get current clients from the **Clients (Nurture)** data source: `[page-id]`.
- For each client with recent activity, read their CRM page's `## Calls` section and follow the linked **ABA Calls** / **ABA Trainings** pages. Fetch transcripts with `notion-fetch` using `include_transcript=true`; transcripts often live as linked Google Docs (read those with the Google Drive tool if needed).
- **Use subagents** — one per client — to dig in parallel. Each returns anonymized candidate angles: specific pains in the client's own words, governance/adoption struggles, quantified wins, objections, and vivid stories. See `references/research.md` for the subagent prompt template and which clients are on-avatar.

### Step 2: Pull the latest analytics (optional but recommended)
Glance at the most recent `linkedin-post-analytics` split findings (or run them) so ideas lean toward what's been working and away from what flopped.

### Step 3: Surface the raw material first
The default first deliverable is **not** a list of finished post angles — it's an inventory of what people actually said and realized, so Shaw can pick what resonates and tell the story himself. Packaged angles with audience tags and barbell labels read as generic and land flat; the raw ore lands.

Cluster the subagents' findings and present them under short topic headings, each with the concrete material underneath:

- **Concrete pains** — in the client's own words, quoted. ("I asked Claude how to govern it, and it scared me even more.")
- **Aha moments / realizations** — the mindset shift, quoted where possible.
- **Counterintuitive specifics** — the surprising rule, tactic, or detail (the connector trust rule, the no-Ctrl-Z guardrail).
- **Vivid stories** — the human moment (the surgeon's 18 to-do lists, the exec's worst quarter).
- **Honest numbers** — with provenance attached, per the verify-numbers principle.

Anonymize everything (see Principles). Keep the strategy and the barbell as your **private reasoning** — they decide what's worth surfacing and drive the gap check (is there governance material? a quantified-proof point? does each thread suggest a closing question?) — but don't make Sponsor/Champion/Reach tags the headline of the output. Lead with ore, not packaging.

**If Shaw asks for hooks**, first read `linkedin-post-writer`'s hook section (its Step 4 archetypes and the "lead with the moment, not the concept" principle) and generate the menu against it — the hooks should already be in Shaw's proven voice, not idea-led restatements of the nugget. A menu of generic, concept-led hooks is worse than none. Then present them grouped under the same short topic headings — one strong hook per nugget, a second only when it gives a genuinely different vibe — drawn across all the material, varied in angle. Skip style labels unless he asks for a named voice (e.g. "in Matt Gray's style"). These hooks are a **menu of directions**, not finished copy: when he picks one, hand it back to `linkedin-post-writer` for the full draft. `linkedin-post-writer` owns hook craft — read it, don't re-teach or duplicate it here.

### Step 4: Dedupe against the SFC backlog
Before proposing, scan the SFC database for overlapping ideas (the backlog parks unscheduled posts on a single future date — see `references/sfc-database.md`). Flag duplicates rather than adding more.

### Step 5: Propose the week — then STOP
Present the lineup in plain story terms, one line per day: **day → the chosen hook (or nugget) → one line on why it sits there → the closing-question idea.** Keep the sequencing logic working underneath — reach/broad posts early in the week (they prime the algorithm to surface later posts to engaged viewers), authority and any hard CTA later — but don't clutter the presentation with audience tags and barbell jargon; Shaw reacted against that. Double up on a day for event promos rather than displacing a CTA. **Wait for Shaw's approval before creating anything.** This is a propose-first skill.

### Step 6: On approval, create the SFC pages
Create each as a **briefing**, not a finished post. Follow `references/sfc-database.md` for the exact schema, the briefing format, the ⬜ icon, dates, tags, and how to reuse an existing backlog page instead of duplicating it.

## Principles

- **Anonymize client material.** Never name a client or individual in a post idea. "a cybersecurity CEO," "a VC firm's CFO," "a policy director" — never the real name or company.
- **Verify numbers before they go in a brief.** The big lesson from past sessions: a quantified claim has to be a real, attributable before/after, and you must distinguish a *manual baseline → AI* result from *first-AI-run → refined-skill*. If the manual baseline wasn't captured, say so and frame the number honestly (e.g., "~1 hour, her estimate"), or flag it to confirm. Don't inflate or conflate.
- **Briefings, not drafts.** The SFC page gets the angle, audience, key points, source, and a closing-question idea — enough that the post can be written later. Writing the full copy now is out of scope for week-planning (hand to `linkedin-post-writer`). The exception is the single-page mode above, where Shaw explicitly asks to draft *this* post now.
- **Build on Shaw's angle, don't override it.** When Shaw arrives with his own hook or framing, refine and stress-test it rather than substituting your own idea-led menu. Pressure-testing means naming the one real weakness (a shaky analogy, an over-claimed number, a buried payoff) and offering tighter variants of *his* direction — he keeps authorship, you sharpen the edge.
- **Lead with ore, not packaging.** Surface what people actually said and realized — quoted pains, aha moments, vivid specifics, honest numbers — not finished post packages with audience labels. Shaw tells the story; your job is to hand him the genuinely valuable raw material.
- **One post, one role.** Each idea targets the sponsor or the champion, not both. Posts that try to serve everyone serve no one (that's the dead "abstract analogy" middle).
- **Lead with reach, bury the ask.** Front-load the week with reach posts; weave CTAs in late, on a warmed audience.
