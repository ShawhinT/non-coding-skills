# Workflow 7: Discovery Call Intake

Use when a discovery call gets booked — either detected during a Workflow 1 sync (a Calendly
booking surfaced in Gmail) or when Shaw mentions in chat that a discovery call was booked.

This workflow is the **execution layer** for the Discovery Call SOP. The SOP owns intent,
policy, the question bank, the confirmation email template, and the alias list; this workflow
owns the tool calls, database IDs, payload shapes, and orchestration order. Read the Discovery
Call SOP before running — it's the source of truth for the *what* and *why*. Its page ID lives
in `notion-helper/SKILL.md` → "Event-Type SOPs."

## Trigger

- **During a Workflow 1 sync** — Sub-agent A surfaces a Calendly booking whose event type is a
  discovery call. Workflow 1's reconciliation hands it here instead of creating the ABA Calls
  entry and CRM record piecemeal.
- **Chat mention** — Shaw says a discovery call was booked (e.g., "so-and-so booked an intro
  call", "got a discovery call on the calendar for Friday").

## Discovery-call event types

Calendly books discovery calls under several event names — `ABA Intro Call`, `AI Transformation`,
`1:1 Claude Workshop (Discovery)` — and they **all resolve to one call type**. The Discovery
Call SOP holds the canonical list; treat any of them as a discovery call.

## Step 1 — Confirm the booking

Cross-check two sources so a booking isn't missed or misread:

1. **Gmail** — the `notifications@calendly.com` confirmation, subject
   `New Event: <name> - <time> - <event type>`. The invitee email, exact time, and any Calendly
   intake answers live in the body. (Global scan: `from:notifications@calendly.com
   subject:"New Event" after:<last-sync-date>`.)
2. **Google Calendar** — the auto-created event (`gcal_list_events` around the booked time).

Pull: invitee first name, email, exact call date/time, event type, and Calendly question
answers. The invitee email **may differ** from a CRM email on file — match by name, not email.

## Step 2 — Resolve the CRM record

Search Active Leads (`collection://[page-id]`) by name:

- **Existing lead** → apply **Workflow 2**: Status → `Booked Call`, bump `Last Contact?` and
  set `Next Contact` to the call date, append a dated Notes entry. If the booking email differs
  from the one on file, keep the CRM email as primary and note the alt in Notes.
- **Previously-`Lost` lead rebooking** → flip Status off `Lost`, then treat as a fresh
  discovery (Workflow 2 update).
- **New lead** → apply **Workflow 3** to create the Active Leads record. Source = `ABA Discovery
  Call` for a direct Calendly booking on aibuilder.academy; carry the real source if it's known
  to be something else.

## Step 3 — Create the ABA Calls page + brief

Invoke the **`pre-call-research`** skill. When invoked from this workflow it creates the ABA
Calls page, links it bidirectionally with the CRM record, and populates the pre-call brief —
all without asking Shaw first. Do **not** create the ABA Calls page yourself; pre-call-research
is the single creator, so it doesn't get made twice.

After pre-call-research returns, log the Calendly question answers in the ABA Calls page body
(per the Discovery Call SOP).

## Step 4 — Create the follow-up task

Hand off to **`notion-helper`** to create a `FU - [First Name]` task in the ABA database,
`Date` = call date + 1.

## Step 4.5 — Optionally pre-book a check-in (lead nurture safety net)

If Shaw indicates he wants a check-in pre-booked off the discovery (to keep the conversation
warm regardless of whether the discovery converts), hand off to **`calendar-helper`** to
schedule a `Name / Shaw - Check-in` event ~3 weeks out at the discovery slot's time-of-day.
calendar-helper consults the Check-in Call SOP for full Setup (paired ABA Calls page, FU task,
bidirectional CRM linking) — no extra orchestration needed here. Skip this step by default;
only run when Shaw explicitly asks for it.

## Step 5 — Draft the confirmation email

**Hard gate.** `email-helper` must be invoked in the current turn *before* the `create_draft`
call. This is not "defer to" — it's "stop and load." The failure mode this prevents: by the
time the workflow reaches step 5, the agent has already batched several writes (CRM record,
ABA Calls page, FU task) and the draft feels like one more parallel write. Composing inline at
that point produces off-template drafts that miss the SOP question selection, the threading
mechanics, and Shaw's voice rules. See the "When another skill is already running" section in
`email-helper/SKILL.md` for the canonical composition rule.

Once email-helper is loaded, its `discovery-call-confirmations.md` owns the threading mechanics
(reply inside the Calendly notification thread — or the contact-form / sales thread if the lead
came in that way) and points to the Discovery Call SOP for the canonical template and question
selection.

## Step 6 — Confirm

Summarize what happened: the CRM record (created or updated), the ABA Calls page link, the FU
task, and the confirmation email draft link.

## Note on drafts

The confirmation email is a *draft* until Shaw sends it — don't advance CRM state for the send.
Step 2's CRM update reflects only the booking itself. See "Drafts aren't touchpoints" in
SKILL.md; the next Workflow 1 sync picks up the send via Gmail signal.
