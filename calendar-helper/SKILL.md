---
name: calendar-helper
description: >
  Create, reschedule, and delete events on Shaw's Google Calendar — and keep the matching Notion
  page in sync when one exists. Use this skill whenever Shaw wants to put something on the
  calendar, move an existing event, or cancel one. Triggers include: "schedule X", "create an
  event for", "put X on my calendar", "book a call with Y next Tuesday", "set up a 1:1 with",
  "another session with X next Saturday", "follow-up call with X", "reschedule the X meeting",
  "move my X call to Friday", "cancel the X event", "delete that meeting", or any casual
  phrasing that implies adding/changing a calendar block (e.g., "let's do another one with
  Justin", "block off Wednesday morning for the workshop"). Even when Shaw doesn't say
  "calendar" explicitly, this skill should fire if the request is about scheduling. This skill
  also creates a paired Notion page in ABA Calls or ABA Trainings when the event is a sales
  call or a delivery session and a paired page is part of the existing pattern.
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
- Reschedule and delete events, then hand the corresponding Notion page off to `notion-helper`

**Doesn't:**
- Build rich event descriptions from Gmail/Notion context (planned for a later iteration —
  for now, just copy the reference event's description verbatim if it has one)
- Create Notion pages for events outside the sales-call / training pattern (personal events,
  internal blocks, dentist appointments, etc. stay calendar-only)
- Manage Notion pages for non-create operations directly — those hand off to `notion-helper`
- Take over for `crm`, `pre-call-research`, `executive-briefing`, or `notion-helper` when the
  request is really about one of those

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

- **Attendee + topic** is the strongest signal. E.g., for "another session with Justin", search
  for past events with Justin's email on the attendee list.
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
- **Description** (copy verbatim if present; leave blank if not)

### Step 3 — Check Notion for a paired page

This step matters **only for sales calls and trainings**. Skip Notion entirely for other
event types.

Use `notion-search` to look for a Notion page that pairs with the reference calendar event.
Search the most likely database first based on event type:

| Calendar event type | Notion database | Database page ID |
|---|---|---|
| Sales call (discovery, intro, qualifier) | `ABA Calls` | `[page-id]` |
| Training / delivery / workshop / 1:1 session | `ABA Trainings` | `[page-id]` |

Search query: combine attendee name + topic keywords (e.g., "[Person] skill building"
or "[Person] training session"). Look at the top 1-3 matches and pick the one whose title most
closely mirrors the calendar event's title pattern.

**Decision rule:**
- **Reference event has a paired Notion page** → the new event needs one too. Note the
  database; you'll create the new page in Step 4.
- **Reference event has no paired Notion page** → the new event doesn't need one either.
  Mirror the existing pattern.
- **No reference event found at all, but the request is clearly a sales call or training**
  → default to creating a paired page in the matching database. (Surface this in Step 5
  if you're not sure of the type.)

### Step 4 — Build the event (and the page, if needed)

Compose the calendar event using the defaults from Step 2, with the request overriding
where it explicitly differs (e.g., user said "noon" → use noon, not the reference time).

If a Notion page is needed (per Step 3), construct a page with:
- **Title** matching the calendar event's title pattern (or a slightly trimmed version that
  matches the database's existing naming convention — sample 2-3 recent pages in that
  database to confirm)
- **Date** property set to the calendar event's date
- **Empty body** — no content, no template fill, no imagined notes
- **Same database** as the reference page

### Step 5 — Confirm or create

**Default behavior: create then report.** If the request is unambiguous (clear attendee,
clear date, clear reference event, clear Notion pairing), just do it. Then report back with:
- The created event (link, time, attendees, Meet URL)
- The created Notion page (link), if one was created
- One sentence noting which reference event/page was used

**Surface ambiguity via `AskUserQuestion`** when:
- Multiple attendees match the name (which Justin?)
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
- `[Person] / Shaw - 1:1 Skill Building (Session 1)` → `(Session 2)`
- `LFC Recording — Episode 12` → `Episode 13`
- `Cohort 3 Workshop, Week 4` → `Week 5`
- `ABN Issue #47` → `#48`

If the pattern increments, use the incremented title. If the pattern doesn't increment (a
generic recurring meeting like "Weekly Sync"), reuse the same title.

When you can't tell whether the user wants the next number in a sequence vs. a one-off,
default to incrementing — that's almost always what Shaw means when he says "another one"
or "next session".

**Spaces around `/` and `x` separators.** When a title joins two names with `/` or `x`,
always include surrounding spaces: `[Person] / Shaw – Catch-up`, never `[Person]/Shaw`. Same for
`x` collabs: `[Person] x Shaw`, never `[Person]xShaw`. This applies to any new title composition;
when mirroring an existing reference event, preserve its exact format.

---

## Rescheduling an Event

When Shaw asks to move an event ("move my call with Y to Thursday", "push the training to
next week", "reschedule X for 3pm"):

1. **Find the event** with `list_events` (filter by attendee, title keyword, or date range).
   If multiple match, ask via `AskUserQuestion`.
2. **Update the event** with `update_event` — change `startTime` / `endTime`, keep everything
   else (attendees, Meet URL, description).
3. **Hand off to `notion-helper`** to update the corresponding Notion page's `Date` property.
   Pass `notion-helper` the page ID (you found it in Step 3 of the create flow, or search
   for it now using the same logic) and the new date.
4. **Report back** with the updated event + a note that the Notion page was updated (or
   that no paired page exists).

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
- **Notion pairing** — only create a page if the user explicitly asks ("schedule a sales
  call with X and add it to ABA Calls"), or if the topic is unambiguously a sales call or
  training and the user hasn't said otherwise

When using defaults, mention it in the report: "no reference event found — used defaults".
That tells Shaw to double-check.

---

## Notion Database Reference

Pulled from `notion-helper` for convenience. If these IDs need updating, update them in
`notion-helper/SKILL.md` (the canonical source) first.

| DB | Database Page ID | Data Source ID | Purpose |
|---|---|---|---|
| ABA Calls | `[page-id]` | `[page-id]` | Sales call pages — discovery, intro, qualifier |
| ABA Trainings | `[page-id]` | `[page-id]` | Delivery sessions — 1:1s, workshops, ongoing engagements |

Use the data source ID when calling `notion-create-pages`.

---

## Edge Cases

**Ambiguous attendee name** — "Justin" could be multiple people. Search calendar for past
events with anyone named Justin; if there's exactly one frequent match, use it. If there
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

**Notion (only for sales calls and trainings):**

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
  wants attendees to know about new/changed events
- **Always include a Google Meet URL when attendees exist** unless the reference event
  explicitly didn't have one
- **Never create a Notion page for an event that isn't a sales call or training** — even if
  Shaw seems excited about the meeting, the rule holds
- **Title-only Notion pages by default** — the body stays empty; Shaw fills it in himself
  when he preps for the session
- **Mirror the reference, don't reinvent** — if the reference event has a quirk (specific
  color, weird notification setting, custom description), preserve it
- **Hand off, don't duplicate** — for Notion updates on reschedule/delete, route through
  `notion-helper`. For prep notes, route through `pre-call-research`. For lead pipeline
  updates, route through `crm`.
