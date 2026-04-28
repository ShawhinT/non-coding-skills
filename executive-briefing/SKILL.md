---
name: executive-briefing
description: >
  Generate Shaw's daily executive briefing by pulling today's tasks from his main Notion databases.
  Use this skill whenever Shaw asks for his daily briefing, rundown, what's on his plate, what he has
  going on today, or anything about reviewing his scheduled tasks for the day. Triggers include:
  "give me my briefing", "what do I have today", "daily rundown", "executive briefing", "what's on
  my plate", "what's scheduled today", "morning briefing", "what am I working on today", or any
  reference to checking tasks across his Notion databases. Even casual mentions like "what's today
  look like" or "run me through my day" should trigger this skill.
---

# Executive Briefing Skill

Shaw organizes his work across several Notion databases. Each uses a calendar/date view —
items are pages with a Date property, and Shaw schedules work by assigning dates to pages.
This skill pulls all items dated for today and presents a concise briefing.

The briefing is a snapshot of what Shaw has scheduled — not a project management tool. It only
shows items dated for today. No overdue items, no upcoming items, no backlog.

---

## Databases in Scope

The canonical database catalog (IDs, icons, descriptions, and view URLs) lives in
`notion-helper/SKILL.md` under "Main Databases" and "Today Views (executive-briefing)."
This skill queries **all main databases listed there**:

- 🎓 **ABA** — tasks, launches, outreach, partnerships, events
- 🏫 **ABA Trainings** — delivery sessions (1:1 workshops, trainings, ongoing engagements)
- 👨‍🏫 **ABA Calls** — sales calls (notes, prep, scheduling)
- 📹 **LFC** — YouTube videos
- 📅 **SFC** — LinkedIn posts, YT community posts, social shares
- 🗞️ **ABN** — newsletter editions, email blasts

If a new database is added, update `notion-helper/SKILL.md` and it will flow through here
automatically.

---

## Workflow

### Step 1: Query all databases

Use `notion-query-database-view` on each view URL listed in `notion-helper/SKILL.md` →
"Today Views (executive-briefing)." Each view is filtered server-side to today's date,
so the result set is already the items you need — no client-side date filtering required.
Run all six queries in parallel in a single tool-call batch.

### Step 2: Fetch page content for each matching item

For each returned item, use `notion-fetch` with the page URL/ID to pull the page content.
This gives you the context needed to write a useful 1-2 sentence description. Fetch all
pages in parallel.

Also extract the page's `icon` attribute from the `<page>` tag in the fetch response
(e.g., `<page url="..." icon="✅">`). Shaw uses ✅ as the page icon to mark completed
tasks. If the icon is ✅, prepend it before the linked task name in the output. For any
other icon (or no icon), display the item normally with no prefix.

When summarizing page content:
- For ABA tasks: describe the specific action or deliverable
- For ABA Trainings: include the participant's name, session type (1:1 workshop, training,
  etc.), and any key context from session notes or prior prep
- For ABA Calls: include who the call is with, their company/role, and any key context
  from call notes or pre-call research
- For LFC items: describe the video topic and current stage (outline, scripting, filming, etc.)
- For SFC items: describe the post topic and whether draft copy exists
- For ABN items: describe the newsletter edition or email task

### Step 3: Present the briefing

Output as plain text, organized by database section. Format:

```
**🎓 ABA**
- [**Item name**](https://www.notion.so/page-id) — Brief context from page content.
- ✅ [**Item name**](https://www.notion.so/page-id) — Brief context from page content.

**🏫 ABA Trainings**
- [**Participant name**](https://www.notion.so/page-id) — Session type and key context.

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
- Completed items (page icon ✅) get a ✅ prefix before the linked name; all others have no prefix
- Descriptions are 1-2 sentences max, pulled from the actual page content
- Keep the section order consistent: ABA → ABA Trainings → ABA Calls → LFC → SFC → ABN
- No commentary, no prioritization advice, no suggestions — just the facts
- No widget/visualization — plain text only
