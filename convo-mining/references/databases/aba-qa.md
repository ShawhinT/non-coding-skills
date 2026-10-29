# 🏷️ ABA Q&A

Every question or objection someone raised about ABA's own offer, and the answer Shaw gave. Split
out of 💬 Q&A and Pain Points on 10/11/26.

**Database:** `https://app.notion.com/p/[database-id]`
**Data source:** `collection://[page-id]`

## Schema

Same as 💬 Q&A — `Question` (title), `Asker` (the spine's `Person`), `Avatar` with Q&A's rules, and
the shared spine — plus one property:

| Property | Type | Note |
|---|---|---|
| Kind | Select | `Question` / `Objection` |

- `Question` — reaching for information about the offer
- `Objection` — a stated reason not to buy, or a challenge to price, value, or need. Same rule
  `pain-points.md` used for its retired `Objection` type: it presumes a live buying decision. A peer
  or friend on a free session has nothing to object to.

## Body template

```markdown
## Question            ← `## Objection` when Kind is Objection

> <verbatim words, blockquoted>

*<one italic line of provenance>*

## Answer

<Shaw's reply, verbatim — omit this heading entirely when he gave none>
```

An objection nobody answered is a complete row. Where Shaw did answer, the reply is the rebuttal —
the half you reach for when prepping a call.

## What belongs here

A question or objection about **what buying or working with ABA looks like**:

- scope, structure, format — group vs 1:1, session granularity, what an audit or activation stage
  covers, where an engagement starts, next steps
- process — how one-on-ones run, how Shaw picks use cases *for the engagement*, what support looks
  like, how he onboards a team
- proof — prior clients, results, ROI of the engagement
- fit and prerequisites — technical bar, who should attend, whether a team has the bandwidth
- price, budget, payment terms, risk of buying, "why not build it ourselves", "why you"
- referral-partner logistics — how a partner refers, the fee, the ideal client (Shaw's call, 10/11/26)
- an Upwork poster's asks about scope, prerequisites, or prior work — buyer questions answered in a
  proposal (Source `Upwork`; Shaw's call, 10/11/26)

The test: *would it sit on an FAQ page for buying or working with ABA?*

## What stays out

- **AI questions that drew a pitch.** Route on what the asker was reaching for. Shaw often answers
  an AI question with how his engagement handles it; the pitch doesn't move the row here.
- **His adoption methodology** — bottom-up vs top-down, champions vs managers, who should own AI,
  how to measure a process's ROI. That's Q&A, unless the question is specifically about how ABA's
  engagement executes it.
- **Anthropic's pricing** — Claude seats, plans, tokens. That's a tool question → Q&A.
- **Doubts about AI itself** — "my team won't adopt it." Pain Points.
- **Recitation of the strategy page.** "What does the fractional department cost?" answered by
  reading off the price list adds nothing the strategy page doesn't hold better. An objection to the
  price is a row; a lookup of the price isn't.

## What this database is for

- **Pre-call prep and sales-page FAQ** — what buyers actually ask and push back on, with Shaw's
  answers.
- **Offer design** — repeated scope and format questions say where the offer is unclear.
- **Objection handling** — filter `Kind = Objection` for the rebuttal library.
