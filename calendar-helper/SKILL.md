---
name: "calendar-helper"
description: "Create, reschedule, and delete events on Shaw's Google Calendar — and keep the matching Notion page in sync when one exists. Use this skill whenever Shaw wants to put something on the calendar, move an existing event, or cancel one. Triggers include: \"schedule X\", \"create an event for\", \"put X on my calendar\", \"book a call with Y next Tuesday\", \"set up a 1:1 with\", \"another session with X next Saturday\", \"follow-up call with X\", \"reschedule the X meeting\", \"move my X call to Friday\", \"cancel the X event\", \"delete that meeting\", or any casual phrasing that implies adding/changing a calendar block (e.g., \"let's do another one with [First Name]\", \"block off Wednesday morning for the workshop\"). Even when Shaw doesn't say \"calendar\" explicitly, this skill should fire if the request is about scheduling. This skill also creates the paired Notion page in ABA Calls or ABA Trainings for every business-calendar invite."
---

# Calendar Helper Skill

Shaw's Google Calendar assistant. This skill creates, reschedules, and deletes calendar events
the way Shaw would do it himself — by looking at past similar events for the right naming,
duration, attendees, and Meet preferences, and by mirroring the calendar ↔ Notion pairing he
maintains for sales calls and delivery sessions.

The core principle: **never create an event from scratch when a reference exists.** Search
calendar history first, search Notion second, and let what's already there shape what gets
created next.

---

## What This Skill Does (and Doesn't)

**Does:**
- Create new calendar events with smart defaults pulled from past similar events
- Detect title patterns ("Session 1" → "Session 2", "Episode 4" → "Episode 5") and increment
- Auto-pair sales calls and trainings with Notion pages in `ABA Calls` and `ABA Trainings`
- **Execute the matching event-type SOP's Setup step in full** when one applies — not just the
  paired page, but the FU task, bidirectional CRM linking, and engagement linking that the SOP
  prescribes (the gap that previously left check-ins half-set-up)
- Reschedule and delete events, then hand the corresponding Notion page off to `notion-helper`

**Doesn't:**
- Build rich event descriptions from Gmail/Notion context (planned for a later iteration —
  for now, copy the reference event's description verbatim if it has one, and leave the
  field empty if there's nothing to copy)
- Run discovery-call intake — a Calendly-sourced discovery call is CRM Workflow 7's job (see
  "Discovery calls are Workflow 7's territory" under Step 3)
- Manage Notion pages for non-create operations directly — those hand off to `notion-helper`
- Take over for `crm`, `meeting-prep`, `executive-briefing`, or `notion-helper` when the
  request is really about one of those

---

## Which Calendar

Shaw has three writable calendars:

| Calendar | Role |
|---|---|
| `shaw@aibuilder.academy` | **Business** — all ABA work: sales calls, trainings, workshops, partner calls, work blocks |
| `shawhintalebi@gmail.com` | General |
| `[email]` | Personal |

ABA work is the default. Pass the business calendar ID explicitly on every create, update, and
delete rather than relying on the connector's default — the default is the primary account, not
the business one, and an event that lands on the wrong calendar is invisible to the people who
need it. Use general or personal only when the request is plainly non-ABA, and ask when it isn't
obvious which.

When searching for a reference event (Step 2), search the calendar the new event will land on. A
past session lives where it was created, so searching the wrong one returns nothing and drops you
into the no-reference defaults for an event that actually has a template.

---

## Core Workflow: Creating a New Event

Most requests look like "schedule X with Y next [time]" or "another session with Z next
Saturday at noon". Walk through these steps in order.

### Step 1 — Parse the request

