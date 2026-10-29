# Workflow 5 — Daily Engagement Sync

Keep the Engagements ledger aligned with Stripe, the delivery calendar (ABA Trainings / ABA
Calls), and the relationship records (Clients (Nurture), Reviews/Referrals) — automatically each
morning, the same way the CRM sync keeps the pipeline current.

The check definitions live in `references/reconciliation-checks.md`. This workflow orchestrates
them: detect across every engagement, auto-apply the AUTO-tier fixes idempotently, and produce a
digest of what changed and what needs Shaw's eyes.

## When it runs

- **Scheduled (default):** daily, after the morning CRM sync so Clients (Nurture) and Reviews/Referrals
  are already fresh. Also runs after the night transcript-linker, so completed sessions are
  reflected on their ABA Trainings/Calls pages.
- **Ad hoc:** "audit the engagements", "sync the engagements", "is the engagement data up to date",
  "reconcile E###".

## Modes

- **Full sync (default):** detect + auto-apply the AUTO tier + digest.
- **Audit only:** detect + digest, change nothing. Use for a dry run ("just audit, don't touch").
- **Single engagement:** scope to one `E###` ("reconcile E006").

## Scheduled-run defaults

The daily scheduled task is a thin trigger — it carries no logic of its own and just invokes this
workflow. A bare invocation ("run the daily engagement sync") therefore uses these defaults:

- **Mode:** Full sync (detect + auto-apply the AUTO tier + digest).
- **Scope:** every row in the Engagements database.
- **Policy:** the AUTO / SURFACE tiers defined in `references/reconciliation-checks.md` *are* the
  agreed policy — apply AUTO automatically and idempotently, surface everything else. Money is
  never auto-changed. Check 10 is the one place the sync creates Notion pages, and only when the
  booking feed proves the event exists and an SOP defines the page's shape.
- **Delivery:** render the digest as the run's final report, per `skimmable-summary` — its
  delivery rule governs notifications (clean run: none; findings: a one-line ping, never the
  digest itself).

To change what the scheduled sync does — which fixes auto-apply, the cadence's expectations, the
digest shape — edit this workflow or the check catalog. Never put that logic in the scheduled task.

## Steps

1. **Pull the ledger and the reference sets once.** Query the Engagements default view (sorted).
   Pull the four reference databases in full so workers share one source of truth: Clients
   (Nurture), Reviews/Referrals, ABA Calls, ABA Trainings. Hit Stripe per engagement as needed — where
   "as needed" always includes any engagement that is `Unpaid`/`Partial` or `Sold`/`Active` with an
   outstanding invoice, so a payment that landed since the last run is caught (see Check 7). Don't
   trust the Notion-recorded Paid Status as proof of the current money state. If Stripe isn't
   connected, drop the money axis and run the remaining checks — no digest note.

2. **Pull the booking feed.** ABA Trainings and ABA Calls are the *record* of delivery, not the
   calendar itself — a page exists only once someone creates it, so a session booked this morning
   is invisible to every other check until then. Read the feed directly (see "The booking feed"
   below) and reconcile it against paired pages via Check 10.

3. **Fan out.** Dispatch subagents in parallel, each owning a slice of engagements (≈2 each) and
   carrying the shared reference data, so the sweep stays fast as the ledger grows. For a small
   ledger, inline is fine. (This mirrors how the original audit was run.)

4. **Run every check per engagement.** Walk `references/reconciliation-checks.md` top to bottom.
   - For **AUTO** checks: compute the target from the source of truth; if the current value
     differs, apply it with `notion-update-page` (Status, End Date, mention-page additions,
     date-label string fixes, held-state labels and tracker counts read off page icons, missing CRM
     backlink). Status transitions follow
     `workflow-2-status.md`; Stripe lookups follow `workflow-4-stripe-fill.md`; Check 10's three
     states hand off to `calendar-helper` rather than writing the pages here.
   - For **SURFACE** checks: collect the finding with its context. Apply nothing.

