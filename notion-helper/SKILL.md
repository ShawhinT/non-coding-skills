---
name: notion-helper
description: >
  Navigate Shaw's Notion workspace and create ad hoc tasks, follow-ups, and reminders across his
  databases and pages. Use this skill whenever Shaw asks to add a task, schedule a follow-up,
  create a reminder in Notion, add something to his plate for a specific day, drop a note into
  one of his databases, or find/reference pages in his workspace. Triggers include: "add a task
  for X", "create a FU for tomorrow", "put this on my plate for Monday", "add this to ABA",
  "remind me to follow up with X in Notion", "make a note in Notion to…", "find me the page
  about X", "link the call page to Y", or any ad hoc Notion
  creation/navigation that isn't already covered by a more specific skill (CRM, executive
  briefing, SOPs, etc.). Also trigger when Shaw asks to create follow-up tasks after calls,
  workshops, or meetings — those belong in ABA as dated task pages. Even casual mentions like
  "throw a reminder in Notion" or "add this to my list for Friday" should trigger this skill.
---

# Notion Helper Skill

Shaw's general-purpose Notion assistant. Use this skill for ad hoc Notion work that doesn't fall
under a more specialized skill — creating tasks, follow-ups, and notes in his databases, adding
reference pages, and navigating his workspace to find and link related content.

This skill is Notion-only. It does NOT create iOS Reminders, calendar events, or anything
outside Notion. If Shaw needs a cross-system action, another skill (or tool) handles that part.

---

## How Shaw Organizes Work in Notion

Shaw schedules his work as **dated pages** in a handful of main databases. He assigns a `Date`
property to each page to indicate the day he wants to *act* on it — the page then shows up in
his daily briefing for that date. Most task pages are simple (title + date), with optional body
content when context or next steps are needed.

**This skill is the canonical catalog of Shaw's Notion databases.** Other skills (`crm`,
`executive-briefing`, `pre-call-research`, etc.) should reference this section rather than
duplicating IDs, so updates only need to happen in one place.

### Main Databases

| DB | Icon | Database Page ID | Data Source ID | What Lives Here |
|---|---|---|---|---|
| ABA | 🎓 | `[page-id]` | `[page-id]` | Main business tasks — launches, outreach, partnerships, events, follow-ups |
| ABA Trainings | 🏫 | `[page-id]` | `[page-id]` | Delivery sessions — 1:1 workshops, trainings, ongoing engagements |
| ABA Calls | 👨‍🏫 | `[page-id]` | `[page-id]` | Sales calls — notes, prep, scheduling |
| ABN | 🗞️ | `[page-id]` | `[page-id]` | Newsletter editions, email blasts, list management |
| LFC | 📹 | `[page-id]` | `[page-id]` | YouTube videos — scripting, filming, editing, uploads |
| SFC | 📅 | `[page-id]` | `[page-id]` | LinkedIn posts, YT community posts, social shares |
| Active Leads | 💼 | — | `[page-id]` | Pipeline rows — leads being actively worked. Lives under CRM page; handled by `crm`. Read-only for `executive-briefing` (surfaces rows whose `Next Contact` is due) |
| Clients (Nurture) | 🌱 | — | `[page-id]` | Active / nurturing / expansion clients. Lives under CRM page; handled by `crm`. Read-only for `executive-briefing` (surfaces rows whose `Next Contact` is due) |
| Testimonials | ⭐ | — | `[page-id]` | Testimonial workflow (Not Asked → Asked → Form Submitted → Approved → Published). Handled by `testimonials`. Read-only for `executive-briefing` (surfaces rows whose `Next Contact` is due) |

The six dated work databases (ABA, ABA Trainings, ABA Calls, ABN, LFC, SFC) use a `Date`
property. For task pages, the expanded property is `date:Date:start` (ISO format, e.g.
`2026-04-17`) and `date:Date:is_datetime` (0 for date-only). The three relationship databases
(Active Leads, Clients (Nurture), Testimonials) use `Next Contact` instead — expanded as
`date:Next Contact:start`.

