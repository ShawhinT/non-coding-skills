# Workflow 1: Three-Source Sync (Gmail ↔ ABA Calls ↔ CRM)

Use when Shaw asks to review, sync, or audit the CRM — whether leads, clients, or both. This
workflow covers **both** Active Leads and Clients (Nurture) in a single pass.

## Mental model

There are three sources of truth and they must be kept in sync with one another:

1. **Gmail** (`shaw@aibuilder.academy`) — ground truth for communications
2. **ABA Calls** — ground truth for sales call records + notes
3. **CRM** (Active Leads + Clients Nurture) — ground truth for pipeline state

Each reconciliation pass flows **Gmail → ABA Calls → CRM**, because each layer depends on the
one before. New communications reveal new calls; new calls must be reflected in ABA Calls
before the CRM can be updated with accurate pipeline state and linked call history.

The common failure mode is treating Gmail as the only external signal and forgetting that ABA
Calls is also a source Shaw is actively editing. Both-way orphan detection is how you catch
drift: any ABA Calls entry without a CRM record needs a new lead; any CRM lead with a known
call but no ABA Calls entry needs one created.

## Architecture — parallel sub-agents for the read phase

The read phase is the slow part of this workflow: many leads, multiple sources, each requiring
several searches. To avoid doing 15+ sequential fetches, fan the read work out to read-only
sub-agents in a single message and reconcile their outputs in the main agent.

**Writes always stay in the main agent.** Sub-agents must be read-only so they can't step on
each other or duplicate updates.