Extract from the user's message:
- **Who** (attendee names, emails if given)
- **What** (topic / event type — sales call, training, 1:1, workshop, etc.)
- **When** (date and time; resolve relative dates like "next Saturday" against today's date)
- **Duration** (if specified — otherwise leave for reference lookup)
- **Recurrence** (if implied — "every other Tuesday", "weekly")

If any of these are missing AND can't be filled from a reference event in Step 2, that's an
ambiguity to surface in Step 5.

### Step 2 — Find a calendar reference

Use `list_events` to search Shaw's calendar for past events that match the request. The right
search depends on what's available:

- **Attendee + topic** is the strongest signal. E.g., for "another session with [First Name]", search
  for past events with [First Name]'s email on the attendee list.
- **Topic alone** if no attendee is named (e.g., "schedule the next podcast recording" →
  search for "podcast" in past event titles).
- **Pure recurrence** (e.g., a weekly standup) may have no attendee and no topic keyword —
  search the calendar for the same time slot in prior weeks.

Take the **most recent matching event** as the primary reference. If multiple recent events
have conflicting patterns (e.g., last 3 sessions were 60 min, 30 min, 90 min), surface the
ambiguity in Step 5 rather than guessing.

From the reference event, extract these defaults:
- **Title pattern** (see "Title pattern detection" below)
- **Duration** (end time minus start time)
- **Time of day** (use only if the request didn't specify)
- **Attendee list** (preserve unless the request changes it)
- **Google Meet** (on/off — match the reference)
- **Color** (`colorId`)
- **Notification level** (default to `ALL` for events with attendees, `NONE` for solo blocks)
- **Description** (copy verbatim if present; leave blank if not). Event descriptions are guest-visible — every attendee sees the same invite, so the description is an external-facing field, not a private scratchpad. Keep it to the shared purpose of the meeting (what it's for, what to expect). Never put internal notes in it: who to confirm timing with and when, internal reasoning, pricing, lead status, prep reminders, or anything you wouldn't say to the attendee's face. Those belong on the paired Notion page or a personal note. If a reference event's description carries an internal line, drop it when copying rather than propagating it. Descriptions are **inherited, not authored** — when no reference event supplies a usable one, leave the field empty rather than composing a summary of the meeting. A manually scheduled invite is a title, a time, and a Meet link; the context already lives in the email thread that produced it, so a written-from-scratch description only restates what the attendee just agreed to. This applies to Calendly-sourced references too: those descriptions are Calendly's intake boilerplate (cancel/reschedule links, form answers) and belong to that booking, not to an invite Shaw creates by hand.

### Step 3 — Pair the event with a Notion page

Every invite on the business calendar — any event with someone besides Shaw on it — gets a
paired page: ABA Trainings for delivery sessions, ABA Calls for everything else. The page is
where prep and notes live, and a meeting with no page is one nobody prepares for. Holds count:
a hold Shaw sends is a real invite. Solo blocks and events on the other calendars don't get one.

Use `notion-search` to find the reference event's paired page, to mirror its title and body
shape. Search the most likely database first:

| Calendar event type | Notion database | Database page ID |
|---|---|---|
| Any non-delivery call (sales, follow-up, coffee chat, partner) | `ABA Calls` | `[page-id]` |
| Training / delivery / workshop / 1:1 session | `ABA Trainings` | `[page-id]` |

Search query: combine attendee name + topic keywords (e.g., "[Client Name] skill building"
or "[First Name] training session"). Look at the top 1-3 matches and pick the one whose title most
closely mirrors the calendar event's title pattern. When none exists, create the page anyway.
Discovery calls are the one carve-out — see Step 3.5.

### Step 3.5 — Consult the matching event-type SOP

For sales-call and training events, look up the matching event-type SOP on the SOPs page
(`[page-id]`). Fetch that page and match its child pages by title —
don't work from a list memorized here, because the set changes as offers change, and a
remembered title that no longer exists sends you hunting for an SOP that was never there. As of
this writing: **Acquisition** — Discovery Call, AI Rollout Audit Call. **Delivery** — 1:1 Claude
Workshop, Group 1:1 Claude Workshops, Team Workshop, Check-in Call (plus its variant spokes),
Wrap-up Call. Treat that list as a dated snapshot,
not the source of truth. See `sop-helper` for how SOPs are structured and found. Read the SOP's
**Setup** section — it's the authoritative recipe for everything that happens around the
calendar event in Notion. The SOP defines:

- What the paired page's body should contain (usually a one-liner with the CRM link — not
  empty)
- Whether a `FU - [First Name]` task gets created in ABA, and on what date
- Which record the page links back to and where the `## Calls` entry goes — see "Which record
  a call links to" under Step 4
- Whether the page links to an Engagements row (when the call sits inside a paid engagement)

In Step 4 you'll execute this Setup in full — not just the paired page.

**Match the SOP by the call's purpose, not by which SOP has a Setup.** Each SOP opens with a
`**Context**:` line defining the call it covers; confirm the event fits that definition before
running its Setup. A call booked as the next step of a prior call (a BAMFAM) is owned by the
*prior* call's SOP — e.g. the proposal walkthrough booked off a discovery call is set up per the
Discovery Call SOP as a `Follow-up`, not as a Check-in. A Check-in is a relational catch-up
triggered by a cadence; a Follow-up exists to discuss something specific from a prior call.
Reaching for the nearest SOP that happens to have a Setup is how a follow-up gets mislabeled.

**Check-in Calls share one Setup across variants.** The Check-in Call SOP is a base plus several
variant spokes, which the base SOP lists. The Setup mechanics are identical across all of them
and live in the **base "Check-in Call"** SOP; the specific spoke governs only pre-call research +
templates, not Setup. So for calendar setup, read the base "Check-in Call" Setup — the spoke
doesn't change what gets created in Notion.

**Discovery calls are the carve-out.** The Discovery Call SOP's execution layer is **CRM
Workflow 7** (it orchestrates `meeting-prep`, `notion-helper`, and `email-helper` together
— too involved to inline here). For a Calendly-sourced discovery call, create the calendar
event and hand the Notion side off to Workflow 7 — don't run the SOP yourself. Every other
call-type SOP (Check-in, Wrap-up, 1:1 Workshop, Group Workshop) gets executed by
calendar-helper directly.

**No SOP applies?** The page is still owed (Step 3); the SOP only supplies the specifics.

- **An ABA event whose offer isn't documented yet** — a new or ad hoc offer (a standalone paid
  office hour, a one-off advisory session) is still a paid delivery session or sales call, and
  still earns the standard pairing: paired page in the matching DB, engagement link, FU task.
  Run the closest comparable SOP's Setup as the template, and tell Shaw the SOP is missing so
  the gap gets closed rather than re-improvised next time.
- **An ABA event that isn't an offer at all** — coffee chats, peer syncs, partner catch-ups,
  podcast intros, three-way intros. No money moves, so there is no engagement to link and no
  SOP will ever exist for these. They still earn the same record: a paired page in `ABA Calls`
  with pre-call research, and a bidirectional link — to the **Friends** database (under
  Partners, `collection://[database-id]`) rather than Active Leads or
  Clients (Nurture), because the person is a peer, not a lead or a client. Revenue determines
  *which* record the call links to; it never determines *whether* one is created.

### Step 4 — Build the event and execute the SOP's Setup

Compose the calendar event using the defaults from Step 2, with the request overriding
where it explicitly differs (e.g., user said "noon" → use noon, not the reference time).

If a Notion page is needed (per Step 3 — and not pre-empted by the discovery-call carve-out
in Step 3.5), execute the SOP's Setup section in full. That typically means:

- **Create the paired page** — title matching the calendar event's pattern (or a slightly
  trimmed version matching the destination DB's naming convention; sample 2-3 recent pages to
  confirm). Date = the calendar event's date. **Icon** = `⭐` (the default for ABA Calls /
  ABA Trainings pages — canonical icon conventions live in `notion-helper` → "Default icons
  by page type"). **Body** = per the SOP's Setup — typically a
  one-line link to the record that owns the relationship (`CRM:` or `Company:`, see below)
  plus a single short time-of-day line; not empty.
