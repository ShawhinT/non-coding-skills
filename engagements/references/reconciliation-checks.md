# Reconciliation Checks

The canonical catalog of checks the engagement sync runs. `workflows/workflow-5-sync.md`
executes every check here; ad hoc audits reference the same list. Keep the checks defined
once, here — the workflow orchestrates, this file defines *what* "in sync" means and *how*
each gap gets closed.

## The triangulation principle

An engagement is in sync when independent sources agree:

- the **Notion engagement** (properties + body),
- the **money** (Stripe),
- the **delivery calendar** — what is actually booked, read from the booking feed, with ABA
  Trainings and ABA Calls as its Notion record — and
- the **relationship records** (Clients (Nurture), Reviews/Referrals).

Most discrepancies are exactly where two of these disagree — Notion says "Active" while the
calendar says the work is done; the body says "awaiting approval" while the Reviews/Referrals row
says Declined. Every check below is one axis of that agreement.

## Tiers

Each check is tagged with how the sync may act on it:

- **AUTO** — the correct value already exists in another record, so the fix is a deterministic
  copy. Safe to apply unattended and idempotently. Always logged in the digest under
  "Changes I made."
- **SURFACE** — needs judgment, touches money, creates a page/row, or composes free text.
  Never applied automatically; reported in the digest under "Needs your review."

**Idempotency contract for every AUTO fix:** compute the target from the source of truth and
apply only if the current value differs. Never append free text, never change money. Re-running
the same day must be a no-op.

**Page creation is permitted in exactly one place — Check 10.** Every other check copies a value
between records, and creating a page reads like a categorically different act, which is why this
contract once forbade it outright. But a session the booking feed says exists, whose shape an SOP
already specifies, is still a deterministic copy from a source of truth — the composition lives
in the SOP, not in the model. What stays forbidden is unchanged: free text, money, and any row
that no external source attests to. When the feed can't prove the event exists, there is nothing
to copy and the finding is SURFACE.

---

## Checks

### 1. Lifecycle Status vs Program Scope completion — AUTO (flip) / SURFACE (scoped deliverable outstanding)
- **Rule:** `Sold` = paid/committed, no session yet. `Active` = at least one session has occurred.
  `Delivered` = **every contracted deliverable in `## Program Scope` is complete** — not merely
  that the last dated session has passed. A dated session going by is necessary but not sufficient;
  the engagement is only done when nothing it was sold still owes delivery.
  What counts as *owed* comes from the offer's SOP (SOPs page → Delivery), not from the numbers in
  Program Scope alone: some offers sell a count as a ceiling — room to use, not a quota — and unused
  ceiling capacity is neither an outstanding deliverable nor a reason to hold the row open past its
  term. Read the SOP before treating any count as unfinished.
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
  A dated ABA Trainings/Calls row is **not proof the session happened** — read the page **icon**
  (`⭐` booked, `✅` held, `❌` no-show; see `notion-helper`). A `❌` row is a session that was sold
  and never delivered, so it neither advances the lifecycle nor closes out the deliverable: it holds
  the engagement `Active` and the underlying scope item stays open. Counting one as held is how a
  `Delivered` flip lands on work nobody received. The same read governs Check 2 — a no-show date is
  not an End Date. Don't rely on the body prose to say so; the prose is optional, the icon is not. The evidence bar runs one way: **a linked transcript is not proof the session was held** — a
  false start (both parties join, agree within minutes to reschedule, drop) records a transcript
  like any real meeting, and the night transcript-linker attaches it either way. Artifacts like
  transcripts or calendar attendance can corroborate the icon, never override it; a `⭐`/`⚠️` page
  with a transcript attached is a finding to surface, not an auto-flip to `✅`.

### 2. End Date vs last session — AUTO
- **Rule:** `End Date` = date of the last session.
- **Source of truth:** the latest linked session/call date.
- **Fix:** set `End Date` to the true last-session date (extend if a later session was added).
- **Traps:** leave open for ongoing `AI Advisory`. Don't shorten past a booked future session.

### 3. Reviews & Referrals 4R ↔ Reviews/Referrals DB — AUTO (link only)
- **Rule:** `### Reviews & Referrals` lists one mention-page per Reviews/Referrals record whose
  `Engagement` relation points to this engagement — each row carries both the testimonial and
  referral tracks. Never status text — the record holds the live status.
