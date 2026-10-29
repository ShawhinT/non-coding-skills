---
name: "engagements"
description: "Use this skill whenever Shaw mentions creating, updating, querying, or wrapping a paid client engagement. Triggers include: \"create an engagement for X\", \"X just paid the invoice\", \"log the engagement\", \"what's the engagement ID for Y\", \"wrap up [Client Name]'s intensive\", \"mark X as delivered\", \"X's session moved\", \"fill in Stripe data for E###\", \"update engagement status\", \"look up the engagement for X\", \"did X pay yet\". Also fires for auditing/syncing the ledger: \"audit/sync the engagements\", \"is the engagement data up to date\", \"reconcile E###\", or the daily scheduled sync. Also fires when a CRM workflow signals \"deal closed\" (kickoff for a new row), or when a new ABA Trainings/Calls page needs linking to an existing engagement. This skill governs the Engagements database in ABA (Master) — the project ledger that tracks one row per won, invoiced project. The CRM (Nurture) database tracks the relationship; this database tracks the work.\n"
---

# Engagements Skill

The Engagements database is Shaw's project ledger. One row = one won, invoiced project. [Client Name]'s
1:1 Workshop and his 30-Day Intensive are two separate rows. Re-ups become new rows. Past and
active engagements live here together.

This skill governs how to read, create, update, and wrap engagement rows — and how the
Engagements DB relates to the CRM (Clients (Nurture)) database, ABA Calls, and ABA Trainings.

---

## Key Locations

| Resource | Location |
|---|---|
| Engagements database (page) | `https://www.notion.so/[database-id]` |
| Engagements data source | `collection://[page-id]` |
| Parent page (ABA Master) | Notion page ID: `[page-id]` |
| Clients (Nurture) data source | `collection://[page-id]` |
| ABA Calls data source | `collection://[page-id]` |
| ABA Trainings data source | `collection://[page-id]` |

For CRM (Nurture, Active Leads), see `crm/SKILL.md`. For ABA tasks/events, see `notion-helper/SKILL.md`.

---

## Engagements Database Schema

| Field | Type | Notes |
|---|---|---|
| Engagement ID | Title | Format `E### - <Name>` — 3-digit zero-padded number, then the client name (e.g., `E007 - [Company]`, `E005 - [Client Name]`). Use the organization name when the engagement has a Company, the person's name for solo individuals. Pull the name from the Company relation (falling back to Client), never a search result. NOTE: the property is named "Engagement ID" not "ID" — Notion reserves "id" as a system field name and rejects it. |
| Client | Relation → Clients (Nurture) | The **key decision makers and economic buyers** on this engagement — whoever approved or paid for it. Usually one or two people, always at least one (a solo client is their own buyer). Not attendees, and not everyone at the company with a Nurture row — the link is what puts the engagement on each person's CRM page, so it should mark the people the deal actually ran through. They are the decision-making subset of Context → Champions. The synced backlink on the Nurture page is named "Engagements". |
| Company | Relation → Companies | The account the engagement belongs to. Blank for a solo client with no company. Drives the company page's Revenue and Last Engagement rollups, so an engagement left unlinked is missing from the account's lifetime value. |
| Offer | Multi-select | **Read the current options from the data source schema** — don't work from a list written down in this skill; they drift. Roughly: solo workshop, team/group workshops, 30-Day Intensive, Custom AI Training, AI Advisory, Ad Hoc Consulting. See `references/offer-scopes.md` for deliverable shapes. |
| Source | Multi-select | `LinkedIn`, `YouTube`, `Personal`, `ABB`, `ABA Contact`, `Homepage Contact`, `ABA Discovery Call`, `Referral`. Mirrors CRM Source options. |
| Status | Select | `Sold`, `Active`, `Delivered`, `Refunded`, `On Hold`. See Lifecycle below. |
| Start Date | Date | Date of first scheduled session (or kickoff date if no sessions yet). |
| End Date | Date | Date of last session, or projected end. Open for ongoing advisory. |
| Price | Number ($) | Contract value. Leave blank if unknown — never guess. |
| Paid Status | Select | `Unpaid`, `Partial`, `Paid in Full`, `Refunded`. Reflects payment status, not invoice state. |

---

## Naming Convention

Engagement titles are `E### - <Name>`: a 3-digit zero-padded number assigned in **temporal order by Start Date**, followed by the client name. Use the **organization name** when the engagement has a `Company` (e.g., `E007 - [Company]`, `E004 - [Company]`) and the **person's name** when it doesn't (e.g., `E005 - [Client Name]`). Pull the name from the Company relation, falling back to the Client relation, never from a search result. The fixed-width `E###` prefix keeps an ID-ascending sort chronological regardless of the suffix.