- **Create the FU task** if the SOP calls for one (it usually does — `FU - [First Name]` in
  ABA, dated call date + 1, icon `✉️`). Every delivery session gets a follow-up email, so the
  FU task is the norm for trainings, not an extra.
- **Append the bidirectional link** — a `## Calls` line pointing at the new page on the record
  that owns the relationship, where that record has a `## Calls` section (see below).
- **Link to an Engagements row** if the SOP calls for it (see Step 4.5 below for the trainings
  case; for check-ins or follow-up calls, only when the client has an active engagement).

**Which record a call links to.** The link follows who owns the relationship, not which
database is called "the CRM." A person with their own row — a lead in Active Leads, a buyer or
champion in Clients (Nurture), a peer in Friends — gets a `CRM:` line to that row and a
`## Calls` backlink on it. Anyone else at a client account (a session participant, a department
lead, a stakeholder who never entered a commercial conversation) has no row of their own by
design; their call links to the **Companies** record with a `Company:` line instead, and no
backlink is written there, because the Companies body is Context-only and the account's call
history already lives on the engagement's `## Calls` list. Pointing such a call at the nearest
buyer's row makes that buyer's history lie about how often Shaw has spoken to them. The `crm`
skill owns the who-gets-a-row rule; this step only follows it.

If you only create the page and skip the rest, you've half-executed the SOP — that's the bug
this section exists to prevent.