### Default View URLs

Used by `notion-query-database-view` to pull every item in a database — useful when you
need to scan the whole database or apply your own filters in code:

| DB | View URL |
|---|---|
| ABA | `https://www.notion.so/[page-id]?v=[page-id]` |
| ABA Trainings | `https://www.notion.so/[page-id]?v=[page-id]` |
| ABA Calls | `https://www.notion.so/[page-id]?v=[page-id]` |
| ABN | `https://www.notion.so/[page-id]?v=[page-id]` |
| LFC | `https://www.notion.so/[page-id]?v=[page-id]` |
| SFC | `https://www.notion.so/[page-id]?v=[page-id]` |

### Today Views (executive-briefing)

Filtered server-side: the dated-work views (ABA → ABN) filter on `Date is Today`; the
relationship views (Active Leads, Clients (Nurture), Testimonials) filter on `Next Contact`
being due. Used by the `executive-briefing` skill so each query returns only what's owed
right now — no client-side date filtering needed. The filters are relative and update
automatically each day.

| DB | View URL |
|---|---|
| ABA | `https://www.notion.so/[page-id]?v=[page-id]` |
| ABA Trainings | `https://www.notion.so/[page-id]?v=[page-id]` |
| ABA Calls | `https://www.notion.so/[page-id]?v=[page-id]` |
| LFC | `https://www.notion.so/[page-id]?v=[page-id]` |
| SFC | `https://www.notion.so/[page-id]?v=[page-id]` |
| ABN | `https://www.notion.so/[page-id]?v=[page-id]` |
| Active Leads | `https://www.notion.so/[page-id]?v=[page-id]` |
| Clients (Nurture) | `https://www.notion.so/[page-id]?v=[page-id]` |
| Testimonials | `https://www.notion.so/[page-id]?v=[page-id]` |

### Other Key Pages

| Page | Page ID | When to Use |
|---|---|---|
| CRM | `[page-id]` | Parent hub page for the Active Leads + Clients (Nurture) databases. Updates handled by the `crm` skill — don't duplicate that work here |
| SOPs | `[page-id]` | Standard operating procedures; handled by the `sop-helper` skill — don't duplicate that work here |
| ABA (Master) | `[page-id]` | Parent page for the ABA database and related resources |
| ABA Trainings (Hub) | `[page-id]` | Hub page under ABA Master grouping all training/delivery sessions |
| Campaigns | `[page-id]` | Parent page under ABA (Master) for per-campaign pages (e.g. event promos). Each campaign page carries its own campaign-local databases (e.g. a Promo Calendar) — fetch the campaign page to get their `collection://` data source IDs rather than hardcoding them |

### Event-Type SOPs

Event-type SOPs live as child pages under the SOPs page (`[database-id]`) — the one ID worth hardcoding, since it's the stable entry point. **Don't hardcode the individual SOP IDs.** They drift as SOPs are added, split, or renamed. Instead, `fetch` the SOPs page and read its child pages to get the current set and their live IDs, then match by title. Other skills (`crm`, `pre-call-research`, `email-helper`, `calendar-helper`) point here for *how to find* an SOP rather than carrying their own IDs.

What to expect on the SOPs page (titles, for orientation — confirm against the live page):

- **Acquisition** — Discovery Call, Testimonial Ask, Referral Ask, AI Rollout Audit Call, Event Series, Post Event
- **Delivery** — 1:1 Claude Workshop, Group Claude Workshop, Wrap-up Call, and the Check-in Call family: **Check-in Call** (shared base — Setup, call bank, post-call mechanics) plus three spokes carrying the agenda + templates: **Check-in Call (1:1 Claude Workshop)** (post-session 4Rs), **Check-in Call (Client Nurture)** (periodic; 4Rs not forced), **Check-in Call (Lead Nurture)** (warm lead; no 4Rs)
- **Resources** — reference pages, not process SOPs (e.g. The 4Rs Framework, Hormozi frameworks); SOPs link to these instead of restating them

