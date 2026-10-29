# Workflow 1: Create a New Engagement

**Triggers:**
- "Create an engagement for X"
- "X just paid the invoice" / "X closed"
- A CRM workflow flips an Active Lead's Status to `Closed`
- Shaw confirms a deal is signed and ready to deliver

**Goal:** Add one row to the Engagements DB representing a single won, invoiced project. Set up
the body template so the engagement is ready to receive sessions, calls, and notes as delivery
progresses.

---

## Steps

### 1. Confirm the client exists in Clients (Nurture)

Search Clients (Nurture) by name and email. If no match:
- The client may still be in Active Leads. Run the CRM skill's **Workflow 5 (Move Lead to
  Clients)** first, then come back here.
- Don't create an engagement without a Nurture row to link to — the Client relation property
  is required, and it points at the deal's decision makers and economic buyers, not at
  colleagues who attend.

Get the Nurture page URL of the buyer, plus any other decision maker who approved this deal
and has a Nurture row — you'll need them as a JSON array for the `Client` property:
`["https://www.notion.so/<page-id>", ...]`

### 1.5 Confirm the company exists in Companies

Read the `Company` relation on the buyer's Nurture row. If it's set, reuse that page URL as
the engagement's `Company` (JSON array, same shape as `Client`). If it's blank and the buyer
represents a company, the Companies row is missing: create it (Name, Domain, Website,
Relationship `Client`, a two-bullet `## Context`) and link it on both the Nurture row and the
engagement. If the buyer is a solo client, leave `Company` blank. Either way, a company that
now has a paid engagement carries Relationship `Client` — flip it if it still says `Prospect`.

### 2. Determine the next Engagement ID

Query the Engagements data source sorted by Engagement ID descending, take the top row's
`E###` numeric prefix, increment by 1, and format the title as `E### - <Name>` — the name being
the client's organization from the Company relation confirmed in Step 1.5 (or the person's name
for a solo individual with no company).

```
view URL: https://www.notion.so/[page-id]?v=<view-id>
```

If this is a backfill of an older engagement (Start Date significantly before existing rows),
ask Shaw whether to renumber siblings or append at the end. Default: append unless the insert
point is recent (≤5 rows would need renumbering).

### 3. Determine the offer + price

Identify the offer from Shaw's description or the lead's most recent ABA Calls notes, then match
it to a **current** option — fetch the Engagements data source and read the `Offer` multi-select
schema rather than working from a list. The options drift, and a hardcoded list silently goes
stale (it once named the team offer `— Team` while every real row said `(Group)`).

Price comes from the agreement — the email thread or call where the number was named — not from a
default table. See `references/pricing-principles.md`. If the deal doesn't map cleanly to an
existing option or the price is unclear, leave `Price` blank and flag it rather than guessing.

### 4. Determine Source

Mirror the Source from the client's Active Leads or Nurture row (whichever has it set).
Common sources: `LinkedIn`, `YouTube`, `Personal`, `ABB`, `ABA Contact`, `Homepage Contact`,
`ABA Discovery Call`, `Referral`.

### 5. Set Status + dates

- **Status:** `Sold` if no sessions held yet; `Active` if at least one session has happened.
- **Start Date:** Date of first scheduled session, or kickoff date if no sessions yet.
- **End Date:** Projected last session date if known; leave blank if not.

### 6. Create the page

Use `notion-create-pages` with parent `data_source_id: [page-id]`.

**Property keys (use these exact names):**
- `Engagement ID` (NOT `ID` — Notion rejects it). Value is `E### - <Name>`, e.g. `E009 - [Company]`.
- `Client` (JSON array of page URLs: `"[\"https://www.notion.so/<id>\"]"`) — the decision makers' / buyer's Nurture rows
- `Company` (JSON array with the Companies page URL; omit for a solo client)
- `Offer` (JSON array: `"[\"30-Day Claude Intensive\"]"`)
- `Source` (JSON array: `"[\"LinkedIn\"]"`)
- `Status` (string: `"Sold"`)
- `date:Start Date:start` (ISO date: `"2026-04-25"`)
- `date:End Date:start` (ISO date or omit)
- `Price` (number, no quotes: `6000`)
- `Paid Status` (string: `"Paid in Full"` / `"Unpaid"` / `"Partial"`)

**Body content (use this template):**

```markdown
**Stripe link:** _paste invoice URL_

## Program Scope

**Deliverables:**
- _one bullet per deliverable — start from the canonical list in `references/offer-scopes.md`_

**Bonus:** _if any; omit the line if none_

**Guarantee:** _if any; omit the line if none_

## Sessions

_None yet — add as ABA Trainings pages get created._

## Calls

- <mention-page url="<discovery-call-page-url>"/> (M/D — discovery)

## Notes

- Closed (M/D). [One-line context if useful.]

## 4Rs

### Results

_TBD at wrap_

### Re-up

_TBD at wrap_

### Referrals

_TBD at wrap_

### Reviews

_TBD at wrap_
```

Replace `_paste invoice URL_` with the real Stripe link if available (run **Workflow 4** in the
same pass to fill it in).

**Program Scope is filled at creation, never left for later — and it starts from the canonical
shape.** Copy the deliverables for this offer from `references/offer-scopes.md`, then edit them to
match the deal. When a deal customizes the format (grouped sessions, different counts), edit the
canonical bullets rather than composing the list from scratch — that's how closing deliverables
survive the rewrite. In particular, keep the canonical closing deliverable (the wrap-up call on
team workshops, the Day-7 check-in on solo workshops) unless Shaw explicitly confirms it wasn't
sold; ask before dropping it. A scope missing its closing deliverable makes the daily sync
mis-time the `Active → Delivered` flip (E009: a custom grouped-session scope omitted the wrap-up
call, and the sync repeatedly flagged a status decision that was really a scope gap).

### 7. Open placeholder Reviews/Referrals rows

Every participant in the engagement gets a Reviews/Referrals row at creation time, not at
wrap. Placeholder rows opened now act as standing reminders so the ask never gets skipped
later.

For each participant (champion included only if they attend sessions): create a row with
`Review Status: Not Asked`, `Referral Status: Not Asked`, the `Engagement` relation set to
this new row, and `CRM` pointed at the champion's Clients (Nurture) page. Partial info is
fine — tag unknown names with the company (e.g. `[Person] ([Company])`) and leave Email blank,
then fill both in when the participant list arrives. Mechanics live in
`reviews-referrals/workflows/testimonial-ask.md` (§1).

### 8. Confirm with Shaw

Reply with the Engagement ID, link, and a one-line summary:

> Created [E009 - [Client Name]](url) — 1:1 Claude Workshop · Sold · $[amount] · Paid in Full.

This is also the moment to flag a **new offer shape**. If the deal is a format Shaw hasn't sold
before (a shorter session, a new bundle), say so — it likely needs a new Stripe SKU and a new
multi-select option, and both are better created deliberately than improvised at invoice time.

Flag any blanks (Price, Stripe link, projected End Date) so Shaw can fill them in.
