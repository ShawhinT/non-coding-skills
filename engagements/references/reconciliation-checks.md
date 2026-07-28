# Reconciliation Checks

The canonical catalog of checks the engagement sync runs. `workflows/workflow-5-sync.md`
executes every check here; ad hoc audits reference the same list. Keep the checks defined
once, here — the workflow orchestrates, this file defines *what* "in sync" means and *how*
each gap gets closed.

## The triangulation principle

An engagement is in sync when independent sources agree:

- the **Notion engagement** (properties + body),
- the **money** (Stripe),
- the **delivery calendar** (ABA Trainings sessions, ABA Calls), and
- the **relationship records** (Clients (Nurture), Testimonials).

Most discrepancies are exactly where two of these disagree — Notion says "Active" while the
calendar says the work is done; the body says "awaiting approval" while the Testimonials row
says Declined. Every check below is one axis of that agreement.

## Tiers

Each check is tagged with how the sync may act on it:

- **AUTO** — the correct value already exists in another record, so the fix is a deterministic
  copy. Safe to apply unattended and idempotently. Always logged in the digest under
  "Changes I made."
- **SURFACE** — needs judgment, touches money, creates a page/row, or composes free text.
  Never applied automatically; reported in the digest under "Needs your review."

**Idempotency contract for every AUTO fix:** compute the target from the source of truth and
apply only if the current value differs. Never append free text, never create pages or rows,
never change money. Re-running the same day must be a no-op.

---

## Checks

### 1. Lifecycle Status vs Program Scope completion — AUTO (flip) / SURFACE (scoped deliverable outstanding)
- **Rule:** `Sold` = paid/committed, no session yet. `Active` = at least one session has occurred.
  `Delivered` = **every contracted deliverable in `## Program Scope` is complete** — not merely
  that the last dated session has passed. A dated session going by is necessary but not sufficient;
  the engagement is only done when nothing it was sold still owes delivery.
- **Source of truth:** the `## Program Scope` deliverables checked against the linked ABA Trainings
  sessions and ABA Calls (including any wrap-up call) vs today. Read the scope, not just the calendar.
- **Fix (AUTO):** `Sold → Active` once the first session date ≤ today. `Active → Delivered` only once
  the last session is in the past **and** every other scoped deliverable — most commonly a wrap-up
  call named in Program Scope — has occurred, with nothing booked ahead. See `workflow-2-status.md`.