The call/session SOPs follow a consistent **Trigger → Setup → Pre-call research → Call → Post-call** structure; delivery/acquisition SOPs follow their own order. Creating or editing SOPs is `sop-helper`'s job, not this skill's.

---

## Core Workflow: Creating an Ad Hoc Task

Most requests are "add a task for X on [date]" or "create a FU for [person] [when]". For the
full step-by-step workflow — including title parsing, naming conventions, duplicate checks,
and the `notion-create-pages` payload — see `references/create-task-workflow.md`.

---

## Other Common Asks

### Creating a page in a database other than ABA

When Shaw names the database explicitly (e.g. "add to LFC", "put in SFC"), use that database's
data source ID. If the data source ID isn't in the table above, fetch the database page first
to get it from the `<data-source url="collection://...">` tag, then create.

### Mirroring campaign tasks into ABA

Campaign-local databases (like a Promo Calendar under a campaign page) don't feed the daily
briefing — only the main databases do. So when action items land in a campaign database and
Shaw needs to act on them day-to-day, mirror each one as a task copy in ABA: same title and
date, `⭕` icon, body containing just a `<mention-page>` link back to the campaign row. The
campaign database stays the campaign's source of truth; the ABA copy is what surfaces the work
in the briefing.

### Finding a page

Use `notion-search` with the content term. Don't search over just a person's name when the
target is specific content — include both (e.g., "[Name] workshop", not just "[Name]").
Return the top 1-3 most relevant results with links.

### Linking pages on an existing task

Fetch the page, then use `notion-update-page` with `command: "update_content"` and a
search-and-replace to inject `<mention-page url="..."/>` inline.

### Capturing a Kit/newsletter draft into an ABN page

When appending a newsletter draft (e.g. from Kit) to its dated ABN page, match Shaw's
layout — the page *is* the container, so don't wrap the draft in your own headings or labels:

- The source link the newsletter repurposes stays at the top, followed by a `---` divider.
  The source is often a LinkedIn post, but it can just as easily be a blog post, video, or any
  piece the newsletter is built from — label it for what it is (e.g. `Source blog: <title>`) so
  the origin is clear at a glance.
- **Subject + Preview** go together as one tight block, not two separate paragraphs:
  `**Subject**: "..."` then `<br>**Preview:** ...`.
- The newsletter body follows as written — mirror what actually shipped in Kit, don't re-edit
  it here. The CTA isn't always a P.S.; it's sometimes an inline line right before the signoff,
  so capture whatever the final draft used rather than forcing a P.S.
- Keep the signoff compact: `Keep building,<br>Shaw`.
- If the email closes on a trailing asset (e.g. a cheat-sheet image), keep it *after* the
  signoff, mirroring the email — the signoff isn't always the last element on the page.
- No section heading like "Latest Kit Draft" above the draft.

This is the ABN-specific instance of the general "match formatting from recent examples"
rule below — when in doubt, sample the last 1-2 ABN pages and mirror them.

### Marking a task done

Shaw tracks task status via the page icon: `⭕` = open, `✅` = done. Marking a task done
is just flipping the icon — no property or content change needed. The `executive-briefing`
skill reads the same convention on the other end to show completed items in the daily
briefing.

Use `notion-update-page` with `command: "update_properties"`, an empty `properties` object,
an empty `content_updates` array, and `icon: "✅"`. Example:

```json
{
  "page_id": "[page-id]",
  "command": "update_properties",
  "properties": {},
  "content_updates": [],
  "icon": "✅"
}
```

When Shaw asks to close out multiple tasks at once ("mark these all done"), fire the updates
in parallel — one tool call per page in a single message. Before doing so, confirm which pages
are in scope: "this one and the other follow-ups" usually means only the tasks already
discussed in the conversation, not every open task in the database. If in doubt, list the
pages you plan to flip and ask before proceeding.

## Page-Freshness Workflows