**Dispatch sub-agents A, B, and C with `model: 'opus'`.** This workflow's parallel fan-out
is especially prone to entity conflation across long parallel-source reports (e.g., attributing
one lead's notes to another, fabricating a Status from an unrelated mention). Opus is the floor
— don't downshift to Sonnet or Haiku for the read phase.

**All sub-agents must be dispatched in a single message with multiple Task calls.** Wall time = max(A, B, C, D), not sum. Serial dispatch — firing one, waiting for it, then firing the next — defeats the architecture and roughly N-multiplies the read phase. If you find yourself reaching for a second Task call after the first one has already returned, stop and fire the rest together.

### Sub-agent A — Gmail Scanner

Purpose: find every new signal in Gmail since the last sync.

For each non-LinkedIn lead, client, **and active-campaign contact**, run three searches since
their `Last Contact?` watermark (campaign-contact emails come from the trackers Sub-agent C pulls):

1. `from:<email> OR to:<email>` — direct thread activity
2. `<company domain>` — catches cc'd stakeholders from the same org (e.g., Srikanth at Matson
   cc'd on the Debarshi thread)
3. Name-based fallback for Calendly: `from:notifications@calendly.com "<first> <last>"` —
   catches bookings where the invitee email differs from the CRM email on file
4. **Multi-participant client engagements:** when the CRM record is a client whose engagement
   involves team-member sessions (visible as multiple ABA Trainings pages on the client's
   CRM page, each with a different participant email), expand the Gmail search to include
   `from:shaw@aibuilder.academy to:<participant-email>` for each participant. This catches
   per-participant follow-ups, intake forms, scheduling, reschedules, and testimonial chases
   that only touch the participant's inbox — none of which the primary-email or domain
   searches reliably surface back to the parent client record.

Also run one **global** search to catch brand-new leads who booked without an existing CRM
entry: `from:notifications@calendly.com subject:"New Event" after:<last-sync-date>`.

Return a structured per-lead delta report: new messages, new bookings, stakeholders cc'd,
and any orphan Calendly bookings that don't match an existing CRM record.

### Sub-agent B — ABA Calls + ABA Trainings + Google Calendar Auditor

Purpose: reconcile ABA Calls (sales calls), ABA Trainings (delivery sessions), and Google
Calendar events against the CRM. See SKILL.md's "Three Databases Show Up During CRM Work"
section for the distinction.

1. Pull all ABA Calls entries from the last ~90 days plus any future-dated entries.
2. Pull Google Calendar events for the same window using `gcal_list_events`. Match each event
   against ABA Calls and ABA Trainings entries by attendee name. Flag any calendar events that
   have no corresponding Notion page — these are meetings that happened but were never logged.
3. For each ABA Calls entry, check whether a matching CRM record exists in **Active Leads,
   Clients (Nurture), or 🧊 Archived Leads** (`collection://[page-id]`) —
   match by email, then name, then company domain. An Archived Leads match means the lead was
   previously triaged out (Lost / Disqualified, batch-archived) — it is **not an orphan**, just
   inactive. Do not flag Archived matches for new-lead creation; note them in the report as
   "matched in Archived Leads" so the main agent can skip them cleanly. Return true orphans (no
   match in any of the three tables) as `{aba_call → proposed new CRM lead}`. **Only ABA Calls
   orphans trigger new CRM lead creation** — ABA Trainings pages are created by Shaw manually
   (or via Workflow 6) and don't imply a missing lead.
4. For each CRM lead/client, pull the **full list** of linkable pages from *both* ABA Calls and
   ABA Trainings matching their name, email, or company/domain. Also search related call
   databases (e.g., AI at Work Calls) for older context. Return the full ordered list per
   person so the main agent can rewrite the CRM page body in one shot via Workflow 4.

### Sub-agent C — CRM State Reader

Purpose: surface every lead, client, and active-campaign contact that's due for attention.

1. Pull **all** Active Leads (including `Lost`) and **all** Clients (Nurture). Lost leads are
   included because re-engagement dates live on `Next Contact`; excluding them silently kills
   the re-engagement cadence. **Do not fetch 🧊 Archived Leads** — their `Next Contact` is
   always blank, so they're never due and never worth-reviewing. Archived Leads are Sub-agent B's
   concern (orphan matching), not Sub-agent C's.
2. The primary filter is structured, not derived: flag every record where `Next Contact <= today`.
   Same field on Active Leads and Clients. That single check covers FU #1/FU #2 timing,
   post-proposal nudges, post-call BAMFAMs, Lost re-engagement, scheduled client sessions, and
   any explicit future FU dates — all of which Workflow 2 sets per `references/follow-up-guidance.md`.
3. Also flag records where `Next Contact` is **blank** if context suggests it may be a miss —
   e.g., an active non-terminal lead with recent activity, or a client in `Active` status with
   no upcoming session date. Label these as "worth reviewing" in the summary. Never auto-fill
   `Next Contact` without Shaw's approval; blank is assumed intentional.
4. For clients specifically, also flag `Last Contact?` >4 months ago regardless of `Next Contact`
   — catches cases where a touchpoint got pushed out repeatedly and the relationship went cold.
5. **Active campaigns sweep.** Fetch the CRM page and read the Active Campaigns section. For
   each linked campaign page, locate its outreach tracker (inline database) and apply the same
   filter logic as Active Leads: flag contacts where `Next Contact <= today`. Only surface
   contacts with an explicit due date; blank `Next Contact` on campaign contacts is intentional.
   Treat `Added to CRM`, `Passed`, `Workshop Booked` (and any equivalent
   campaign-specific terminal status) as terminal — those contacts are either dead or being
   tracked in the main CRM, so they don't belong in the sweep. Group results by campaign in
   the report so the main agent can act on them without re-querying. See SKILL.md → "Active
   Campaigns" and "Promotion to main CRM" for context on why this matters.

**Required output format.** Sub-agent C must return its filter results as a structured table — not prose — so the main agent can verify them directly against the data source. For each table (Active Leads due, Clients due, each campaign tracker due), include:

- A header line stating both totals: `Active Leads scanned: N | Records with Next Contact <= today: M`
- One row per matching record: `Name | Email | Next Contact (verbatim) | Status (verbatim) | URL`

Verbatim means copied directly from the data source — no rounding, no paraphrasing, no derived assumptions about whether a record "should" be due. If `M` looks suspiciously low relative to `N`, that's a signal for the main agent to re-run the structured query in Step 0 before trusting the list.

### Sub-agent D — Pre-Call Context Gatherer (conditional)

Only fire if any lead/client has an upcoming call in the next 7 days.

Rather than duplicating logic, **invoke the `pre-call-research` skill** for each upcoming call.
It handles the web + email + CRM research and writes the brief to the call page directly.
This keeps pre-call research logic in a single canonical home.

## Main-agent reconciliation (serial, writes)

Once the four sub-agents return, merge their reports and apply updates in this order.

**Discovery-call bookings route to Workflow 7.** Before working through the steps below, pull
out any Calendly bookings Sub-agent A surfaced whose event type is a *discovery call* (per the
Discovery Call SOP — `ABA Intro Call`, `AI Transformation`, `1:1 Claude Workshop (Discovery)`).
Each one is handled end-to-end by **Workflow 7 (Discovery Call Intake)**, which orchestrates
the CRM record, the ABA Calls page and brief, the FU task, and the confirmation email. Run
Workflow 7 for each, then continue with the steps below for everything else.

### 0. Re-verify the "due today" list against the data source

Before acting on Sub-agent C's narrative, run a direct structured query against each data source — Active Leads, Clients (Nurture), and every active-campaign outreach tracker — for `Next Contact <= today`. Compare the result to Sub-agent C's Section 1/2/3. If counts differ or any record is missing, fetch the deltas yourself and add them to the working set.

This step exists because sub-agent prose is lossy: a record can silently drop out of a long parallel-source report (real failure mode: a contact-form lead due for FU#1 today wasn't surfaced because Sub-agent C's "due today" section returned two records that weren't even due, while the genuinely due record was omitted). Treat the data source as truth and the sub-agent narrative as a hint. If Sub-agent C's "due today" section looks suspiciously short relative to the size of the pipeline, that's the signal to re-verify, not skip.

For each due record, also pull `Last Contact?`, `Status`, and the most recent line of `Notes` so the summary has enough context.

### 1. Create missing ABA Calls entries

This step covers **non-discovery sales calls only** — discovery-call bookings are already
handled by Workflow 7 (see the routing note above), which creates their ABA Calls entry itself.

For any Gmail signal that references a non-discovery **sales call** (follow-up call, proposal
review, research chat) where no matching ABA Calls entry exists, create one. Name, Email, Date,
Source.

Do NOT auto-create entries for delivery sessions (1:1 workshops, trainings) — those live in
the ABA Trainings database and Shaw creates them himself (or Workflow 6 does it on onboarding).
If a delivery session shows up in Gmail without a matching ABA Trainings page, just note it in
the summary so Shaw can decide.

### 2. Add missing CRM records

For any orphan ABA Calls entry (no matching CRM lead/client), create a new Active Lead using
**Workflow 3**. Pull context from the ABA Calls page body and any matching Gmail threads.

Discovery-call bookings won't appear as orphans here — Workflow 7 creates their CRM record
(via Workflow 3 internally) as part of the same pass.

### 3. Update existing CRM records

For each record with new signals, apply **Workflow 2**:
- Append dated entries to `Notes` (short, `(M/D)` format)
- Update `Status` to furthest confirmed stage
- Update `Last Contact?` to most recent touchpoint
- Update `Next Contact` per the cadence rules in `references/follow-up-guidance.md`

"Confirmed" means actually happened — calls that took place, emails that were sent. Sub-agent
A's Gmail signal is the source of truth for sends; drafts created later in step 6 do NOT
advance `Status`, `Last Contact?`, or `Next Contact`. See "Drafts aren't touchpoints" in
SKILL.md.

### 4. Refresh ABA Call links in CRM pages

For every lead/client, call **Workflow 4** using the full ordered list from Sub-agent B.
Always rewrite the full list — never partial-append — so older calls that were never linked
get picked up automatically.

### 5. Graduate closed leads

For any lead now at `Closed`, apply **Workflow 5** to move them to Clients (Nurture).

### 6. Draft follow-ups

Apply cadence rules from `references/follow-up-guidance.md` to determine *who* needs a follow-up
and *what* the message should say (FU#1, FU#2, Calendly nudge, etc.). For *how* to draft and
send — voice, threading, draft management — defer to the **email-helper** skill. For
LinkedIn-only leads, flag for manual DM.

**Missing follow-up audit:** In addition to cadence-based follow-ups, check whether any
recent calls or meetings (last 48 hours) are missing a follow-up email. Cross-reference
calls found in ABA Calls, ABA Trainings, and Google Calendar (`gcal_list_events`) against
Gmail sent mail. **Use the actual session attendee's email** (from the ABA Trainings or
ABA Calls page) — not the parent client's email — and search broadly:
`from:shaw@aibuilder.academy to:<attendee-email> after:<call-date>`. Subject patterns vary
(e.g., "1:1 Claude Workshop Follow-up", "Call Follow-up"); don't constrain on subject or
you'll miss real follow-ups that used a different template. Batch all missing follow-ups
into a single prompt at the end of the sync summary under a **"Calls missing follow-up
emails:"** section. For each, ask Shaw whether to draft one — and if yes, use the
email-helper skill's call follow-up reference (`references/call-follow-ups.md`).

### 7. Expansion signal check (clients only)

For clients with recent Gmail activity, look for expansion signals: new use cases mentioned,
budget-cycle references, new hires, positive sentiment about past work. Flag candidates for
`Expansion` status in the summary — don't auto-change the status.

## Summary report format

Report back in three sections, in this order. Drop sections that are empty — don't show an
empty bucket. Do not include a "quiet / waiting on others" / "looks up to date" section.

### 1. Follow-ups due today

Bulleted list of leads/clients/campaign contacts who are *due right now*. For each bullet where
you created a Gmail draft, link the draft inline using
`https://mail.google.com/mail/u/2/#drafts/<draftId>` (the `<draftId>` is the `id` returned by
`create_draft`, including the `r` or `r-` prefix). LinkedIn-only DM follow-ups go here too —
flag the channel inline instead of linking.

```
- [Name] ([source/segment] — [reason]) → [Gmail draft](<link>)
- [Name] ([source/segment] — [reason]) → Needs LinkedIn DM
```

### 2. Updates made to CRM

Flat list of every change you actually made during this sync: new leads added, status
transitions, Notes/date updates, call-link refreshes, graduations to Clients, discovery-call
intakes run via Workflow 7, schema changes, expansion signals flagged on clients, etc. One
bullet per change, terse.

```
- [Name] — [what changed]
- Schema: [change]
```

### 3. Coming up

Everything on the near horizon. Split into two sub-lists so Shaw can triage at a glance:

- **Calls / sessions** — scheduled meetings, 1:1 workshops, training sessions (things on the
  calendar). Include the date/time and who it's with.
- **Messages to send** — follow-ups, check-ins, campaign pings Shaw needs to author or approve
  (including in-flight threads where the ball is in his court, like a testimonial chase).

```
**Calls / sessions:**
- [Name] — [date/time], [context]

**Messages to send:**
- [Name] ([source/segment]) — [reason, due date if applicable]
```

## Principles

**Multi-call refresh, not append.** When linking call pages into a CRM page body, always rewrite
the full ordered list. Appending means older un-linked calls stay invisible forever. Workflow 4
handles this — just make sure you pass it the full list from Sub-agent B.

**Calendly invitee emails may differ from CRM emails.** Match Calendly bookings by name, not
email. A lead can book with a personal email even when their CRM entry has a work email.

**Never skip LinkedIn-only leads during assessment.** They skip Sub-agent A's Gmail search but
still need cadence evaluation in the CRM State Reader. Flag due ones for manual DM.

**Sub-agent narratives are prose; the CRM data source is truth.** When a sub-agent reports a
structured field value (Status, Last Contact, Next Contact, Source) for a specific lead, verify
it against the CRM record before propagating into the summary or triggering a write. Common
failure mode: conflating one lead's notes onto another in a long parallel-source report —
e.g., attributing one lead's "hired in-house trainer" detail to a different lead, or fabricating
a `Booked Call` Status from an unrelated Calendly mention. Cheap fix: re-fetch the lead's row
from the data source whenever a sub-agent's claim would change the summary or trigger a write.

**Don't override structured cadence signals with derived heuristics.** When `Next Contact <= today`,
the lead is due — full stop. Don't reason "but it's only been 2 days since the last touchpoint,
give it the week." Shaw set that date intentionally. If the cadence feels wrong, the fix is to
update the field, not silently ignore it.
