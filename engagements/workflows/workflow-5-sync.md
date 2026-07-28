# Workflow 5 — Daily Engagement Sync

Keep the Engagements ledger aligned with Stripe, the delivery calendar (ABA Trainings / ABA
Calls), and the relationship records (Clients (Nurture), Testimonials) — automatically each
morning, the same way the CRM sync keeps the pipeline current.

The check definitions live in `references/reconciliation-checks.md`. This workflow orchestrates
them: detect across every engagement, auto-apply the AUTO-tier fixes idempotently, and produce a
digest of what changed and what needs Shaw's eyes.

## When it runs

- **Scheduled (default):** daily, after the morning CRM sync so Clients (Nurture) and Testimonials
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
  never auto-changed.
- **Delivery:** post the digest the same way as the morning CRM sync.

To change what the scheduled sync does — which fixes auto-apply, the cadence's expectations, the
digest shape — edit this workflow or the check catalog. Never put that logic in the scheduled task.

## Steps

1. **Pull the ledger and the reference sets once.** Query the Engagements default view (sorted).
   Pull the four reference databases in full so workers share one source of truth: Clients
   (Nurture), Testimonials, ABA Calls, ABA Trainings. Hit Stripe per engagement as needed — where
   "as needed" always includes any engagement that is `Unpaid`/`Partial` or `Sold`/`Active` with an
   outstanding invoice, so a payment that landed since the last run is caught (see Check 7). Don't
   trust the Notion-recorded Paid Status as proof of the current money state.

2. **Fan out.** Dispatch subagents in parallel, each owning a slice of engagements (≈2 each) and
   carrying the shared reference data, so the sweep stays fast as the ledger grows. For a small
   ledger, inline is fine. (This mirrors how the original audit was run.)

3. **Run every check per engagement.** Walk `references/reconciliation-checks.md` top to bottom.
   - For **AUTO** checks: compute the target from the source of truth; if the current value
     differs, apply it with `notion-update-page` (Status, End Date, mention-page additions,
     date-label string fixes, missing CRM backlink). Status transitions follow
     `workflow-2-status.md`; Stripe lookups follow `workflow-4-stripe-fill.md`.
   - For **SURFACE** checks: collect the finding with its context. Apply nothing.

4. **Hold the idempotency line** (see the catalog's contract): AUTO fixes only ever overwrite a
   structured field with a value copied from another record. No free-text writes, no page/row
   creation, no money changes. A second run the same day is a no-op.

5. **Compile the digest** in three groups:
   - **Changes I made** — `E### · field · old → new · (source)`, one line per auto-fix.
   - **Needs your review** — the SURFACE findings: Paid Status mismatches (with invoice ID +
     amount), sessions/pages to create, `Delivered` engagements with TBD 4Rs, referrals to log,
     cross-DB cleanups.
   - **All clear** — engagements with nothing to do, one line each.

6. **Deliver the digest** to the same place as the morning CRM sync digest.

## Known traps (recap — full detail in the catalog)

- **notion-fetch stale-cache glitch:** a valid ID can return a wrong/old page. Re-fetch and verify
  before declaring a mention-link broken or "fixing" a link that's actually fine.
- **External / proxy payers:** money may sit in a different Stripe account or a vendor portal;
  "Paid in Full" can be true but unverifiable, and a voided invoice ≠ unpaid. Money is always
  SURFACE.
- **Multi-attendee testimonials:** each attendee has their own Testimonials row (all pointing at
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