**Getting the next ID for a brand-new engagement (Start Date = today or future):**
1. Query the Engagements DB sorted by Engagement ID descending
2. Parse the `E###` numeric prefix of the highest existing ID and increment by 1
3. Format as `E### - <Name>` (e.g., `E023` → `E024 - <Name>`)

**Inserting an older engagement (backfill):**
If the new engagement has a Start Date that falls before existing rows, you have two options:
- **Renumber** all later rows to maintain temporal order (clean, but requires updating every later row's title)
- **Append at the end** with the next available ID, even though it's out of temporal order (simpler, accept that ID order ≠ temporal order until cleanup)

Default to renumber if the inserted engagement is recent enough that few rows need updating (≤5).
Append if the insert is deep in the past and would require updating many rows. Always confirm with
Shaw before bulk renumbering.

**Why temporal:** Sorting the DB by Engagement ID ascending gives a chronological revenue ledger
without needing a separate sort.

---

## Lifecycle

```
Sold → Active → Delivered
         ↓
      Refunded
         ↓
       On Hold
```

| Status | Meaning | Trigger to flip into this |
|---|---|---|
| **Sold** | Invoice paid (or signed proposal in hand), but delivery hasn't started yet. | Invoice paid in Stripe (or other payment confirmed). Sessions not yet held. |
| **Active** | Delivery in progress. At least one session has happened. | First session occurs. |
| **Delivered** | All sessions complete. The work is done. Wrap-up (testimonial, referrals, re-up) lives in CRM Nurture from here forward. | Last scheduled session occurs. |
| **Refunded** | Engagement cancelled, money returned (full or partial). | Refund issued. |
| **On Hold** | Delivery paused, not killed. Client went dark, hit a blocker, or both waiting on something. Different from Active because nothing is moving and no near-term session is booked. | 30+ days of stalled progress with no booked next step. |

**Delivered → CRM handoff:** Once an engagement flips to Delivered, the engagement row stops
being the active workspace. All wrap-up activity (testimonial chasing, referral asks, re-up
conversations) tracks in the Clients (Nurture) page going forward. The engagement row stays
as a permanent record for revenue/case-study purposes, but its 4Rs body section gets filled in
once and not actively maintained. If the client re-ups before wrap-up is done, the wrap-up items
(testimonial ask, 4Rs) roll forward to the newest engagement; the older row staying at TBD is
not a gap. The handoff is engagement-level, not account-level: the client's CRM row only flips to
`Nurturing` (with a ~3-month `Next Contact`) when this was their *last* open engagement. If other
engagements are still `Sold`/`Active`, the account stays `Active` and `Next Contact` points to the
next real touchpoint — see Workflow 2 step 4.

---

## Body Template

Every engagement page body has these sections, in this order:

```markdown
## Context
- **Offer:** <offer name> — one clause on what it is
- **Term:** <start> – <end> (<duration>)
- **Investment:** $<total> — how it breaks down, and any discount off list
- **Champions:** <name> (<role>) · <name> (<role> — approves spend, invoice payer) · ...
- **Attendees:** <name> (<function>) · ... — group engagements only; omit on solo
- **Closed:** proposal sent M/D, closed on the M/D <call type>
<one line on where this sits strategically — offer-stack position, what it's graded on>

**Notes**
- M/D — short, date-stamped, append-only. Same style as CRM notes.

---

**Stripe link:** [in_xxxxx](https://dashboard.stripe.com/invoices/in_xxxxx) — Paid in full M/D ($X). Billed to <email>.

## Engagement Goal
<only when the offer is sold against outcomes — see Section rules>

## Program Scope
**Deliverables:**
- <bullet per deliverable, with count × duration when relevant>

**Bonus:** <if any; omit the line entirely if none>

**Guarantee:** <if any, with specifics on what triggers it; omit if none>

## Deliverable Tracker
<only for multi-deliverable engagements — see "Deliverable Tracker" below>

<columns>
	<column>
		## Calls
		- <mention-page url="..."/> (M/D — discovery / check-in / etc.)
	</column>
	<column>
		## Sessions
		- <mention-page url="..."/> (M/D — name)
	</column>
</columns>

## Metrics
<only for metric-graded engagements — see "Metrics" below>

## Ideas & Parking Lot
<ideas and open threads that surface mid-engagement; omit on short engagements>

---

## 4Rs

### Results

_TBD at wrap_

### Re-up

_TBD at wrap_

### Reviews & Referrals

_TBD at wrap_
```

**Section rules:**
- **Context leads, and it absorbs the notes log.** The dated log is a `**Notes**` block *inside* Context, not its own H2 at the bottom — the story of how a deal closed and why it's structured the way it is belongs where a reader lands first. Append new entries under that `**Notes**` label; don't create a `## Notes` section.
- **Context facts are bullets**, one per line (`- **Term:** ...`), not loose bold lines.
- **Champions and Attendees are different lists.** Champions are who bought and who to talk to; Attendees are who sits in the sessions. On a solo engagement they collapse into one line — omit Attendees. On a group or team workshop they diverge (a payer who never attends, five participants who never see an invoice), and the roster is load-bearing for the testimonial asks and the Sessions list, so it earns its own bullet.
- **The engagement's notes stay on the engagement.** Don't relocate them to the CRM: the CRM `Notes` property is the *account* timeline, while these are *project* facts — why billing was structured this way, what went out when. Someone opening the row months later shouldn't have to read the account history to answer "why three invoices?"
- **Two dividers.** One closes Context; one sits above `## 4Rs`, separating the live engagement from wrap-up material that gets filled once at the end.
- **Calls before Sessions, side by side** in a two-column block. Calls first because the sales thread is what explains the engagement; Sessions fills in as delivery happens. Both keep their `## ` headings so append targets are unchanged.
- **Program Scope** captures what was promised **at sale** — not what's actually being delivered. Pull defaults from `references/offer-scopes.md`. If a deal diverges from the canonical scope, write what Shaw confirms was sold.
- **Stripe link** stays one line, directly under the Context divider. If no Stripe invoice exists (paid via vendor portal, Venmo, etc.), italicize a one-line note explaining how it was paid. For installments, use the Payment Schedule table below instead.
- **Sessions** lists ABA Trainings mention-pages chronologically with `(M/D — name)` annotation
- **Calls** lists ABA Calls mention-pages chronologically with `(M/D — type)` annotation
- **Notes** mirrors CRM notes style: short, date-stamped, append-only
- **4Rs** runs as three sub-headings — Results, Re-up, and a merged **Reviews & Referrals**,
  since one Reviews/Referrals row carries both lifecycles per person and separate sections would
  link the same records twice; fill in during wrap, then leave alone. **Reviews & Referrals** is
  the exception to the prose style — it links the Reviews/Referrals DB record(s) (one mention-page per attendee), never restated status text, because that record holds the live status. The one prose element is landed referrals — engagement-level
  outcomes ("referred X → became E00Y") recorded at wrap, since an outcome is not any single
  person's status.

### Engagement Goal (outcome-sold engagements only)

Most offers are sold as a number of sessions, and "delivered" means the sessions happened. Some —
retainers especially — are sold against an *outcome*: adoption hitting a threshold, every seat
activated. When that's the deal, the goal and its measurement method go in the body near the top,
because session count stops being a meaningful progress signal and the Metrics section takes over.
Lift the targets and the definitions verbatim from the proposal; a target the client didn't agree to
isn't a target.

Skip this section entirely on session-count offers — a 1:1 workshop doesn't have one.

### Deliverable Tracker

For engagements with many deliverables across parallel tracks, a tracker near the scope gives an
at-a-glance count. Put the recurring tracks in a `<columns>` block, one column each, so they read
side by side rather than as three long stacked lists:

```markdown
## Deliverable Tracker
<columns>
	<column>
		### <Track A> — 0 / 13
		*<cadence / how each is chosen>*
		*None yet.*
	</column>
	<column>
		### <Track B> — 0 / 13
		*<cadence>*
		*None yet.*
	</column>
	<column>
		### <Track C> — 0 / 3
		- [ ] <unit 1> —
		- [ ] <unit 2> —
	</column>
</columns>

### Standing / One-Time
- [ ] <one-time deliverable>
```

**Don't pre-list checkboxes for work that gets its own Notion page.** Each training and each call
earns an ABA Trainings page, so the tracker takes a `<mention-page>` line as each one happens and
the count comes from the links. A pre-listed row of 13 empty checkboxes is a second copy of a fact
that already lives in the session page — it goes stale, and ticking a box adds nothing the link
doesn't say better.

Checkboxes are right for deliverables with **no page of their own**: infra builds, "Slack channel
set up", "skill library delivered". Those go in the third column and in `### Standing / One-Time`.

### Metrics (metric-graded engagements only)

When an engagement is graded on numbers, the record needs somewhere to hold them over time.
Targets and definitions sit above as static text — they don't change week to week, so putting them
in the database would repeat them in every row. Below them, an **inline database**, one per
engagement record, where each row is a dated reading:

| Property | Type | Notes |
|---|---|---|
| **Date** | Title | ISO date of the reading (`2026-08-11`). ISO sorts chronologically as text, so no separate date property is needed. |
| `<metric> (%)` | Number | one column per metric |
| `<count>` | Number | absolute counts where the goal is a count (seats activated, total seats) |
| Notes | Text | one line — what moved, what's stuck |

**Percentages are plain numbers with `%` in the column name, not Notion's percent format.** Percent
format stores decimals and renders them ×100, so a `65` typed off a dashboard displays as 6500%.
Plain numbers mean what you type is what you get.

Add the baseline row in week 1, then a row at each recurring review call — the cadence the proposal
already commits to is the natural trigger.

The tradeoff to know: an inline database per record can't roll up across engagements. That's the
right default (self-contained records, and it matches how Shaw tracks experiments), but if the
question ever becomes "adoption curves across all retainer clients," that wants one shared Metrics
database with an Engagement relation instead.

### Installment engagements (one row, several invoices)

When the contract is billed in installments, the single `**Stripe link:**` line can't carry them.
Replace it with a lead-in plus a schedule table, so the row shows at a glance what's been collected
and what's still coming:

```markdown
**Stripe:** billed as **3 monthly invoices of $6,000**, not one — `Price` above is the $18,000
contract value, so no single invoice matches it. Billed to <name> (<email>, `cus_...`).

### Payment Schedule

| # | Amount | Due | Invoice | Sends | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | $6,000 | Mon 8/10 | [in_xxxxx](https://dashboard.stripe.com/invoices/in_xxxxx) | sent 7/29 | Open — [pay](<hosted_invoice_url>) |
| 2 | $6,000 | Thu 9/10 | [in_yyyyy](https://dashboard.stripe.com/invoices/in_yyyyy) | auto Thu 9/3 | Draft |
| 3 | $6,000 | Sat 10/10 | [in_zzzzz](https://dashboard.stripe.com/invoices/in_zzzzz) | auto Fri 10/2 | Draft |
```

Note the send dates explicitly — later invoices typically carry `automatically_finalizes_at`, so
they email themselves without anyone acting, and a reader should be able to see that from the row.
`stripe-helper` owns the mechanics.

Once saved, Notion converts that markdown table into a `<table>`/`<td>` block, so any later edit to
a cell has to target the XML form, not the pipes you wrote. See `notion-helper` → Connector quirks.

---

## Engagements vs CRM Boundary

This is the load-bearing rule that determines what goes where.

| Concern | Lives in |
|---|---|
| The relationship with a person (long-term) | **Clients (Nurture)** |
| The project / paid work (one per invoice) | **Engagements** |
| Active sales pipeline (pre-payment) | **Active Leads** |
| Sales call notes | **ABA Calls** (linked from CRM page AND engagement body) |
| Delivery session notes | **ABA Trainings** (linked from CRM page AND engagement body) |
| Wrap-up tracking (testimonial chasing, referral asks, re-up conversations) | **Clients (Nurture)** Notes — NOT engagement body |

**The flow:**
1. Lead enters CRM (Active Leads) at first contact
2. Lead closes → moves to Clients (Nurture), Engagement row created (Status=Sold)
3. Engagement runs through Sold → Active → Delivered
4. Once Delivered, engagement row is archive material; Clients (Nurture) takes over for nurture/expansion

**Why this matters:**
- One client can have many engagements ([Client Name] = Workshop + Intensive). Two rows in Engagements,
  one row in Nurture. Don't conflate.
- Wrap-up (4Rs) gets filled in once when the engagement flips to Delivered. After that, all
  ongoing nurture activity goes in the Nurture row's Notes — not back into the engagement.

---

## Workflows

| Workflow | Trigger | File |
|---|---|---|
| 1. Create Engagement | A deal closes; "create engagement for X"; "X paid the invoice" | `workflows/workflow-1-create.md` |
| 2. Status Transitions | First session held; last session held; refund issued; engagement stalled | `workflows/workflow-2-status.md` |
| 3. Link Session/Call to Engagement | New ABA Trainings or ABA Calls page created for an active client | `workflows/workflow-3-link-session.md` |
| 4. Stripe Fill | "Look up Stripe for X"; filling in Price + Stripe link on existing row | `workflows/workflow-4-stripe-fill.md` |
| 5. Daily Sync / Audit | scheduled daily; "audit the engagements", "sync the engagements", "is the engagement data up to date", "reconcile E###" | `workflows/workflow-5-sync.md` |

---

## References

| Reference | Contents | File |
|---|---|---|
| Pricing Principles | Where price comes from + judgment rules that outlive a price change | `references/pricing-principles.md` |
| Offer Scopes | Canonical deliverable shapes per offer (deliverables, bonuses, guarantees) | `references/offer-scopes.md` |
| Reconciliation Checks | Canonical catalog of sync checks with auto/surface tiers, sources of truth, fixes, and traps | `references/reconciliation-checks.md` |

---

## Key Principles

- **One project = one row.** Re-ups, multi-attendee team workshops billed together, and follow-on
  engagements all become new rows. Never collapse separate *work* into one engagement.
  - The axis is the **work, not the payments.** A single contract split into installments
    ($6,000/month × 3 for one $18,000 engagement) stays **one row**: `Price` holds the contract
    value, and `Paid Status` walks `Unpaid` → `Partial` → `Partial` → `Paid in Full` as each
    invoice clears. Splitting installments into E013/E014/E015 breaks more than it fixes — one
    deliverable set can't be divided three ways, revenue counts would show three sales where
    there was one, and the 4Rs would get filled in three times. See "Installment engagements"
    under Body Template.
- **Title is `Engagement ID`, not `ID`.** Notion reserves "id" as a system field name. Don't try
  to rename back.
- **Leave Price/Paid Status blank if unsure.** Better to flag for Shaw than guess. The Stripe
  workflow can fill these in later.
- **Don't cache offer names or prices in this skill.** Offers change often — new SKUs appear
  mid-conversation, formats get shortened, prices move. Read names from the `Offer` multi-select
  schema and prices from the agreement or live Stripe. A number written here reads as
  authoritative long after it stops being true.
- **Check for proxy-email payers before declaring "no invoice found."** Some clients pay via
  vendor portals ([Company], [Company], [Company]) where the billing email differs from the
  client's contact email. The actual payer may be a procurement contact at the company. Search
  by company domain or company name before giving up. See `workflows/workflow-4-stripe-fill.md`.
- **Voided + replaced invoices are common.** Don't assume a voided invoice means no payment —
  the same amount may have been collected via a different invoice or a different Stripe account
  (e.g., the client's own vendor portal billed Shaw separately).
- **Engagement ID order = temporal order.** When adding a new engagement, query existing IDs and
  increment. When backfilling something old, decide whether to renumber or append (see Naming
  Convention).
- **Don't track wrap-up here once Delivered.** Testimonial chasing, referral asks, and re-up
  conversations belong in the Clients (Nurture) Notes field. The engagement's 4Rs section gets
  filled in once at wrap and not maintained.
- **Always read before writing.** Fetch the engagement page before any update — body sections
  use exact-string match for content updates, and notes are append-only.
- **The calendar is what's booked; the Notion DBs are its record.** ABA Trainings and ABA Calls
  contain a session only once someone creates the page, so treating them as the delivery calendar
  means reading a record that lags reality — a session booked this morning is invisible to every
  check that reads only those tables. The sync closes that gap by reading the booking feed
  directly (`workflow-5-sync.md` → "The booking feed"). Detection lives here; *execution* belongs
  to `calendar-helper`, which already owns the event-type SOP Setup.
- **Sessions and Calls in body are mention-pages, not properties.** The relation to Clients
  (Nurture) is the only relation property. ABA Trainings and ABA Calls links live in body
  sections so the narrative ordering is preserved.
- **Scope reflects what was sold, not what was delivered.** The `## Program Scope` section
  captures the promise at sale. If actual delivery diverges materially (different sessions,
  different format, different deliverables, materially different price), that's almost always a
  new engagement — split into a second row rather than editing the original scope. Record the
  re-up in the prior engagement's Notes. The split rule governs *delivery* diverging from the
  sale; when the sale itself was mis-recorded and corrected before delivery (a scoping
  misunderstanding surfaces, the invoice gets voided and replaced), update the row in place —
  same project, one row — and log the correction plus the voided/replacement invoice in Notes.
  The row reflects the actual agreement; only real follow-on work earns a new row.
