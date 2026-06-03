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

Shaw organizes his work across several Notion databases. The first six are dated work
databases — pages with a `Date` property, scheduled for the day Shaw wants to act on them.
The last three are relationship databases (Active Leads, Clients (Nurture), Testimonials)
where each page has a `Next Contact` field; the briefing surfaces rows whose next touch is
due. Together they form a single daily picture of what's on Shaw's plate.

The briefing is a snapshot of what's due now — not a project management tool. No overdue
items from prior days, no upcoming items beyond today's window, no backlog.

---

## Databases in Scope

The canonical database catalog (IDs, icons, descriptions, and view URLs) lives in
`notion-helper/SKILL.md` under "Main Databases" and "Today Views (executive-briefing)."
This skill queries **all main databases listed there**:

Dated work:

- 🎓 **ABA** — tasks, launches, outreach, partnerships, events
- 🏫 **ABA Trainings** — delivery sessions (1:1 workshops, trainings, ongoing engagements)
- 👨‍🏫 **ABA Calls** — sales calls (notes, prep, scheduling)
- 📹 **LFC** — YouTube videos
- 📅 **SFC** — LinkedIn posts, YT community posts, social shares
- 🗞️ **ABN** — newsletter editions, email blasts

Follow-ups due (filtered by `Next Contact`):

- 💼 **Active Leads** — pipeline rows where the next touch is due
- 🌱 **Clients (Nurture)** — active/nurturing client check-ins coming up
- ⭐ **Testimonials** — testimonial asks where the next nudge is due

If a new database is added, update `notion-helper/SKILL.md` and it will flow through here
automatically.

---

## Workflow

### Step 1: Query all databases

Use `notion-query-database-view` on each view URL listed in `notion-helper/SKILL.md` →
"Today Views (executive-briefing)." Each view is filtered server-side, so the result set
is already the items you need — no client-side date filtering required. Run all nine
queries in parallel in a single tool-call batch.

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
- For Active Leads: status (Booked Call, Outline Sent, etc.) and the most recent Note line
  so the next step is obvious
- For Clients (Nurture): status (Active, Nurturing, Expansion) and the most recent Note line
  — what's the next touch
- For Testimonials: status (Asked, Form Submitted, Approved) and what's owed (FU nudge,
  polish quote, publish, etc.)

The relationship-database rows (Active Leads, Clients (Nurture), Testimonials) often have
rich `Notes` columns in the query response itself — use those directly rather than fetching
each page, unless the row needs deeper context.

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

**💼 Active Leads**
- [**Lead name**](https://www.notion.so/page-id) — Status; next step from Notes.

**🌱 Clients (Nurture)**
- [**Client name**](https://www.notion.so/page-id) — Status; next touch from Notes.

**⭐ Testimonials**
- [**Person name**](https://www.notion.so/page-id) — Status; what's owed.
```

---

## Output Rules

- Only items due today (dated work + follow-ups whose Next Contact has arrived) — no
  overdue items from prior days, no upcoming items beyond today's window, no backlog
- Every section appears even if empty — show "Nothing scheduled for today." for empty sections
- Each item name is bold and linked to its Notion page URL
- Completed items (page icon ✅) get a ✅ prefix before the linked name; all others have no prefix
- Descriptions are 1-2 sentences max, pulled from the actual page content
- Keep the section order consistent: ABA → ABA Trainings → ABA Calls → LFC → SFC → ABN →
  Active Leads → Clients (Nurture) → Testimonials (dated work first, then follow-ups)
- No commentary, no prioritization advice, no suggestions — just the facts
- No widget/visualization — plain text only
