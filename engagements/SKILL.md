---
name: engagements
description: >
  Use this skill whenever Shaw mentions creating, updating, querying, or wrapping a paid client
  engagement. Triggers include: "create an engagement for X", "X just paid the invoice", "log
  the engagement", "what's the engagement ID for Y", "wrap up [Client]'s intensive", "mark X as
  delivered", "X's session moved", "fill in Stripe data for E####", "update engagement status",
  "look up the engagement for X", "did X pay yet". Also fires when a CRM workflow signals "deal
  closed" — that's the kickoff for a new engagement row. Also fires when a new ABA Trainings or
  ABA Calls page is created for an active client and needs to be linked to an existing engagement.
  This skill governs the Engagements database in ABA (Master) — the project ledger that tracks
  one row per won, invoiced project. The CRM (Nurture) database tracks the relationship; this
  database tracks the work.
---

# Engagements Skill

The Engagements database is Shaw's project ledger. One row = one won, invoiced project. A single
client's 1:1 Workshop and 30-Day Intensive are two separate rows. Re-ups become new rows. Past and
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
| Engagement ID | Title | Format `E####` (4-digit zero-padded). E.g., `E0001`, `E0023`. NOTE: the property is named "Engagement ID" not "ID" — Notion reserves "id" as a system field name and rejects it. |
| Client | Relation → Clients (Nurture) | Single client per engagement. The synced backlink on the Nurture page is named "Engagements". |
| Offer | Multi-select | `1:1 Claude Workshop`, `1:1 Claude Workshops — Team`, `30-Day Claude Intensive`, `Custom AI Training`, `AI Advisory`, `Ad Hoc Consulting`. See `references/offer-pricing.md` for default prices. |
| Source | Multi-select | `LinkedIn`, `YouTube`, `Personal`, `ABB`, `ABA Contact`, `Homepage Contact`, `ABA Discovery Call`, `Referral`. Mirrors CRM Source options. |
| Status | Select | `Sold`, `Active`, `Delivered`, `Refunded`, `On Hold`. See Lifecycle below. |
| Start Date | Date | Date of first scheduled session (or kickoff date if no sessions yet). |
| End Date | Date | Date of last session, or projected end. Open for ongoing advisory. |
| Price | Number ($) | Contract value. Leave blank if unknown — never guess. |
| Paid Status | Select | `Unpaid`, `Partial`, `Paid in Full`, `Refunded`. Reflects payment status, not invoice state. |

---

## Naming Convention

Engagement IDs are `E####` (4-digit zero-padded), assigned in **temporal order by Start Date**.

**Getting the next ID for a brand-new engagement (Start Date = today or future):**
1. Query the Engagements DB sorted by Engagement ID descending
2. Take the highest existing ID and increment by 1
3. Format as `E####` (e.g., `E0023` → `E0024`)

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
once and not actively maintained.

---

## Body Template

Every engagement page body has these sections, in this order:

```markdown
**Stripe link:** [in_xxxxx](https://dashboard.stripe.com/invoices/in_xxxxx) — Paid in full M/D ($X). Billed to <email>.

_Optional one-line context (e.g., team workshop attendee list, payer info)._

## Sessions

- <mention-page url="..."/> (M/D — name)
- <mention-page url="..."/> (M/D — name)

## Calls

- <mention-page url="..."/> (M/D — discovery / follow-up / etc.)

## Notes

- Short chronological log of what happened. Same style as CRM notes — date-stamped, comma-separated, no business context.

## 4Rs

### Results

_TBD at wrap_ — fill in concrete results during wrap-up (time saved, skills built, etc.)

### Re-up

_TBD at wrap_ — what happened next? New engagement, declined, or still considering?

### Referrals

_TBD at wrap_ — who got referred from this engagement?

### Reviews

_TBD at wrap_ — testimonial captured (yes/no/declined), with quote or page link
```

**Section rules:**
- **Stripe link** stays at top, one line. If no Stripe invoice exists (paid via vendor portal, Venmo, etc.), italicize a one-line note explaining how it was paid.
- **Sessions** lists ABA Trainings mention-pages chronologically with `(M/D — name)` annotation
- **Calls** lists ABA Calls mention-pages chronologically with `(M/D — type)` annotation
- **Notes** mirrors CRM notes style: short, date-stamped, append-only
- **4Rs** stays as four sub-headings; fill in during wrap, then leave alone

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
- One client can have many engagements (e.g., Workshop + Intensive). Two rows in Engagements,
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

---

## References

| Reference | Contents | File |
|---|---|---|
| Offer Pricing | Canonical offer names + default prices | `references/offer-pricing.md` |

---

## Key Principles

- **One invoice = one row.** Re-ups, multi-attendee team workshops billed together, and follow-on
  engagements all become new rows. Never collapse multiple invoices into one engagement.
- **Title is `Engagement ID`, not `ID`.** Notion reserves "id" as a system field name. Don't try
  to rename back.
- **Leave Price/Paid Status blank if unsure.** Better to flag for Shaw than guess. The Stripe
  workflow can fill these in later.
- **Check for proxy-email payers before declaring "no invoice found."** Some clients pay via
  vendor portals (some enterprise clients) where the billing email differs from the
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
- **Sessions and Calls in body are mention-pages, not properties.** The relation to Clients
  (Nurture) is the only relation property. ABA Trainings and ABA Calls links live in body
  sections so the narrative ordering is preserved.
