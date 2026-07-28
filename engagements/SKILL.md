---
name: engagements
description: >
  Use this skill whenever Shaw mentions creating, updating, querying, or wrapping a paid client
  engagement. Triggers include: "create an engagement for X", "X just paid the invoice", "log
  the engagement", "what's the engagement ID for Y", "wrap up [Client Name]'s intensive", "mark X as
  delivered", "X's session moved", "fill in Stripe data for E###", "update engagement status",
  "look up the engagement for X", "did X pay yet". Also fires for auditing/syncing the ledger:
  "audit/sync the engagements", "is the engagement data up to date", "reconcile E###", or the
  daily scheduled sync. Also fires when a CRM workflow signals "deal closed" (kickoff for a new
  row), or when a new ABA Trainings/Calls page needs linking to an existing engagement.
  This skill governs the Engagements database in ABA (Master) — the project ledger that tracks
  one row per won, invoiced project. The CRM (Nurture) database tracks the relationship; this
  database tracks the work.
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
| Engagement ID | Title | Format `E### - <Name>` — 3-digit zero-padded number, then the client name (e.g., `E007 - [Company]`, `E005 - [Client Name]`). Use the organization name when the client is a company, the person's name for solo individuals. Pull the name from the Client relation, never a search result. NOTE: the property is named "Engagement ID" not "ID" — Notion reserves "id" as a system field name and rejects it. |
| Client | Relation → Clients (Nurture) | Single client per engagement. The synced backlink on the Nurture page is named "Engagements". |
| Offer | Multi-select | **Read the current options from the data source schema** — don't work from a list written down in this skill; they drift. Roughly: solo workshop, team/group workshops, 30-Day Intensive, Custom AI Training, AI Advisory, Ad Hoc Consulting. See `references/offer-scopes.md` for deliverable shapes. |
| Source | Multi-select | `LinkedIn`, `YouTube`, `Personal`, `ABB`, `ABA Contact`, `Homepage Contact`, `ABA Discovery Call`, `Referral`. Mirrors CRM Source options. |
| Status | Select | `Sold`, `Active`, `Delivered`, `Refunded`, `On Hold`. See Lifecycle below. |
| Start Date | Date | Date of first scheduled session (or kickoff date if no sessions yet). |
| End Date | Date | Date of last session, or projected end. Open for ongoing advisory. |
| Price | Number ($) | Contract value. Leave blank if unknown — never guess. |
| Paid Status | Select | `Unpaid`, `Partial`, `Paid in Full`, `Refunded`. Reflects payment status, not invoice state. |

---

## Naming Convention

Engagement titles are `E### - <Name>`: a 3-digit zero-padded number assigned in **temporal order by Start Date**, followed by the client name. Use the **organization name** when the client is a company (e.g., `E007 - [Company]`, `E004 - [Company]`) and the **person's name** for solo individuals with no company context (e.g., `E005 - [Client Name]`). Pull the name from the Client relation, never from a search result. The fixed-width `E###` prefix keeps an ID-ascending sort chronological regardless of the suffix.

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
**Stripe link:** [in_xxxxx](https://dashboard.stripe.com/invoices/in_xxxxx) — Paid in full M/D ($X). Billed to <email>.

_Optional one-line context (e.g., team workshop attendee list, payer info)._

## Program Scope
**Deliverables:**
- <bullet per deliverable, with count × duration when relevant>

**Bonus:** <if any; omit the line entirely if none>

**Guarantee:** <if any, with specifics on what triggers it; omit if none>

## Sessions

- <mention-page url="..."/> (M/D — name)
- <mention-page url="..."/> (M/D — name)

## Calls

- <mention-page url="..."/> (M/D — discovery / follow-up / etc.)

## Notes

- Short chronological log of what happened. Same style as CRM notes — date-stamped, comma-separated, no business context.

## 4Rs

_Framework reference: see "The 4Rs Framework" resource in Notion (https://www.notion.so/[page-id]) for the full operating system behind these four sub-headings._

### Results

_TBD at wrap_ — fill in concrete results during wrap-up (time saved, skills built, etc.)

### Re-up

_TBD at wrap_ — what happened next? New engagement, declined, or still considering?

### Referrals

_TBD at wrap_ — who got referred from this engagement?

### Reviews

- <mention-page url="..."/>  ← link the Testimonials DB record(s) for this engagement, one bullet per record (a team engagement links every attendee's row). The Testimonials record carries the live Status (Asked → Approved → Published → Declined), so don't restate status or quotes in prose here — the linked record is the source of truth. If no Testimonials row exists yet, leave _TBD at wrap_ and create the row when the ask goes out.
```

**Section rules:**
- **Program Scope** captures what was promised **at sale** — not what's actually being delivered. Pull defaults from `references/offer-scopes.md`. If a deal diverges from the canonical scope, write what Shaw confirms was sold.
- **Stripe link** stays at top, one line. If no Stripe invoice exists (paid via vendor portal, Venmo, etc.), italicize a one-line note explaining how it was paid.
- **Sessions** lists ABA Trainings mention-pages chronologically with `(M/D — name)` annotation
- **Calls** lists ABA Calls mention-pages chronologically with `(M/D — type)` annotation
- **Notes** mirrors CRM notes style: short, date-stamped, append-only
- **4Rs** stays as four sub-headings; fill in during wrap, then leave alone. **Reviews** is the exception to the prose style — it links the Testimonials DB record(s) (one mention-page per attendee), never restated status text, because that record holds the live status.

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

- **One invoice = one row.** Re-ups, multi-attendee team workshops billed together, and follow-on
  engagements all become new rows. Never collapse multiple invoices into one engagement.
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