**A repeat session's page links to context; it doesn't re-derive it.** The SOP's session-page
skeleton assumes a *first* session with someone, where the pre-call brief (person, company,
from emails, intake, read) is the only place that research exists. Session N of a multi-session
engagement is the opposite case: the person and company are already written up on the prior
session page, and the scope lives on the engagement. So the page opens with links — `CRM:`,
`Engagement:`, `Previous session:` — then the time line and the agenda, and skips the brief.
Restating research the reader can reach in one click is how two pages for the same client drift
apart, and it spends prep time on a client who is no longer unknown.

### Step 4.5 — Link new Notion page to its engagement (trainings only)

When the page you just created is in **ABA Trainings** (a delivery session), the matching
engagement row in the Engagements DB needs a backlink to the new session. Without this, the
session exists in ABA Trainings but the engagement page stays out of sync — anyone looking at
the engagement won't see the new session in its `## Sessions` body section.

Steps:
1. Fetch the client's Clients (Nurture) page (search by name/email)
2. Read the synced "Engagements" backlink property — pick the engagement whose `Status` is
   `Active` or `Sold` and whose date range brackets the new session
3. Append the new mention-page line to the engagement's `## Sessions` section in chronological
   order

This is the `engagements` skill's `workflow-3-link-session.md` — hand off there for the exact
body update pattern (chronological insertion, exact-string `update_content` calls).

When the page is in **ABA Calls** (a sales call), only link if an engagement *already exists*
for this client (e.g., mid-engagement check-in or follow-up call). Most discovery calls predate
the engagement and don't need linking.

### Step 5 — Confirm or create

**Default behavior: create then report.** If the request is unambiguous (clear attendee,
clear date, clear reference event, clear Notion pairing), just do it. Then report back with:
- The created event (link, time, attendees, Meet URL)
- The created Notion page (link), if one was created
- One sentence noting which reference event/page was used

**Don't ask about the Notion side — execute it.** When the event is a sales call or training,
the paired page + FU task + CRM linking is part of the standard Setup, not an opt-in. Even
when the user's request sounds focused on just the calendar event ("schedule the check-in for
next week", "put it on my calendar", "send him a Google Meet"), the full Setup still runs by
default. Asking "do you also want the Notion pages?" is the half-execution bug Step 3.5 exists
to prevent — just report what got created. The discovery-call carve-out (Workflow 7) is the
only exception.

**Surface ambiguity via `AskUserQuestion`** when:
- Multiple attendees match the name (which [First Name]?)
- Multiple reference events have conflicting patterns and no recent winner
- Duration is undefined and no reference exists
- Event type is unclear (sales call vs. training) and a Notion page might be needed
- Date/time can't be resolved confidently

Don't ask about things that don't matter — color, Meet preference, notification level all
have safe defaults.

---

## Title Pattern Detection

Many of Shaw's recurring events use numbered patterns. Detect these and auto-increment.

**Examples:**
- `[First Name] / Shaw - 1:1 Skill Building (Session 1)` → `(Session 2)`
- `LFC Recording — Episode 12` → `Episode 13`
- `Cohort 3 Workshop, Week 4` → `Week 5`
- `ABN Issue #47` → `#48`

If the pattern increments, use the incremented title. If the pattern doesn't increment (a
generic recurring meeting like "Weekly Sync"), reuse the same title.

When you can't tell whether the user wants the next number in a sequence vs. a one-off,
default to incrementing — that's almost always what Shaw means when he says "another one"
or "next session".

