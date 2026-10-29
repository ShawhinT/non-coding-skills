---
name: campaign-retrospective
description: Run a retrospective on any ABA campaign or initiative after it wraps — events, webinars, launches, cohorts, content pushes, outreach campaigns, sponsorships, partnerships. Use whenever Shaw says "let's do a retrospective", "retro", "post-mortem", "how did X go", "what did we learn from", "break down the numbers", "was it worth it", or shares a results export after a campaign. Also fires when he links a Notion retro page, drops a Luma/Kit/LinkedIn/Zoom export following a campaign, or asks why something underperformed. Pulls goal vs actual from the Notion campaign hub, reconciles actuals against each channel's source of truth, separates organic conversions from chased ones, diagnoses the binding constraint, and drafts the retro in chat for approval before writing anything to Notion. Do NOT use for pre-launch planning (business-strategy), live campaign syncs (crm / outreach), or single-channel analytics pulls (linkedin-post-analytics).
---

# Campaign Retrospective

A retrospective is not a report card. Its only job is to name **the one thing to change next
time** — and to be right about it. A retro that lists twelve improvements has failed, because
Shaw will do none of them.

The failure mode this skill exists to prevent: producing a confident, well-formatted analysis
that points at the wrong constraint. That is worse than no retro, because it sends real effort
at a non-problem. Most of what follows is about earning the diagnosis before stating it.

---

## Workflow

### 1. Frame the game before looking at any numbers

Read the campaign hub page and its plan page in Notion (Campaigns → the campaign's page; use
`notion-helper` for database mechanics). Extract, before you see results:

- The **goal** — usually a revenue or contract number, not a traffic number
- The **primary metric** and the **funnel model** with its assumed conversion benchmarks
- What was actually shipped (the promo calendar) vs what was planned

Knowing the intended model first is what lets you spot which stage broke. If you read the
actuals first, you will anchor on whatever number is most dramatic.

### 2. Reconcile actuals against each channel's source of truth

Do not trust the numbers written on the campaign hub. They are often a snapshot taken
mid-campaign and never updated. Pull the raw export and recompute.

`references/data-sources.md` covers where the truth lives per channel and the specific gotchas
in each export format. **Read it before parsing any export.** The Luma section in particular
documents semantics that are easy to get backwards and that have already produced one wrong
conclusion in a real retro.

When the recomputed number disagrees with the tracker, say so explicitly and go with the raw
source. Note the discrepancy in the retro — a tracker that drifts is itself a finding.

### 3. Build the funnel table: goal vs actual, every stage

Lay every stage side by side with its target. This is the spine of the retro and usually makes
the break obvious.

The reading that matters: **a stage can beat its benchmark while the goal metric is zero.** When
that happens, the beaten benchmark is almost always a measurement artifact, not a win. Treat any
over-performing stage sitting upstream of a zero as suspect and go audit how it was counted
before you praise it.

### 4. Split organic from assisted at every stage

This is the highest-value move in the whole skill and the one most easily skipped.

For each conversion stage, ask: **how many of these happened on their own, and how many happened
because Shaw chased them?** A stage metric that silently includes follow-up effort tells you
nothing about whether the mechanism works.

Worked example — the July 2026 exec webinar reported 9 discovery calls against a target of 4,
which read as 225% of benchmark and a clear success. Only **1** was organic; the other 8 came
from post-event outreach. The CTA's real conversion was under 1%. The entire "success" at that
stage was manufactured by hand, and the initial diagnosis was wrong until this split was made.

If the data doesn't record it, ask Shaw. He remembers which ones he had to work for.

### 5. Attribute by channel — volume and quality are different columns

Always render both: registrations (or leads) **and** the downstream rate. Ranking channels by
volume alone reliably produces the wrong recommendation, because the biggest channel is often
the worst-fit audience.

Ask what each channel's traffic *intends*. A course waitlist is full of people who want to learn
to do it themselves; that is a different human from someone who wants to hire. A channel can be
your largest source and your least likely buyer at the same time — and if you only see the
volume column, you will recommend scaling it.

### 6. Diagnose — find the binding constraint

Work down the funnel to the first stage that actually failed against the goal, and stop there.
Everything downstream of a broken stage is unmeasurable; everything upstream is not the problem
no matter how much it under- or over-performed.

Two tests that keep the diagnosis honest:

**The revenue-history test.** List where every paying client actually came from. If the campaign's
channels don't appear on that list, the campaign is unproven as a revenue channel regardless of
its top-line numbers — and the honest conclusion may be that it serves a different function
(awareness, pain detection, partner sourcing) than the one it was measured against. Say that
plainly rather than grading it against a goal it was never structurally able to hit.

**The friction-direction test.** Check whether the offer's commitment level runs *with* or
*against* the ICP. A free, low-commitment ask selects for people with spare time. If the ICP is
busy, low friction filters *for* non-buyers — the filter runs backwards. High-volume, low-quality
response is the signature.

Then resist the pull to recommend fixes for stages that weren't binding. If show rate missed but
the room was already big enough, show rate is not the problem, and saying so is more useful than
adding it to a list.

### 7. Draft in chat, write only on approval

Present the analysis and the proposed doc in the conversation first. Shaw corrects the read
before it becomes a page — he has context on the individual people and calls that no export
contains, and he has caught real errors this way.

**State the data semantics you relied on.** Not "here are the numbers" but "I'm treating
`approval_status = approved` as registered and blank UTM on the blast date as a blast
conversion." Shaw can only check the reasoning if he can see it. This exists because a retro was
once published claiming a channel produced zero registrations when it had produced 26 — the
error was in how one column was read, and it was invisible until the assumption was stated out
loud.

When he approves, write to the Notion retro page (`replace_content` for a full rewrite; see
`notion-helper` for connector quirks).

---

## Document structure

Match Shaw's density: terse bullets, keywords over sentences. He is the audience and he already
has the context — anything explanatory is a rewrite he has to trim. Depth belongs in chat, where
he can pull what he wants into the page himself.

```
<one-line framing: what this campaign was testing>

## Funnel
<table: Stage | Goal | Actual | verdict>
- <the caveat that makes the table honest — e.g. organic vs chased split>
- <who the conversions actually were>

## Channels
<table: Channel | Volume | % mix | Quality rate>
**Reading the export**: <the data semantics relied on, so it's auditable later>

## Diagnosis
- <the binding constraint, stated in one line>
- <revenue-history comparison>
- <what the campaign actually is, if it isn't what it was measured as>
- <open question the next run should answer>

## What worked
## What didn't
## Next time
- <ordered by leverage; the lead domino first>
- ⚠️ <open decisions, flagged not resolved>

## Open threads
- <named people, dated commitments>
```

Sections stay even when thin — an empty "what worked" is itself a finding. Drop the tables when
the campaign has no funnel (a content push, a partnership) and keep the rest.

---

## Standing conclusions

Findings that have already survived a retro. Treat these as priors, not re-openable questions —
a new retro should either build on them or produce evidence that overturns them. Add to this
list when a retro establishes something durable.

- **One sharp CTA, one door.** A confused mind doesn't buy. Multiple parallel CTAs split a mixed
  room rather than sorting it. *(July 2026 exec webinar)*
- **Price belongs in the CTA, not on the call.** When money isn't in the ask, the call defaults
  to a peer conversation and price has to be introduced against a frame already set. 2 of 9 calls
  reached a quote without it. *(July 2026)*
- **Warmth is not the qualifier — active pain is.** The clients who closed weren't the warmest
  contacts; they were the ones with an immediate, live problem. One closed off a near-cold
  LinkedIn reply because he was publicly asking for exactly that help. Screen for urgency and
  timing, not just firmographics. *([Company], July 2026)*
- **Events are pain-detection channels, not sales channels.** Every ABA client to date came from
  a 1:1 surface — warm outreach, inbound, LinkedIn outreach, referral. Measure an event by the
  qualified 1:1 conversations it surfaces, not by contracts closed from the room. *(July 2026)*
- **Qualify at registration.** Email-only signup leaves the post-event chase undifferentiated,
  which produces peer chats. Screening questions turn the same effort into a targeted list.
  *(July 2026)*

---

## Composing with other skills

- `notion-helper` — database catalog and connector quirks; load before any Notion write
- `business-strategy` — when the retro turns into a strategy conversation about what to do next,
  which it usually should. The retro establishes what happened; that skill decides what's next
- `outreach` — for retros on DM campaigns, where the tracker is the primary data source
- `crm` — to reconcile which calls and deals actually came from the campaign
- `skimmable-summary` — only when Shaw asks for the retro *as a digest*; the retro doc itself
  follows the structure above