- **Source of truth:** the Reviews/Referrals `Engagement` relation.
- **Fix:** add a mention-page bullet for any matching record not yet linked. No duplicates.
- **Traps:** a team engagement links *every* attendee's row (each attendee has their own
  Reviews/Referrals row even though they all share the payer's CRM page). Do **not** auto-create a
  missing Reviews/Referrals row — that's SURFACE. If no record exists, leave `_TBD at wrap_`.
  **Re-up exception:** if the client has a newer engagement still `Sold`/`Active`, a missing
  Reviews/Referrals row on the older Delivered engagement is not a finding — the testimonial ask
  happens once, at the newest engagement's wrap.
  **Refunded exception:** a refunded engagement gets no review or referral ask — the refund
  closes both tracks (the client's Reviews/Referrals rows go Declined), and whatever the 4Rs
  section already links stays as-is. Skip Check 3's link consistency and Check 9's TBD-4Rs
  finding on `Refunded` rows: there's nothing to chase, so anything surfaced there is closer noise.

### 4. Sessions ↔ ABA Trainings — AUTO (clear) / SURFACE (ambiguous)
- **Rule:** every delivery session appears under `## Sessions` as a mention-page, and each
  in-body `(M/D — name)` label matches the linked page's real date.
- **Source of truth:** ABA Trainings rows for the attendee(s) within the engagement window.
- **Fix (AUTO):** correct a stale in-body date label to the linked page's canonical date; add a
  Trainings row that unambiguously belongs (matching attendee, within window) but isn't linked.
- **Fix (AUTO) — held state follows the icon:** on an engagement with a Deliverable Tracker, a
  line's state word (`booked` / `held`) and the track's `N / total` count are copies of the linked
  pages' icons, so they are deterministic too. When a linked page reads `✅`, drop `booked` from its
  line (in the tracker and in `## Sessions` / `## Calls` alike) and set the track's count to the
  number of linked pages with a `✅` icon. Log it under "Changes I made" like any other fix.
- **Fix (SURFACE):** a contracted session with no Trainings page at all (needs creation), or an
  attendee whose identity is ambiguous. Whether a session counts toward a track's total is defined by
  the offer's SOP (it may set a length threshold, or name session types that don't count and belong
  in ABA Calls rather than Trainings) — apply it from there. Surface only what the SOP doesn't
  settle; once Shaw answers, the line carries its number and the count follows from then on.
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
- **Rule:** the engagement's `Client` relation holds its decision makers and economic buyers
  (at least one), and each of those pages' `Engagements` relation includes this engagement.
- **Fix:** if the backlink is merely missing, AUTO-add it. If `Client` is empty or points to a
  conflicting page, SURFACE — don't guess. Don't auto-link other people at the same company;
  who counts as a decision maker is a judgment, not a join on `Company`.
- **Traps:** one client with many engagements is normal (e.g. [Client Name] = E002 + E005). Don't dedupe.

### 7. Paid Status ↔ Stripe — SURFACE (always)
- **Rule:** `Paid Status` reflects the real Stripe state, and `Price` matches the **sum of the
  engagement's invoices** — not any single one.
- **Installment engagements are not mismatches.** A contract billed in installments has a `Price`
  that no individual invoice equals ($18,000 against three invoices of $6,000). Compare against the
  total, and read `Paid Status` as a position along the schedule: `Partial` is the correct value
  once some but not all installments have cleared. Comparing `Price` to one invoice surfaces the
  same false positive on **every run for the length of the engagement** — months of a recurring
  finding that trains the reader to skim past this check, which is exactly how a real payment
  discrepancy gets missed. The engagement body's Payment Schedule table lists the invoice IDs;
  sum those.
