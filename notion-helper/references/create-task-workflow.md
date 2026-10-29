# Create Task Workflow

Read this when creating a new task or follow-up page in one of Shaw's main databases. Most
requests are "add a task for X on [date]" or "create a FU for [person] [when]."

## Step 1: Parse the request

Extract:

- **Title** — short, action-oriented, matching Shaw's existing naming patterns (see below)
- **Date** — the day Shaw wants to act on it (resolve "tomorrow", "next Monday", etc. against
  today's date; use `user_time_v0` if unsure)
- **Database** — default to **ABA** unless Shaw explicitly names another or it's clearly a
  newsletter/video/social/call item
- **Related people or pages** — names mentioned in the request (e.g., "FU with [Person]" → auto-link
  [Person]'s CRM entry and most recent call page)

## Step 2: Match Shaw's naming conventions

Shaw's task titles are short, action-first, and follow recurring patterns:

| Pattern | Example |
|---|---|
| `FU - <Name>` | `FU - [Person 2]`, `FU - [Person 3]` |
| `Send <Name> <thing>` | `Send [Person] agenda + Call Prep`, `Send [Person 4] FU email` |
| `Follow up with <Name>` | `Follow up with [Person]`, `Follow up with speakers` |
| `Prep for <thing>` | `Prep for 1:1 Training (PM)` |
| `<Name> - <session type>` | `[Person] - Check-in`, `[Person 2] - 1:1 Claude Workshop` |
| `Reply <Name>` | `Reply [person 5]` |
| `<verb> <object>` | `Update website messaging`, `Test new ABA copy` |

Prefer these patterns over verbose titles. If Shaw says "remind me to follow up with [Person 3]
tomorrow," the title is `FU - [Person 3]`, not "Reminder: Follow up with [Person 3] tomorrow."

## Step 3: Find related pages to link

If the request mentions a person's name, search Notion for:

- Their CRM entry (Active Leads data source: `collection://[page-id]`
  or Clients: `collection://[page-id]`)
- Their most recent call page (ABA Calls) or delivery page (ABA Trainings)

Use `notion-search` with the person's name. Pick the most relevant hits — typically the CRM
entry plus the most recent call/session page.

## Step 4: Check for duplicates and sample formatting

Before creating, query the target database view to check for likely duplicates and to confirm
Shaw's current naming/formatting conventions. The old `notion-query-database-view` tool is
deprecated and no longer loads; use `notion-query-data-sources` instead — either in view mode
(`{"mode": "view", "view_url": ...}`) with the database's default (full-scan) view URL below, or,
cheaper for a date-targeted duplicate check, a SQL query on the data source filtering
`date("date:Date:start")` to the relevant range:

| DB | View URL |
|---|---|
| ABA | `https://www.notion.so/[page-id]?v=[page-id]` |
| ABA Trainings | `https://www.notion.so/[page-id]?v=[page-id]` |
| ABA Calls | `https://www.notion.so/[page-id]?v=[page-id]` |
| ABN | `https://www.notion.so/[page-id]?v=[page-id]` |
| LFC | `https://www.notion.so/[page-id]?v=[page-id]` |
| SFC | `https://www.notion.so/[page-id]?v=[page-id]` |

Then:

- **Duplicate check**: If a page with the same (or very similar) title and date already exists,
  stop and tell Shaw — don't auto-create. Example: if `FU - [Person 2]` already exists for `2026-04-17`,
  surface that and ask if he wants to update it, create anyway, or skip.
- **Formatting check**: Look at 2-3 recent pages of the same type (e.g. other `FU -` pages, or
  other `Send X Y` pages) and match their conventions — title capitalization, hyphen vs em dash,
  whether they use parenthetical suffixes like `(AM)` / `(PM)`, etc. Shaw's patterns drift over
  time; mirror the most recent examples, not old ones.

## Step 5: Create the page

Default body: **just a link to the most relevant call/session page**. Shaw's preference is
minimal body content; he adds more himself when needed. If there are multiple clearly relevant
pages (e.g., a CRM entry AND a recent call), link both.

Body format (keep it minimal):

```
<mention url="https://www.notion.so/<call-or-session-page-id>"/>
```

Or, if two pages are clearly relevant:

```
Call: <mention url="https://www.notion.so/<call-page-id>"/>
CRM: <mention url="https://www.notion.so/<crm-page-id>"/>
```

Do NOT add agendas, next steps, context sections, or other prose unless Shaw explicitly asks
for them. The call/session page already has that detail — linking is enough.

## Step 6: Create via `notion-create-pages`

Use the data source ID for the target database. Set the icon based on page type:

- **ABA task pages** → by what the task is: `⭕` generic (default), `✍️` prep/build, `✉️` email to send
- **Event/training pages** (ABA Calls, ABA Trainings) → `icon: "⭐"`
- **ABN, LFC, SFC** → omit the icon unless Shaw asks for one

Example for an ABA task:

```json
{
  "parent": {"data_source_id": "[page-id]", "type": "data_source_id"},
  "pages": [{
    "icon": "⭕",
    "properties": {
      "Name": "FU - [Person 3]",
      "date:Date:start": "2026-04-17",
      "date:Date:is_datetime": 0
    },
    "content": "<mention url=\"https://www.notion.so/[page-id]\"/>"
  }]
}
```

**Icon note**: Pass each emoji as its canonical form — `⭕` (U+2B55), `⭐` (U+2B50), `✅` (U+2705)
are bare; `✍️` (U+270D U+FE0F) and `✉️` (U+2709 U+FE0F) carry a variation selector and Notion
accepts them that way (verified 9/15/26). Don't add a selector to one that lacks it or strip one
that has it — copy the character as written here.

## Step 7: Confirm back to Shaw

Keep it brief: confirm what was created, the date, and the linked page(s). Don't re-explain the
skill.