**Separator semantics — `/` vs `x`.** `/` means working together (1:1 sessions, group
sessions, check-ins, wrap-ups — any event with a closed or active client). `x` means
exploring a collab (intro calls, discovery calls, exploratory chats with cold/warm leads
we haven't worked with yet). Never `:`, `+`, `&`, `and`. When a lead converts to paid,
the next event flips from `x` → `/`. Decide by relationship status (per CRM), not by
what the reference event used — a stale `x` on a paid client's reference is the bug
to avoid. Relationship status also beats an SOP's title template: the Check-in Call
SOP writes `[First Name] / Shaw - Check-in`, but a lead-nurture check-in with a warm,
unconverted lead still takes `x` — SOP templates assume the common (client) case and
don't override the separator rule.

**Name vs company in the title.** Use the attendee's first name when they're the only
person on the other side (`[First Name] / Shaw - 1:1 Claude Workshop`). Use the company
name when multiple people from their side are attending (`[Company] / Shaw - Wrap-Up Call`,
`[Company] / Shaw - Check-in`). This applies to any event type.

**Spaces around `/` and `x` separators.** When a title joins two names with `/` or `x`,
always include surrounding spaces: `[First Name] / Shaw – Catch-up`, never `[First Name]/Shaw`. Same for
`x` collabs: `[First Name] x Shaw`, never `[First Name]xShaw`. This applies to any new title composition;
when mirroring an existing reference event, preserve its exact format.

**Suffix the event type after the names.** Coffee chats, check-ins, workshops, and 1:1s
all take an explicit suffix: `[First Name] / Shaw - Coffee Chat`, `[First Name] / Shaw - Check-in`,
`[First Name] / Shaw - 1:1 Claude Workshop`. A bare `Name / Shaw` (no suffix) is rare — only
use it when the reference event also has none AND the type is genuinely ambiguous. When
in doubt, infer the type from context (CRM status, email thread, prior call notes) and
add the suffix. Older Calendly auto-imports often dropped suffixes — don't take that as
license to drop them on manually scheduled events. When Shaw names the topic himself
(a BAMFAM like "July 9 at 2:30 - AI Strategy"), his stated topic *is* the suffix —
use it verbatim rather than substituting the SOP's generic type suffix; the SOP still
governs which Setup runs, just not the title.

**BAMFAM follow-ups booked right after a call.** When Shaw says "just finished a call
with X, set up the follow-up", the just-ended call's paired ABA Calls page usually has
the BAMFAM recorded in its Follow-up section — check it (and today's calendar) first to
confirm which person/company X is and what the follow-up covers, before searching wider
history. A same-day event with a matching attendee is a stronger identity signal than a
name match on an older event.

**Holds and tentative events.** When Shaw asks for a "hold" or a tentative placeholder,
prefix the title with `[HOLD] ` — brackets, trailing space — e.g. `[HOLD] [Company] / Shaw -
Check-in`. What a hold carries depends on who will send the real invite. For a meeting Shaw
hosts (a call with unlocked timing), the hold *is* the invite: keep the attendees, Google Meet,
and `ALL` notifications exactly as a normal event. For a session the client will invite him to
(a training or workshop — the Team Workshop SOP holds only until the client's invite arrives),
the hold is Shaw's private placeholder: no attendees, no Meet, notifications `NONE` — a guest
would be emailed about an event that isn't the real one. When it's unclear which kind, ask
before adding anyone, since an invite emails the other side and can't be unsent. The type suffix
still has to fit *this* event, not the reference: when the relationship has moved on, the
suffix moves with it (a wrap-up call's next touchpoint is a `Check-in`, not another
`Wrap-Up Call`).

---

## Rescheduling an Event

When Shaw asks to move an event ("move my call with Y to Thursday", "push the training to
next week", "reschedule X for 3pm"):

**The calendar may already reflect the new time.** Many reschedules are externally driven —
Calendly moves the event (and emails the attendees) before Shaw asks, so his request is really
"sync the rest to the new date." A Calendly-moved event is recognizable by its description
(reschedule/cancel links, "Rescheduled from connected calendar event") and often a
freshly-canceled twin sitting at the old slot. So check the event's current state before
touching it, and let what you find decide whether step 2 runs at all.

**A reschedule can also arrive as a cancel-and-rebook pair rather than a moved event.** When the
other side owns the booking — Shaw rebooks on *their* Calendly, or they send a fresh invite — the
original doesn't move: it stays at the old slot renamed `Canceled: <original title>`, marked free
and declined, with a `Cancellation Reason:` line in its description, while a *separate* new event
appears at the target time. Searching for the old event alone finds a cancellation and looks like
the call died, so when a search turns up a canceled twin, scan the surrounding days for a new
event with the same attendee before concluding anything.

Two things follow from the replacement being a different event rather than the same one moved.
First, **nothing carries over — re-read it all from the new event**: duration, Meet link, and time
zone can all differ (a 25-minute slot on Shaw's Calendly comes back as a 30-minute one on theirs).
Second, **Shaw is a guest on it**, so the title is whatever their booking system generates and he
can't rename it to the `Name / Shaw - Type` convention — don't attempt an `update_event` that will
fail on permissions. Make the paired Notion page carry the mapping instead: put the new time,
duration, Meet link, and why the invite looks foreign in its Call line, so the page stays the way
back to the calendar entry. Leave the canceled twin alone — it shows as free and doesn't block the
day; note it rather than deleting it, since deleting fires another notification for a call that's
already settled.

1. **Find the event** with `list_events` (filter by attendee, title keyword, or date range).
   If multiple match, ask via `AskUserQuestion`.
2. **Update the event** with `update_event` — change `startTime` / `endTime`, keep everything
   else (attendees, Meet URL, description). Skip this step entirely when the event already
   sits at the target date/time (the Calendly case above) — there's nothing to write, and the
   real work is the Notion cascade below.
3. **Apply the reschedule cascade — SOP first when one exists.** A reschedule is rarely
   just a calendar move: any paired call/session carries date-anchored infrastructure that
   breaks when the date changes. As a general default, a call may have a
   `Precall - {First Name}` (date − 1), an `FU - {First Name}` (date + 1, create if missing),
   an engagement body `## Sessions` line to keep in chronological order, and any day-of
   comms — shift each to the new date. When shifting a FU or Precall's date, also scan the
   body text for inline date references (e.g., "Send follow-up email after 7/1…") and update
   those too — the date property and the body can drift out of sync if only one changes.
   If a Precall or FU task is already ✅ completed, leave it alone — don't reassign a
   completed task to the new date. Check whether prior reschedules of this same session
   already established a pattern (e.g., a fresh `Precall - {First Name}` created per
   reschedule): if so, mirror it — create the fresh task directly (copy the last one's
   body, date = session − 1) and report it. Only fall back to flagging it and offering
   to create the task when there's no pattern to mirror.
   Pages that carry a per-reschedule history keep it in the same format — append a
   matching entry wherever one exists (the session page's research-history line, the
   engagement's Notes line — and shift the engagement's End Date when the moved session
   is its last).
   The cascade also reaches outside the session's own artifacts: the message that triggered
   the reschedule (their cancellation email, your reply) is a point-person touchpoint, so the
   client's CRM record moves too — `Last Contact?` to the message date, and `Next Contact` to
   the new session date once confirmed, or to the reply-chase date while it isn't. The CRM
   Notes field stays untouched for routine moves; add a line only when something
   relationship-level rode along (a payment offer waived, an expansion signal). Route the
   update through `crm`.
   **When the event type has a matching SOP, that SOP is
   the highest-priority source** — read its Setup / reschedule-handling section and let it
   override these defaults for that event type (e.g. whether a completed `Precall` shifts or
   instead spawns a fresh task). Ad hoc events with a paired page but no SOP (e.g. a one-off
   call) fall back to the general defaults above. Discovery calls follow the same Workflow 7
   carve-out as Step 3.5 — hand the Notion-side cascade off there.
4. **Execute the cascade.** Route through the right specialist for each piece: paired-page
   `Date` and dated-task shifts through `notion-helper`; engagement-body session-line updates
   through `engagements` workflow-3-link-session's "Handle reschedules"; CRM record dates and
   Notes through `crm`; reschedule emails
   (usually unnecessary — the calendar invite handles it; send only when the SOP calls for
   it or the new time is within 24h) through `email-helper`, on the live thread.
5. **Report back** with the updated event and every artifact that moved (or note that no
   paired page exists / no SOP applies).

---

## Deleting an Event

When Shaw asks to cancel or delete an event ("cancel my call with Y", "delete the workshop
on Friday", "drop tomorrow's training"):

1. **Find the event** the same way as for reschedule.
2. **Confirm before deleting** if the event has external attendees — they'll get a
   cancellation email. For solo blocks, delete without asking.
3. **Delete** with `delete_event`, sending `ALL` notifications if there are external
   attendees.
4. **Hand off to `notion-helper`** to archive the corresponding Notion page (flip the icon
   to `🗑️` or move it to an archive — `notion-helper` will know the right convention).
5. **Report back** with confirmation.

---

## Defaults When No Reference Exists

If Step 2 finds nothing, the skill is operating without a template. Use these defaults:

- **Duration** — ask if it's an external meeting; default to 60 min for solo work blocks
- **Notification level** — `ALL` if attendees exist, `NONE` otherwise
- **Google Meet** — on if attendees exist, off otherwise
- **Color** — leave default (no `colorId`)
- **Description** — empty

When using defaults, mention it in the report: "no reference event found — used defaults".
That tells Shaw to double-check.

---

## Picking times to propose

Before picking times, decide whether to propose specific times at all. **The default is to send the appropriate Calendly link** — see email-helper's "Calendly Links and When to Use Them." Only fall back to manually proposed times when the recipient is a senior leader, exec, or busy person who'd treat a Calendly click as friction.

When manual proposal is the right call, don't just offer a generic afternoon window. Pull up the relevant days, look at what's already booked, and cluster proposed times around those anchors. Scattered meetings across an empty day cost more focus than a tight 3-call block.

**Principles:**

- **Cluster, don't scatter.** Pick times adjacent to existing meetings on that day. If an anchor exists at 12–1:30 PM, propose 2 PM next — not 4 PM with empty space between them. Booking calls close to each other is the point: awkward gaps between calls cost more focus than the calls themselves.

- **Back-to-back is fine up to ~90 minutes.** Short stacks are efficient. Once the existing block hits or exceeds 90 minutes, leave a 30-min buffer before adding another call so Shaw isn't stuck on calls for hours straight.

- **Buffer by call type, not duration.** Sales calls, check-ins, wrap-ups, and other higher-stakes conversations get a 30-min buffer after them — they often run long, and Shaw usually needs immediate post-call work time. Coffee chats, casual catch-ups, and low-priority calls can stack back-to-back with no buffer.

- **Empty days get a default spread.** When a day has no anchor meetings, fall back to a compact mid-afternoon window (e.g., 2/3/4 PM) rather than offering the entire 12–5 block.

- **Respect Shaw's day shape.** Before 10 AM CT is sacred focus time — never propose it. Exception: when the recipient's known time zone doesn't allow a slot after 10 AM. From 10 AM onward, any slot is fair game: rank candidates by the other principles here (clustering, buffers), not by time of day. (This supersedes an earlier 8 AM–1 PM focus block + midday-break rule — Shaw confirmed 10 AM is the only protected line.)

- **Re-offer the time of day that already worked.** When rescheduling, the call already had a time both sides agreed to, so include that slot's time of day among the options on the new day whenever it's open — e.g., a 10 AM call that moves keeps 10 AM as one of the proposed times. The same logic extends to anyone Shaw has met with before: when proposing new times to them, include the time-of-day of the last meeting with that person — a slot that already worked once needs no negotiating. (This is the general form of email-helper's coffee-chat anchoring note.)

- **Narrow to the three best options.** After applying the principles above, propose the three strongest times, not every open slot. More than three turns an easy reply into a decision. Rank by fit (cluster + day-shape + original-slot match) and offer the top three.

Once times are picked, invoke the `email-helper` skill to draft the email — don't reach for `create_draft` directly. This applies to *any* email that comes out of a calendar-helper workflow (time proposals, reschedule notices, post-create follow-ups), not just time-proposal emails. email-helper owns voice, HTML formatting, threading, and Gmail mechanics; calendar-helper stays in charge of the scheduling decision.

---

## Notion Database Reference

Pulled from `notion-helper` for convenience. If these IDs need updating, update them in
`notion-helper/SKILL.md` (the canonical source) first.

| DB | Database Page ID | Data Source ID | Purpose |
|---|---|---|---|
| ABA Calls | `[page-id]` | `[page-id]` | Sales call pages — discovery, intro, qualifier |
| ABA Trainings | `[page-id]` | `[page-id]` | Delivery sessions — 1:1s, workshops, ongoing engagements |
| Engagements | `[page-id]` | `[page-id]` | Won-deal project ledger — one row per invoice. Linked from ABA Trainings sessions via Step 4.5. |

Use the data source ID when calling `notion-create-pages`.

---

## Edge Cases

**Ambiguous attendee name** — a bare first name could match multiple people. Search calendar for past
events with anyone by that name; if there's exactly one frequent match, use it. If there
are multiple, ask via `AskUserQuestion` and offer the top 2-3 by recency.

**Multiple reference events with conflicting patterns** — last 3 sessions were 60 / 90 / 60
min. Don't average; ask Shaw which to match.

**Recurring events** — phrases like "every other Tuesday", "weekly", "monthly" → set
`recurrenceData` with the appropriate `RRULE`. Confirm the recurrence interpretation in
the report.

**All-day events** — "block off Friday for offsite" → set `allDay: true` and use UTC
midnight times.

**Different time zones** — default to `America/Chicago` (Shaw's tz). Only deviate if Shaw
specifies or the attendee is clearly in another zone and the time is ambiguous.

**Reference event description contains an outdated link** — if the description includes a
link to the *previous* session's Notion page, the copied description will point at the
wrong place. For now, copy verbatim and let Shaw fix it. (Future iteration: detect and
swap the link.)

---

## Quick Reference: Tools

Assume these tools are loaded via `tool_search` before first use.

**Calendar (Google Calendar MCP):**

| Need | Tool |
|---|---|
| Find past events | `list_events` |
| Get a specific event by ID | `get_event` |
| Create an event | `create_event` |
| Reschedule / update an event | `update_event` |
| Delete an event | `delete_event` |
| Suggest open times | `suggest_time` |

**Notion:**

| Need | Tool |
|---|---|
| Find pages by keyword | `notion-search` |
| Create a page in ABA Calls / ABA Trainings | `notion-create-pages` |
| Read a page | `notion-fetch` |

For reschedule and delete, hand updating/archiving the Notion page off to `notion-helper`
rather than calling `notion-update-page` directly — `notion-helper` owns that convention.

---

## Rules and Preferences

- **Default time zone is `America/Chicago`** unless the user or context says otherwise
- **Default notification level is `ALL` for events with attendees, `NONE` otherwise** — Shaw
  wants attendees to know about new/changed events. On an update, notify only when the
  meeting itself changes for the guest (time, attendees, Meet link); a title or description
  edit takes `NONE`, since an email about a change that doesn't affect them is noise
- **Include a Google Meet URL when attendees exist** unless the reference event didn't have
  one or the meeting runs on another platform (e.g. Zoom). The connector can attach Meet but
  not detach it, so create a non-Meet event without Meet rather than converting it afterward;
  converting an existing invite means removing Meet in the Calendar UI
- **Share event links scoped to the business account** — when giving Shaw a calendar event
  link, insert the `/u/1/` account-index path so it opens his business account
  (shaw@aibuilder.academy): `https://www.google.com/calendar/u/1/event?eid=<eid>`. The raw
  `htmlLink` returned by `create_event` omits the index and can open the wrong account. This
  mirrors the Gmail u/1 convention — see email-helper's "Gmail accounts and the u/ path" for
  what the index means.
- **Don't create ABA Calls pages for discovery calls** — Calendly-sourced discovery-call
  intake is owned by CRM Workflow 7, which creates the ABA Calls page (via `meeting-prep`)
  along with the CRM record, FU task, and confirmation email. calendar-helper creates the
  calendar event and hands the Notion side off. Non-discovery sales calls still get a paired
  ABA Calls page.
- **Let the matching event-type SOP define the paired page and the rest of Setup** — body
  contents (typically a CRM link line), FU task, bidirectional CRM linking, engagement linking.
  Half-executing the SOP (creating only the page) is the bug Step 3.5 exists to prevent.
- **Mirror the reference, don't reinvent** — if the reference event has a quirk (specific
  color, weird notification setting, custom description), preserve it
- **Mirror structure, not state** — a reference page shows you the shape (sections, title
  format, which properties are set); it does not tell you what state a *new* page starts in.
  Status-carrying fields — icon, Status, checkboxes, completion markers — come from the spec,
  not from the reference. Copying `✅` off a finished task onto a fresh one is the failure
  mode: the reference was ✅ because it was done, and the new task isn't.
- **Hand off, don't duplicate** — for Notion updates on reschedule/delete, route through
  `notion-helper`. For prep notes, route through `meeting-prep`. For lead pipeline
  updates and discovery-call intake, route through `crm` (Workflow 7 for discovery calls).
  For linking sessions/calls into active engagement bodies, route through `engagements`
  (workflow-3-link-session).