- **Read the money axis from Stripe, not from Notion.** The recorded `Paid Status` (and the
  body's Stripe-line note) is a snapshot that goes stale between runs — payments routinely land
  in the gap, often the day before a `Sold` engagement's first session. So the source of truth
  for this check is a **live Stripe read**, not the cached status. Any engagement that is
  `Unpaid`/`Partial`, or `Sold`/`Active` with an outstanding invoice on file, gets its invoice(s)
  pulled from Stripe each run and compared to Notion. A body-only pass that trusts the recorded
  "Unpaid" will silently miss real payments.
- **If the Stripe connector isn't available in the run, this check doesn't run — skip it silently.**
  It is the only check whose source of truth lives outside Notion, so an absent connector is an
  environment fact, not a finding about the ledger. Reporting it as a caveat only adds noise to a
  digest that has nothing to act on. Don't fall back to the body's recorded Stripe line as a
  stand-in source of truth either — that snapshot is exactly what this check exists to re-verify.
- **Fix:** never auto-change money. Surface any mismatch (including "invoice now paid, Paid Status
  still Unpaid") with the invoice ID + amount + paid date. See `workflow-4-stripe-fill.md` for the
  lookup.
- **Traps:** proxy / vendor-portal payers ([Company], [Company], [Company] procurement) —
  search by **company domain**, not just the contact email. Payment may land in a different Stripe
  account/org, so "Paid in Full" can be true but unverifiable from the main account; a **voided
  invoice does not mean unpaid** (often replaced or collected elsewhere). Because money is
  high-stakes and frequently external, it is always human-reviewed.

### 8. Landed referrals ↔ CRM — SURFACE
- **Rule:** outbound referrals generated by this engagement are captured as a prose line in
  `### Reviews & Referrals` — per-person referral *status* lives in the linked rows, so this
  check covers engagement-level outcomes only.
- **Fix:** surface referrals found in CRM notes that aren't reflected in the body. Don't auto-write
  prose. (Note: an inbound referral that *created* this engagement belongs in `Source` + the
  referring engagement's Reviews & Referrals prose, not here.)

### 9. Body completeness + 4Rs content — SURFACE
- **Rule:** body has all sections in order; a `Delivered` engagement has its 4Rs filled, not `TBD`.
- **"All sections" means the required ones.** The body template's optional sections — Engagement
  Goal, Deliverable Tracker, Metrics, Ideas & Parking Lot — appear only when the deliverables call
  for them, so their absence is the template working, not a gap: a 1:1 workshop has no engagement
  goal and a two-session engagement has no tracker. Cosmetic variance between rows is not a finding
  either — a framework-reference line on some rows and not others, `Guarantee` vs `Guarantees`,
  `*TBD*` vs `*TBD at wrap*`, the order of Context bullets. The rows differ because the work
  differed. Only a missing **required** section is a finding: Context, Program Scope, Calls,
  Sessions, 4Rs.
- **Template drift is one finding, not one per row.** When the body template itself changes, every
  row written before it becomes non-conforming at once — a fleet-wide condition, not a
  per-engagement defect. Surfacing it per row means N identical lines every morning until someone
  migrates them, which is the Check 7 installment failure mode: a recurring false-positive block
  trains the reader to skim the whole check, and that is how a real discrepancy gets missed.
  Collapse drift into a single line naming the affected range (`E001-E012 predate the current
  template`), and weigh whether it's worth surfacing at all — a long-closed `Delivered` row is an
  archive record, not a work surface.
- **Fix:** surface missing structural sections and any `Delivered` engagement still showing `TBD`
  in Results / Re-up / Reviews & Referrals. Composing that prose is non-deterministic → human review.
- **Note:** once `Delivered`, the 4Rs are filled **once** at wrap; ongoing nurture lives in the
  Clients (Nurture) Notes, not back in the engagement (see the Engagements vs CRM boundary in
  `SKILL.md`).
- **Re-up exception:** when the client has a later engagement that is still `Sold` or `Active`,
  the older row's wrap-up rolls forward — don't surface its `TBD` 4Rs; fill them at the newest
  engagement's wrap (e.g., E002 defers to E005).

### 10. Booking feed ↔ paired pages — AUTO (clear) / SURFACE (ambiguous)
- **Rule:** every booked session or call belonging to a client with a `Sold`/`Active` engagement
  has a paired ABA Trainings / ABA Calls page, dated to match, with the event-type SOP's Setup
  applied in full.
- **Source of truth:** the booking feed — Calendly notifications primary, a short Google Calendar
  window as backstop. See `workflow-5-sync.md` → "The booking feed" for the parse shapes and the
  classification rules.
- **Scope:** engagement-linked events only. An attendee with no `Sold`/`Active` engagement row is
  out of scope here — free workshops and pre-engagement bookings are deliberately not this check's
  business (see Check 4's free-workshop trap; rows that don't exist yet belong to Workflow 1).
- **Fix (AUTO) — three states, all executed by handoff:**
  - *Booked, no page* → hand to `calendar-helper` Step 3.5/4, which reads the matching event-type
    SOP and runs its Setup **in full**: paired page, `FU - <First Name>` task, CRM bidirectional
    link, and the engagement's `## Sessions` / `## Calls` line. Creating only the page is the
    half-execution bug that skill exists to prevent.
  - *Moved* → hand to `calendar-helper`'s reschedule cascade (page Date, Precall/FU dates, the
    engagement body line, and End Date when the moved session is the last one).
  - *Cancelled* → archive the paired page per `notion-helper`'s convention and correct the
    engagement body.
- **Why handoff rather than inline:** `calendar-helper` already owns this recipe for the case where
  Shaw asks to schedule something. The only thing missing was an inbound trigger. Re-implementing
  the Setup here would create a second copy that drifts from the SOPs the moment an offer changes.
- **Traps:** a client with several open engagements and a date that doesn't disambiguate is
  SURFACE — don't guess which row the session belongs to. Discovery calls keep their existing
  carve-out and hand off to CRM Workflow 7, not here. And this check only ever runs
  calendar → Notion: never create a calendar event from a Notion row.

---

## Digest contract

Every run produces three groups:

- **Changes I made** — each AUTO fix: `E### · field · old → new · (source that drove it)`. A
  Check 10 handoff logs what was created or moved rather than a field diff — e.g.
  `E014 · created session page + FU task + CRM link · (Calendly, 8/5)`.
- **Needs your review** — each SURFACE finding, with enough context to act (invoice IDs, page
  links, the specific gap).
- **All clear** — engagements with no discrepancies, one line.