5. **Hold the idempotency line** (see the catalog's contract): AUTO fixes only ever write a value
   copied from a source of truth — a structured field from another record, or, for Check 10 alone,
   a page whose existence the booking feed proves and whose shape an SOP specifies. No free-text
   writes, no money changes, nothing no external source attests to. A second run the same day is a
   no-op: check Notion state before every write, including Check 10's, so a page created yesterday
   is found rather than duplicated.

6. **Compile the digest** in three groups:
   - **Changes I made** — `E### · field · old → new · (source)`, one line per auto-fix; Check 10
     handoffs log what was created or moved instead of a field diff.
   - **Needs your review** — the SURFACE findings: Paid Status mismatches (with invoice ID +
     amount), sessions/pages to create, `Delivered` engagements with TBD 4Rs, referrals to log,
     cross-DB cleanups.
   - **All clear** — engagements with nothing to do, one line each.

   Before a SURFACE finding lands as an ask, check whether a scheduled touch already covers
   it — a dated ABA task page (`FU - <Name>`, per `notion-helper`) or the client's CRM
   `Next Contact`. The sync's job is detection; Shaw's task system may already hold the
   response. A gap with a chase already on the calendar is reported as covered
   ("reschedule pending — FU set 8/25"), not asked about — an ask that duplicates an
   existing reminder dilutes the closer.

7. **Deliver the digest** as the run's final report, rendered per `skimmable-summary`.
   Notifications follow that skill's delivery rule: nothing on a clean run; a one-line ping
   (title + count) when something needs Shaw or the run failed — never the digest body.

## The booking feed

Two sources, in priority order. The first is a **delta** feed — it states what changed and when,
so detection is a bounded read. The second is **state**, which can only answer "what is true now"
and would need a diff to yield changes; it is the backstop, not the workhorse.

### Primary — Calendly notifications (Gmail)

Query `from:notifications@calendly.com` across the window since the last run (a daily task wants
roughly two days of overlap; re-reading is harmless because every write checks Notion state
first). These land on Shaw's **personal** address, `shawhintalebi@gmail.com`, not the business
one — a query scoped to the business inbox returns nothing and looks like a quiet day.

Body fields parse consistently:

```
Event Type: <offer / call type>
Invitee: <name>
Invitee Email: <email>
Additional Guests: <email, email>          <- only on multi-attendee sessions
Event Date/Time: <hh:mmam> - <Weekday, Month D, YYYY> (<timezone>)
```

**Classify on the subject prefix, never the body:**

| Subject shape | Means |
|---|---|
| `New Event: <invitee> - <time> <date> - <event type>` | new booking |
| `Updated: <invitee> - <time> <date> - <event type>` | reschedule |
| `Canceled: <event type> with <invitee> on <date>` | cancellation |

An `Updated:` mail carries the *identical* body sentence as a new booking ("A new event has been
scheduled"), so the prefix is the only discriminator. Reading the body alone labels every
reschedule a new session and creates a duplicate page for each move.

### Secondary — Google Calendar (short window)

Sweep `today → +14 days` only. This catches what Calendly never emailed: an event booked directly
on the calendar (an assistant scheduling on the client's behalf), or a notification that was
filtered or missed. Because the primary feed does the detecting, this window stays small — don't
let it grow into a full-calendar scan, which is the cost the delta feed exists to avoid.

## Known traps (recap — full detail in the catalog)

- **notion-fetch stale-cache glitch:** a valid ID can return a wrong/old page. Re-fetch and verify
  before declaring a mention-link broken or "fixing" a link that's actually fine.
- **A linked transcript ≠ a held session.** The transcript-linker attaches a transcript whenever
  a meeting recorded — including a false start where both parties joined only to agree to
  reschedule. Held/not-held is read from the page icon alone; a `⭐`/`⚠️` page carrying a
  transcript is a surface, never an auto `✅` flip.
- **The Notion DBs lag the calendar.** A Calendly booking hits the calendar within seconds and
  becomes an ABA Trainings/Calls page only when someone creates one. Any check reading only those
  tables is reading a record that is structurally behind reality — which is why the booking feed
  is a first-class source rather than an optional extra.
- **Reschedule chains — last one wins.** A single session can emit many `Updated:` mails (one 1:1
  emitted eight across five weeks). Group the window's mails by invitee + event type, take the
  latest, and reconcile once to the final state. Replaying each mail in order thrashes the page
  Date, the FU task, and the engagement's End Date, and floods the digest with phantom moves.
- **Cancel-then-rebook is a move, not a cancellation.** A `Canceled:` followed by a `New Event:`
  for the same invitee and event type inside the same window is one reschedule. Handling it
  literally archives a live page and then creates a duplicate beside it.
- **`Additional Guests:` defines the attendee set.** Multi-attendee sessions carry the extra
  addresses in that field and take a single page covering everyone (`[Person] & [Person 2]`, `[Person 3] &
  [Person 4]`), not one page each. Skipping the field creates single-attendee pages for 2:1 sessions —
  most damaging on exactly the group engagements this sweep is scoped to.
- **Don't read a tool response's embedded timestamp as the clock.** Notion's `as of ...` line and
  similar payload timestamps can be stale by hours. When timing actually decides something — did
  this land before or after the run? — get the real time instead of inferring it. A wrong clock
  turns a detection gap into a convincing but false "it happened after we looked," which closes
  the investigation on the wrong answer.
- **External / proxy payers:** money may sit in a different Stripe account or a vendor portal;
  "Paid in Full" can be true but unverifiable, and a voided invoice ≠ unpaid. Money is always
  SURFACE.
- **Multi-attendee testimonials:** each attendee has their own Reviews/Referrals row (all pointing at
  the payer's CRM page); Reviews links every one.
- **Lifecycle ≠ payment:** `Active`/`Delivered` is driven by session dates, not by `Paid Status`.
- **Not every delivered workshop is a missing row.** Some 1:1 workshops are intentionally free and
  have no engagement row by design — the attendee lives in the CRM, not the ledger. So the CRM check
  is part of the sweep, not a question for Shaw: when a delivered workshop has no engagement row,
  open the attendee's CRM page (Active Leads / Nurture) *during the run* and read what the note
  actually says. Judge by meaning, not by a magic phrase — any clear signal that the session was
  free or that no payment was expected (e.g. "booked free 1:1 Claude Workshop", "comp'd", "no
  invoice", or an explicit "skip in engagement syncs") means it's documented and silently skipped,
  not surfaced. Only escalate a true orphan whose CRM page shows it was a *paid* engagement that
  never got a row. Deferring a clearly-free session to Shaw as a "verify" ask is itself the miss —
  the whole point of opening the CRM page is to resolve it without his input.
