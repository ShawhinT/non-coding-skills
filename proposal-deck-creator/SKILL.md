---
name: proposal-deck-creator
description: >-
  Build a clean, on-brand client proposal deck for Shaw / AI Builder Academy —
  the short "proposal in slide form" a prospect or partner asks for before an AI
  training or workshop engagement. Use whenever Shaw is assembling a proposal,
  pitch, or offer deck for a specific client (AI training, 1:1 Claude workshops,
  team workshops, a multi-session engagement), or says things like "make a
  proposal deck for X", "put the proposal in slides", "pitch deck for the
  [client] engagement", "turn this offer into a deck", or shares a client
  context and asks for a proposal. Also fire for a partner subcontract or
  enterprise buyer asking for a standard proposal deck, or when Shaw references
  the three-slide arc (executive summary, impact / case studies, transformation
  roadmap). Defaults to three slides but extends as needed. Composes with the
  aba-brand-system and pptx skills. Do NOT use for general slide decks unrelated
  to an ABA offer, long-form sales letters (use sales-letter-writer), or
  one-pagers (use conversion-copy).
---

# Proposal Deck Creator

Build the short, polished slide deck a client asks for when they want "the proposal in deck form" before committing to an AI training or workshop engagement. The job is half research (gathering *real*, defensible impact) and half design (a clean, on-brand, scannable deck). Do the research first; a beautiful deck full of vague claims fails.

This skill **composes with two others** — always use them together:

- **`aba-brand-system`** for color, type, voice, and the AI-slop bans. Read it before writing any copy or choosing colors.
- **`pptx`** for the build mechanics (pptxgenjs) and the mandatory visual-QA loop. Read its `pptxgenjs.md` before building.

## Order of operations (do not skip ahead)

1. **Scope** the proposal with the client's context.
2. **Research** real impact and case studies from the sources Shaw points you to.
3. **Confirm** structure and the featured case studies with Shaw.
4. **Build** the deck with the pptx skill and ABA brand.
5. **QA** visually with fresh-eyes subagents.
6. **Save and present.**

Building before the research is done is the most common failure. The case studies *are* the proposal's credibility; get them right before opening pptxgenjs.

---

## Step 1 — Scope the proposal

Gather (from the conversation, Notion, or by asking):

- **Who is the client and audience?** Enterprise buyer, partner subcontract, the specific roles in the room (executives, AI champions, engineers). The audience drives the impact slide's segmentation.
- **What's the offer?** 1:1 Claude workshops, team workshops, a multi-session engagement, a retainer. Pull the real session structure if it exists (e.g. an "AI Training Overview" or workshop outline page).
- **Any client conventions?** Some enterprises (e.g. [Company]-group entities) expect a specific font or a purpose-first "A3" structure. Honor the client's font convention on the deck while keeping ABA's accent and voice. If the client specified fonts, use them; otherwise default to a safe, clean sans.
- **What must stay off the deck?** Pricing usually lives in the partner/commercial layer, not the customer-facing deck — confirm before including any numbers.

## Step 2 — Research real impact (ask where to look)

Do not invent metrics. **Ask Shaw where to research** before mining — he knows which sources are relevant for this client. Typical sources, each good for different material:

- **Testimonials database** — client-approved, named, quotable results (safest to show).
- **Engagements ledger** — per-project "Results" sections with quantified outcomes.
- **Past training / workshop pages** (ABA Trainings) — what individuals built and the time it saved.
- **Sales / discovery call pages** (ABA Calls) — pains in the client's own words.
- **Intake form responses** (Google Drive sheet) — the *before* numbers ("this took me 1–2 hours, twice a week"). Gold for "before → after" framing.

When the research is broad, **spawn one subagent per source in parallel** (this is much faster and keeps each focused). Have each return concrete, quantified data points with source links, and a verified-vs-anecdotal flag.

**Tag every item as a "Case study" or an "Example."** A case study is a real result from a real person/engagement (mark it, attribute or de-personalize per Shaw's preference). An example is an illustrative capability not yet tied to a specific client (e.g. a live demo you can run). Keeping these honestly separated is what makes the deck defensible in the room — never label an example as proven.

See `references/impact-slide-patterns.md` for how to turn raw research into slide content.

## Step 3 — Confirm structure and featured case studies

Before building, show Shaw the **menu of researched use cases grouped by audience** and let him pick which to feature (typically one to three per audience section). Don't guess — he'll know which land for this client. Also confirm the slide list (the default below, or extended).

## Step 4 — Build the deck

Default structure is three slides; extend when the proposal needs it (project org, scope, next steps). Full per-slide patterns are in `references/structure-patterns.md`:

1. **Executive summary** — purpose (one concrete sentence), then what / why / outcomes.
2. **The impact** — case studies segmented by audience, each tagged Case study or Example.
3. **Transformation roadmap** — a staged arc (e.g. Activation → Adoption → Expansion) with an always-on governance Foundation.

Build with pptxgenjs via the **pptx** skill. Use the `scripts/deck_scaffold.js` starter so you don't rewrite boilerplate — it sets up the wide layout, the ABA palette, the icon rasterizer, the card/shadow helpers, and a shared eyebrow+title header. Apply every rule in `references/design-conventions.md` (the design choices Shaw converged on: header rules, no footers, color-on-icons-not-text, the Case study / Example tags, the warning-yellow Foundation bar, the slop bans).

Write all copy in **ABA voice** (read the `aba-brand-system` voice section): sentence case, no em dashes, no AI-hype words, no exclamation points, concrete over abstract, "put AI to work" / "hand off this workflow" phrasing.

## Step 5 — Visual QA (mandatory)

Render to images and inspect with **fresh-eyes subagents** as the pptx skill requires — you wrote the code and will see what you expect, not what's there. Check first for text overflow inside cards and boxes (the most common defect), then overlaps, alignment, and edge margins. Fix real issues, re-render, and stop after one clean pass. Don't chase sub-pixel nudges.

## Step 6 — Save and present

Save the `.pptx` to the client's working folder and present it. Keep the closing note short: what changed and the one or two open items (e.g. case studies still needing sign-off, pricing kept in the commercial layer). Do not recap every slide — Shaw can open the deck.

---

## Reference files

- `references/structure-patterns.md` — per-slide layouts and copy patterns for the default three slides and common extensions.
- `references/impact-slide-patterns.md` — turning research into the impact slide: audience segmentation, Case study vs Example tagging, before→after framing, attribution rules.
- `references/design-conventions.md` — the concrete design system for these decks (header rules, palette use, icon/tag treatment, the bans). Read alongside `aba-brand-system`.
- `scripts/deck_scaffold.js` — pptxgenjs starter with the ABA palette, helpers, and header function. Copy and fill in the slide bodies.