Batch-style workflows that keep dated pages current, the way `crm` keeps the pipeline current.
Run on-demand today ("link the recent transcripts"); each is written to be **idempotent** so it
can later run unattended on a schedule.

### Linking Meet transcripts to call pages

Google Meet auto-saves each call's transcript to Drive. This workflow attaches the transcript to
its matching ABA Calls (sales) or ABA Trainings (delivery) page, so the link lives on the page
and anything that reads the page later — `pre-call-research`, the daily briefing — picks it up
for free.

The *find* isn't this skill's job: it lives in `google-drive-helper` ("Find the transcript for a
call"). This workflow owns the **match + Notion write** — don't restate the Drive query here,
call it.

For each call page that needs a transcript (a single named call, or — for a batch run — recent
ABA Calls / ABA Trainings pages with no `## Transcript` link yet):
1. **Derive the key** — person/company name from the page title, date from the page's `Date`
   property.
2. **Find the transcript** via `google-drive-helper`. If it returns more than one for that day,
   disambiguate with the matching Google Calendar event's start time.
3. **Link it** — append a `## Transcript` line to the page body with the transcript's Drive
   `viewUrl` as a **plain external Markdown link** (`[Transcript](https://docs.google.com/document/d/...)`),
   *not* `<mention-page>` (that syntax is for internal Notion pages; a Google Doc isn't one). Use
   the `update_content` search-and-replace pattern from "Linking pages on an existing task".
4. **Stay idempotent** — skip any page that already has a `## Transcript` link. This is what makes
   a future scheduled run safe to repeat.
5. **Report** the pages linked, and surface any transcript with no confident page match (or any
   page whose transcript isn't in Drive yet) instead of guessing.

Only forward-looking calls have transcripts — transcription started May 2026, so pages before
that stay notes-only.

---

## Rules and Preferences

- **Default to ABA** for ad hoc tasks and FUs unless another database is clearly right
- **Keep titles short and action-first** — match Shaw's patterns (see `references/create-task-workflow.md`)
- **Match formatting from recent examples** — before creating, sample 2-3 recent pages of the
  same type to confirm current conventions (title style, suffix patterns, etc.)
- **Check for duplicates** — don't auto-create if a similar page already exists on the same
  date; surface it to Shaw first
- **Default icons by page type** — ABA task pages get `⭕` (open). Event/training pages
  (ABA Calls, ABA Trainings) get `⭐`. Pages in other databases (ABN, LFC, SFC) have no icon
  by default unless Shaw asks for one. `⭕` flips to `✅` when a task is done — see
  "Marking a task done".
- **Minimal body content** — default to just a link; add structure only when Shaw asks
- **Auto-link related pages** — if a person's name appears in the request, search and link their
  CRM + most recent call page
- **Use `<mention-page url="..."/>` syntax** for internal links (not Markdown `[text](url)`)
  — this creates a proper Notion page reference with the correct title
- **Notion-only** — don't create iOS Reminders, calendar events, or anything outside Notion.
  If Shaw needs those, he'll ask explicitly and a different skill handles it
- **Don't duplicate CRM work** — if the request is about updating a lead's status, notes, or
  pipeline stage, defer to the `crm` skill. This skill covers *ad hoc* task/page creation that
  sits alongside the CRM, not CRM updates themselves
- **Don't duplicate SOP work** — if the request is about creating, updating, or referencing a
  standard operating procedure, defer to the `sop-helper` skill
- **Don't duplicate briefing work** — if Shaw asks "what's on my plate today", that's the
  `executive-briefing` skill, not this one

---

## Quick Reference: Notion Tools

Assume these tools are loaded via `tool_search` before first use:

| Need | Tool |
|---|---|
| Find pages by keyword | `notion-search` |
| Read a page or database | `notion-fetch` |
| Create one or more pages | `notion-create-pages` |
| Edit a page's properties or content | `notion-update-page` |
| Query a database view (all items) | `notion-query-database-view` |
