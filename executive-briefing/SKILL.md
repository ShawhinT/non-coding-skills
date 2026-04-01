---
name: executive-briefing
description: >
  Generate Shaw's daily executive briefing by pulling today's tasks from his five Notion databases.
  Use this skill whenever Shaw asks for his daily briefing, rundown, what's on his plate, what he has
  going on today, or anything about reviewing his scheduled tasks for the day. Triggers include:
  "give me my briefing", "what do I have today", "daily rundown", "executive briefing", "what's on
  my plate", "what's scheduled today", "morning briefing", "what am I working on today", or any
  reference to checking tasks across his Notion databases. Even casual mentions like "what's today
  look like" or "run me through my day" should trigger this skill.
---

# Executive Briefing Skill

Shaw organizes his work across five Notion databases. Each database uses a calendar/date view —
items are pages with a Date property, and Shaw schedules work by assigning dates to pages. This
skill pulls all items dated for today and presents a concise briefing.

The briefing is a snapshot of what Shaw has scheduled — not a project management tool. It only
shows items dated for today. No overdue items, no upcoming items, no backlog.

---

## The Five Databases

| DB | Full Name | Notion Database ID | What Lives Here |
|---|---|---|---|
| 🎓 ABA | AI Builder Academy | `2f35f2e2-6be9-8038-a5f9-f3bba90f9289` | Main business tasks — launches, outreach, partnerships, website, events |
| 🗞️ ABN | AI Builder Newsletter | `16d5f2e2-6be9-8060-bdd8-cd1b3bc49fe3` | Newsletter editions, email blasts, list management |
| 📹 LFC | Long Form Content | `3bfeb063-56ee-4caf-873f-7de4bf36c609` | YouTube videos — scripting, filming, editing, uploads |
| 📅 SFC | Short Form Content | `e8ab6a81-dd97-4598-8856-ff16c0d1eb78` | LinkedIn posts, YT community posts, social shares |
| 👨‍🏫 ABA Calls | ABA Calls | `1f25f2e2-6be9-804f-847b-d26f36563dd0` | Sales calls — notes, prep, scheduling |

### View URLs for Querying

Each database has a table view that returns all items. Use these view URLs with the
`notion-query-database-view` tool:

| DB | View URL |
|---|---|
| ABA | `https://www.notion.so/2f35f2e26be98038a5f9f3bba90f9289?v=2f35f2e2-6be9-80e8-873c-000cc04fe3e6` |
| ABN | `https://www.notion.so/16d5f2e26be98060bdd8cd1b3bc49fe3?v=16d5f2e2-6be9-8156-a62d-000c73451f2b` |
| LFC | `https://www.notion.so/3bfeb06356ee4caf873f7de4bf36c609?v=2b45f2e2-6be9-809a-bcf1-000c2098a58c` |
| SFC | `https://www.notion.so/e8ab6a81dd9745988856ff16c0d1eb78?v=eb7cdd71-e01b-459f-a1b7-ce2ea120cc07` |
| ABA Calls | `https://www.notion.so/1f25f2e26be9804f847bd26f36563dd0?v=1f25f2e2-6be9-8106-b4ed-000cdda401de` |

### Date Field

All five databases use a `Date` property. The date field in query results appears as
`date:Date:start` in ISO format (e.g., `2026-03-31`). Filter results by matching this
field to today's date.

---

## Workflow

### Step 1: Query all five databases

Use `notion-query-database-view` on each of the five view URLs above. This returns all items
in each database with their dates and names.

### Step 2: Filter for today

From each result set, keep only items where `date:Date:start` equals today's date
(ISO format, e.g. `2026-03-31`). Discard everything else.

### Step 3: Fetch page content for each matching item

For each item dated today, use `notion-fetch` with the item's page URL/ID to pull the page
content. This gives you the context needed to write a useful 1-2 sentence description.

When summarizing page content:
- For ABA tasks: describe the specific action or deliverable
- For ABA Calls: include who the call is with, their company/role, and any key context
  from call notes or pre-call research
- For LFC items: describe the video topic and current stage (outline, scripting, filming, etc.)
- For SFC items: describe the post topic and whether draft copy exists
- For ABN items: describe the newsletter edition or email task

### Step 4: Present the briefing

Output as plain text, organized by database section. Format:

```
**🎓 ABA**
- [**Item name**](https://www.notion.so/page-id) — Brief context from page content.
- [**Item name**](https://www.notion.so/page-id) — Brief context from page content.

**👨‍🏫 ABA Calls**
- [**Person name**](https://www.notion.so/page-id) — Key context from call notes.

**📹 LFC**
- [**Video title**](https://www.notion.so/page-id) — Topic and current stage.

**📅 SFC**
- [**Post title**](https://www.notion.so/page-id) — Post topic and draft status.

**🗞️ ABN**
- Nothing scheduled for today.
```

---

## Output Rules

- Only items dated for today — no overdue, no upcoming, no backlog
- Every section appears even if empty — show "Nothing scheduled for today." for empty sections
- Each item name is bold and linked to its Notion page URL
- Descriptions are 1-2 sentences max, pulled from the actual page content
- Keep the section order consistent: ABA → ABA Calls → LFC → SFC → ABN
- No commentary, no prioritization advice, no suggestions — just the facts
- No widget/visualization — plain text only
