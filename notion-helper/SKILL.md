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
| ABA | 🎓 | `[page-id]` | `[database-id]` | Main business tasks — launches, outreach, partnerships, events, follow-ups |
| ABA Trainings | 🏫 | `[page-id]` | `[database-id]` | Delivery sessions — 1:1 workshops, trainings, ongoing engagements |
| ABA Calls | 👨‍🏫 | `[page-id]` | `[database-id]` | Sales calls — notes, prep, scheduling |
| ABN | 🗞️ | `[page-id]` | (fetch to resolve) | Newsletter editions, email blasts, list management |
| LFC | 📹 | `[page-id]` | (fetch to resolve) | YouTube videos — scripting, filming, editing, uploads |
| SFC | 📅 | `[page-id]` | (fetch to resolve) | LinkedIn posts, YT community posts, social shares |

All databases use a `Date` property. For task pages, the expanded property is
`date:Date:start` (ISO format, e.g. `2026-04-17`) and `date:Date:is_datetime` (0 for date-only).

### Default View URLs

Used by `notion-query-database-view` to pull all items from a database (e.g. the executive
briefing filters these by today's date):

| DB | View URL |
|---|---|
| ABA | `https://www.notion.so/[page-id]?v=[view-id]` |
| ABA Trainings | `https://www.notion.so/[page-id]?v=[view-id]` |
| ABA Calls | `https://www.notion.so/[page-id]?v=[view-id]` |
| ABN | `https://www.notion.so/[page-id]?v=[view-id]` |
| LFC | `https://www.notion.so/[page-id]?v=[view-id]` |
| SFC | `https://www.notion.so/[page-id]?v=[view-id]` |

### Other Key Pages

| Page | Page ID | When to Use |
|---|---|---|
| CRM | `[page-id]` | Active Leads + Clients; handled by the `crm` skill — don't duplicate that work here |
| SOPs | `[page-id]` | Standard operating procedures; handled by the `sop-helper` skill — don't duplicate that work here |
| ABA (Master) | `[page-id]` | Parent page for the ABA database and related resources |
| ABA Trainings (Hub) | `[page-id]` | Hub page under ABA Master grouping all training/delivery sessions |

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

### Finding a page

Use `notion-search` with the content term. Don't search over just a person's name when the
target is specific content — include both (e.g., "[Person] workshop", not just "[Person]").
Return the top 1-3 most relevant results with links.

### Linking pages on an existing task

Fetch the page, then use `notion-update-page` with `command: "update_content"` and a
search-and-replace to inject `<mention-page url="..."/>` inline.

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

---

## Rules and Preferences

- **Default to ABA** for ad hoc tasks and FUs unless another database is clearly right
- **Keep titles short and action-first** — match Shaw's patterns (see `references/create-task-workflow.md`)
- **Match formatting from recent examples** — before creating, sample 2-3 recent pages of the
  same type to confirm current conventions (title style, suffix patterns, etc.)
- **Check for duplicates** — don't auto-create if a similar page already exists on the same
  date; surface it to Shaw first
- **Default icon: ⭕ for FU tasks, nothing otherwise** — any page whose title starts with `FU`
  (or "Follow up with") gets `⭕`. Other tasks have no icon unless Shaw asks for one. `⭕` means
  open and `✅` means done — marking a task done = flipping the icon (see "Marking a task done")
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