- **Fix (SURFACE):** when all dated 1:1 sessions are past but a scoped deliverable is still open —
  e.g. a wrap-up call that Program Scope lists but that isn't booked or held yet — do **not** flip to
  `Delivered`. Hold `Active` and surface "wrap-up call not booked" (or the specific missing
  deliverable) as the real next action. Group-workshop engagements (E004, E006, E008) routinely sell
  a wrap-up call as the closing deliverable, so the last participant 1:1 passing is not the finish
  line. An explicit hold note in the body (e.g. E009's "hold until 7/7 wrap-up call") is the same
  judgment written down — honor it; absence of such a note is not permission to auto-flip.
- **Traps:** a booked future session keeps it `Active` — never flip to `Delivered` if any session
  is today or later. `On Hold` is a manual judgment (30+ day stall) — never auto-set. Lifecycle is
  independent of payment: an engagement can be `Active` while `Paid Status` is `Unpaid`.

### 2. End Date vs last session — AUTO
- **Rule:** `End Date` = date of the last session.
- **Source of truth:** the latest linked session/call date.
- **Fix:** set `End Date` to the true last-session date (extend if a later session was added).
- **Traps:** leave open for ongoing `AI Advisory`. Don't shorten past a booked future session.

### 3. Reviews 4R ↔ Testimonials DB — AUTO (link only)
- **Rule:** `### Reviews` lists one mention-page per Testimonials record whose `Engagement`
  relation points to this engagement. Never status text — the record holds the live status.
- **Source of truth:** the Testimonials `Engagement` relation.
- **Fix:** add a mention-page bullet for any matching record not yet linked. No duplicates.
- **Traps:** a team engagement links *every* attendee's row (each attendee has their own
  Testimonials row even though they all share the payer's CRM page). Do **not** auto-create a
  missing Testimonials row — that's SURFACE. If no record exists, leave `_TBD at wrap_`.
  **Re-up exception:** if the client has a newer engagement still `Sold`/`Active`, a missing
  Testimonials row on the older Delivered engagement is not a finding — the testimonial ask
  happens once, at the newest engagement's wrap.

### 4. Sessions ↔ ABA Trainings — AUTO (clear) / SURFACE (ambiguous)
- **Rule:** every delivery session appears under `## Sessions` as a mention-page, and each
  in-body `(M/D — name)` label matches the linked page's real date.
- **Source of truth:** ABA Trainings rows for the attendee(s) within the engagement window.
- **Fix (AUTO):** correct a stale in-body date label to the linked page's canonical date; add a
  Trainings row that unambiguously belongs (matching attendee, within window) but isn't linked.
- **Fix (SURFACE):** a contracted session with no Trainings page at all (needs creation), or an
  attendee whose identity is ambiguous.
- **Traps:** the **notion-fetch stale-cache glitch** — the fetch tool sometimes returns a wrong or
  old page for a valid ID. Re-fetch by clean UUID and verify before concluding a mention-link is
  broken. Never "fix" a link that is actually correct. **Free workshops are not orphans:** a
  delivered workshop with no engagement row is only a finding if it was *paid*. Open the attendee's
  CRM page during the sweep and judge by what the note means, not by a specific phrase — any clear
  signal it was free or unbilled (e.g. "booked free 1:1 Claude Workshop", "comp'd", "no invoice")
  counts as documented, so skip it silently rather than deferring a "verify" ask to Shaw.

### 5. Calls ↔ ABA Calls — AUTO (clear) / SURFACE (ambiguous)
- Same shape as Sessions, for `## Calls` and the ABA Calls DB. e.g. a wrap-up call that exists in
  ABA Calls and references the engagement but is missing from the body → add the mention-page.

### 6. CRM link + backlink ↔ Clients (Nurture) — AUTO (add missing) / SURFACE (conflict)
- **Rule:** the engagement's `Client` relation points to the right Nurture page, and that page's
  `Engagements` relation includes this engagement.
- **Fix:** if the backlink is merely missing, AUTO-add it. If the `Client` relation points to a
  conflicting page, SURFACE — don't guess.
- **Traps:** one client with many engagements is normal (e.g. [Client Name] = E002 + E005). Don't dedupe.

### 7. Paid Status ↔ Stripe — SURFACE (always)
- **Rule:** `Paid Status` reflects the real Stripe state and `Price` matches the invoice total.
- **Read the money axis from Stripe, not from Notion.** The recorded `Paid Status` (and the
  body's Stripe-line note) is a snapshot that goes stale between runs — payments routinely land
  in the gap, often the day before a `Sold` engagement's first session. So the source of truth
  for this check is a **live Stripe read**, not the cached status. Any engagement that is
  `Unpaid`/`Partial`, or `Sold`/`Active` with an outstanding invoice on file, gets its invoice(s)
  pulled from Stripe each run and compared to Notion. A body-only pass that trusts the recorded
  "Unpaid" will silently miss real payments.
- **Fix:** never auto-change money. Surface any mismatch (including "invoice now paid, Paid Status
  still Unpaid") with the invoice ID + amount + paid date. See `workflow-4-stripe-fill.md` for the
  lookup.
- **Traps:** proxy / vendor-portal payers ([Company], [Company], [Company] procurement) —
  search by **company domain**, not just the contact email. Payment may land in a different Stripe
  account/org, so "Paid in Full" can be true but unverifiable from the main account; a **voided
  invoice does not mean unpaid** (often replaced or collected elsewhere). Because money is
  high-stakes and frequently external, it is always human-reviewed.

### 8. Referrals 4R ↔ CRM — SURFACE
- **Rule:** outbound referrals generated by this engagement are captured under `### Referrals`.
- **Fix:** surface referrals found in CRM notes that aren't reflected in the body. Don't auto-write
  prose. (Note: an inbound referral that *created* this engagement belongs in `Source` + the
  referring engagement's Referrals, not here.)

### 9. Body completeness + 4Rs content — SURFACE
- **Rule:** body has all sections in order; a `Delivered` engagement has its 4Rs filled, not `TBD`.
- **Fix:** surface missing structural sections and any `Delivered` engagement still showing `TBD`
  in Results / Re-up / Referrals. Composing that prose is non-deterministic → human review.
- **Note:** once `Delivered`, the 4Rs are filled **once** at wrap; ongoing nurture lives in the
  Clients (Nurture) Notes, not back in the engagement (see the Engagements vs CRM boundary in
  `SKILL.md`).
- **Re-up exception:** when the client has a later engagement that is still `Sold` or `Active`,
  the older row's wrap-up rolls forward — don't surface its `TBD` 4Rs; fill them at the newest
  engagement's wrap (e.g., E002 defers to E005).

---

## Digest contract

Every run produces three groups:

- **Changes I made** — each AUTO fix: `E### · field · old → new · (source that drove it)`.
- **Needs your review** — each SURFACE finding, with enough context to act (invoice IDs, page
  links, the specific gap).
- **All clear** — engagements with no discrepancies, one line.
