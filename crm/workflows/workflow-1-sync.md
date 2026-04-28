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

Fire these four sub-agents in parallel (single message, multiple Task calls):

### Sub-agent A — Gmail Scanner

Purpose: find every new signal in Gmail since the last sync.

For each non-LinkedIn lead, client, **and active-campaign contact**, run three searches since
their `Last Contact?` watermark (campaign-contact emails come from the trackers Sub-agent C pulls):

1. `from:<email> OR to:<email>` — direct thread activity
2. `<company domain>` — catches cc'd stakeholders from the same org (e.g., a second contact
   at [Company] cc'd on a lead's thread)
3. Name-based fallback for Calendly: `from:notifications@calendly.com "<first> <last>"` —
   catches bookings where the invitee email differs from the CRM email on file

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
3. For each ABA Calls entry, check whether a matching CRM record exists (match by email, then
   name, then company domain). Return orphans as `{aba_call → proposed new CRM lead}`.
   **Only ABA Calls orphans trigger new CRM lead creation** — ABA Trainings pages are created
   by Shaw manually (or via Workflow 6) and don't imply a missing lead.
4. For each CRM lead/client, pull the **full list** of linkable pages from *both* ABA Calls and
   ABA Trainings matching their name, email, or company/domain. Also search related call
   databases (e.g., AI at Work Calls) for older context. Return the full ordered list per
   person so the main agent can rewrite the CRM page body in one shot via Workflow 4.

### Sub-agent C — CRM State Reader

Purpose: surface every lead, client, and active-campaign contact that's due for attention.

1. Pull **all** Active Leads (including `Lost`) and **all** Clients (Nurture). Lost leads are
   included because re-engagement dates live on `Next Contact`; excluding them silently kills
   the re-engagement cadence.
2. The primary filter is structured, not derived: flag every record where `Next Contact <= today`
   (Active Leads) or `Next Check-in <= today` (Clients). That single check covers FU #1/FU #2
   timing, post-proposal nudges, post-call BAMFAMs, Lost re-engagement, and any explicit future
   FU dates — all of which Workflow 2 sets per `references/follow-up-guidance.md`.
3. Also flag records where `Next Contact` is **blank** on any non-Closed/non-Lost lead, or
   `Next Check-in` is blank on any non-Churned client. That's a data-hygiene miss — Workflow 2
   should have set it. Call these out in the summary so Shaw can fix them or you can backfill
   from Notes.
4. For clients specifically, also flag `Last Contact?` >4 months ago regardless of `Next Check-in`
   — catches cases where a check-in got pushed out repeatedly and the relationship went cold.
5. **Active campaigns sweep.** Fetch the CRM page and read the Active Campaigns section. For
   each linked campaign page, locate its outreach tracker (inline database) and apply the same
   filter logic as Active Leads: flag contacts where `Next Contact <= today` or blank on a
   non-terminal status. Group results by campaign in the report so the main agent can act on
   them without re-querying. See SKILL.md → "Active Campaigns" for context on why this matters.

### Sub-agent D — Pre-Call Context Gatherer (conditional)

Only fire if any lead/client has an upcoming call in the next 7 days.

Rather than duplicating logic, **invoke the `pre-call-research` skill** for each upcoming call.
It handles the web + email + CRM research and writes the brief to the call page directly.
This keeps pre-call research logic in a single canonical home.

## Main-agent reconciliation (serial, writes)

Once the four sub-agents return, merge their reports and apply updates in this order:

### 1. Create missing ABA Calls entries

For any Gmail signal that references a **sales call** (discovery call booking, follow-up call,
proposal review) where no matching ABA Calls entry exists, create one. Name, Email, Date, Source.

Do NOT auto-create entries for delivery sessions (1:1 workshops, trainings) — those live in
the ABA Trainings database and Shaw creates them himself (or Workflow 6 does it on onboarding).
If a delivery session shows up in Gmail without a matching ABA Trainings page, just note it in
the summary so Shaw can decide.

### 2. Add missing CRM records

For any orphan ABA Calls entry (no matching CRM lead/client), create a new Active Lead using
**Workflow 3**. Pull context from the ABA Calls page body and any matching Gmail threads.

### 3. Update existing CRM records

For each record with new signals, apply **Workflow 2**:
- Append dated entries to `Notes` (short, `(M/D)` format)
- Update `Status` to furthest confirmed stage
- Update `Last Contact?` to most recent touchpoint
- For clients: update `Next Check-in` if a check-in just happened

### 4. Refresh ABA Call links in CRM pages

For every lead/client, call **Workflow 4** using the full ordered list from Sub-agent B.
Always rewrite the full list — never partial-append — so older calls that were never linked
get picked up automatically.

### 5. Graduate closed leads

For any lead now at `Closed`, apply **Workflow 5** to move them to Clients (Nurture).

### 6. Draft follow-ups

Apply follow-up rules from `references/follow-up-guidance.md`. For Gmail-reachable leads/
clients, create drafts directly. For LinkedIn-only leads, flag for manual DM.

**Missing follow-up audit:** In addition to cadence-based follow-ups, check whether any
recent calls or meetings (last 48 hours) are missing a follow-up email. Cross-reference
calls found in ABA Calls, ABA Trainings, and Google Calendar (`gcal_list_events`) against
Gmail sent mail (`from:shaw@aibuilder.academy to:<email> subject:"Call follow-up"
after:<call-date>`). Batch all missing follow-ups into a single prompt at the end of the
sync summary under a **"Calls missing follow-up emails:"** section. For each, ask Shaw
whether to draft one — and if yes, use the email-writer skill's call follow-up reference
(`references/call-follow-ups.md`).

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
`https://mail.google.com/mail/u/0/#drafts/<draftId>` (the `<draftId>` is the `id` returned by
`create_draft`, including the `r` or `r-` prefix). LinkedIn-only DM follow-ups go here too —
flag the channel inline instead of linking.

```
- [Name] ([source/segment] — [reason]) → [Gmail draft](<link>)
- [Name] ([source/segment] — [reason]) → Needs LinkedIn DM
```

### 2. Updates made to CRM

Flat list of every change you actually made during this sync: new leads added, status
transitions, Notes/date updates, call-link refreshes, graduations to Clients, schema changes,
expansion signals flagged on clients, etc. One bullet per change, terse.

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

**Both-way orphan detection is the key to mechanical correctness.** The failure mode that drops
leads is assuming Gmail is the only external signal. ABA Calls is also a source Shaw edits
directly, so every sync must check `ABA Calls → CRM` as well as `Gmail → CRM`.

**Multi-call refresh, not append.** When linking call pages into a CRM page body, always rewrite
the full ordered list. Appending means older un-linked calls stay invisible forever. Workflow 4
handles this — just make sure you pass it the full list from Sub-agent B.

**Calendly invitee emails may differ from CRM emails.** Match Calendly bookings by name, not
email. A lead can book with a personal email even when their CRM entry has a work email.

**Never skip LinkedIn-only leads during assessment.** They skip Sub-agent A's Gmail search but
still need cadence evaluation in the CRM State Reader. Flag due ones for manual DM.
