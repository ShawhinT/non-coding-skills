# Sync — Reconcile & Sweep (both tracks, one pass)

The database lags its source channels: forms get submitted, approvals and names arrive as
email, and the row still shows the old state. Reconcile against the sources before acting on
any Status. Run this at the start of every sweep and before writing any pre-draft.

## 1. Reconcile

1. **Query the default view once** (`notion-query-data-sources` in `mode: "view"`, `view_url` =
   the database URL with `?v=` from SKILL.md). This is the only DB query the sync needs.
2. **Read both form response sheets** (Drive `read_file_content`; IDs in SKILL.md). Match
   submissions to rows by Name.
   - **Unprocessed submission:** row still `Not Asked`/`Asked`, or Timestamp newer than
     Last Contact with answers not captured → run `testimonial-ask.md` §3. A submission
     supersedes any pending nudge.
   - **Orphans:** match against the *full* table including terminal rows before opening
     anything; only a name appearing nowhere is a true orphan — surface it.
3. **Gmail-sweep every row where either track is non-terminal** — one pass, one person at a
   time (`from:<email> OR to:<email>` since Last Contact). Don't skip rows that look
   settled; quiet-looking rows are where stale state hides. **Always read candidate threads
   with `get_thread`** — the `search_threads` message list truncates at ~5 messages with no
   indication, so a live thread reads as weeks-stale and a sent FU looks unsent.
   - A reply belongs to whichever track is live on that row — no cross-table guessing.
   - Review-track events → `testimonial-ask.md` / `testimonial-approve.md`.
   - Referral-track events (names given, intro landed) → `referral-ask.md` §2 /
     `referral-intro.md` §1.
   - A sent FU or ask found in sent mail is a real touchpoint: update Last Contact, set
     Next Contact per the SOP cadence.
   - On a row with no sibling record, an email that belongs to neither track (a value
     share, a delivery email) is still a touch: advance Last Contact, since this row is the
     only place the person's contact history lives. Leave Next Contact where it is. That
     date belongs to the track's cadence, and an off-track email neither fulfills nor
     delays the touch it schedules.
   - A reply that moves the touch itself is different: when the person names a new time and
     Shaw agrees to it in the thread, Next Contact moves to that time and the reply goes in
     Notes. Next Contact is the only schedule, so a date both sides have replaced is a stale
     one, and leaving it produces a nudge to someone who asked to be left alone until later.
     This holds on any row whose Next Contact lives here; where a sibling owns the touch, the
     date moves on the sibling instead. A deferral Shaw hasn't answered is surfaced, not
     written.
   - Ambiguous replies (conditional approvals, edits, anonymity questions) are surfaced,
     never auto-advanced.
4. **Backfill missing Context.** Rows created before the seeding rule (`testimonial-ask.md`
   §1 step 3) have blank bodies. When a row surfaces in the reconcile with no `## Context`
   section, write one from what the pass already gathered — the channel evidenced by the
   Gmail sweep, the win from the linked call/training page, the state of whichever track has
   run. Shape per `../crm/references/context-sections.md`. Backfill only rows the pass
   already touched; this is not a separate crawl of the database.
5. Status advances only on events that actually happened.
6. **A session wrapping with no ask scheduled yet is not a decision.** The training's own SOP
   owns the next touch after a session (for a 1:1, the post-session check-in) and the review
   ask rides on it, so the row sitting at `Not Asked` with a blank date is the standard
   pipeline working. Surface it only when nothing anywhere carries that post-session touch.

## 2. Sweep

1. From the same query result, filter client-side: **Next Contact ≤ today** on any row
   where the live track is non-terminal. Next Contact says a row is due; the two Status
   fields only say which track and which template. (Referral on-ramp rows sit at Referral
   Status `Not Asked` through the whole check-in phase — Status is the wrong filter, the
   date is the filter.)
2. Map each due row to its FU stage per the relevant SOP cadence (days since Last Contact).
3. **Sibling check** (the one cross-DB check left): for each due row, read the sibling
   record's Next Contact — the row `CRM` points at, else the `Friend` row; a row with
   neither has no sibling and skips this step. If both are live, ownership drifted — if this
   row's sequence is mid-cadence and the sibling date is stale, repair it (blank the sibling
   date, add the pointer, report the repair); if both are genuinely live, surface it as a
   decision per "One person, one next touch" in the `crm` skill.
4. Surface per row: name, track, status, days since Last Contact, which FU is due. Hand
   drafts to `email-helper`.

## 3. Scheduled-run report

The morning sync task renders one report per the `skimmable-summary` skill; the task file
declares the section map. Due rows are informational there (drafting belongs to
morning-emails); decisions, ready-to-publish, and ready-to-thank go in the closer.
