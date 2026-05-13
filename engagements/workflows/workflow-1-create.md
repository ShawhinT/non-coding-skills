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
  is required.

Get the Nurture page URL — you'll need it as a JSON array for the `Client` property:
`["https://www.notion.so/<page-id>"]`

### 2. Determine the next Engagement ID

Query the Engagements data source sorted by Engagement ID descending, take the top row's ID,
increment by 1, format as `E####`.

```
view URL: https://www.notion.so/[page-id]?v=<view-id>
```

If this is a backfill of an older engagement (Start Date significantly before existing rows),
ask Shaw whether to renumber siblings or append at the end. Default: append unless the insert
point is recent (≤5 rows would need renumbering).

### 3. Determine the offer + default price

Identify the offer from Shaw's description or the lead's most recent ABA Calls notes. Match to
one of the canonical options:

- `1:1 Claude Workshop`
- `1:1 Claude Workshops — Team` (multi-attendee, single payer)
- `30-Day Claude Intensive`
- `Custom AI Training`
- `AI Advisory`
- `Ad Hoc Consulting`

Pull the default price from `references/offer-pricing.md`. For team workshops, multiply
$1,500 × N attendees unless Shaw specifies a different bundle rate.

If you can't determine the offer or price confidently, leave Price blank and flag for Shaw to fill.

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
- `Engagement ID` (NOT `ID` — Notion rejects it)
- `Client` (JSON array of page URLs: `"[\"https://www.notion.so/<id>\"]"`)
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

### 7. Confirm with Shaw

Reply with the Engagement ID, link, and a one-line summary:

> Created [E0006](url) — [Client Name] · 1:1 Claude Workshop · Sold · $1,500 · Paid in Full.

Flag any blanks (Price, Stripe link, projected End Date) so Shaw can fill them in.
