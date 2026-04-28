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
  that person's CRM entry and most recent call page)

## Step 2: Match Shaw's naming conventions

Shaw's task titles are short, action-first, and follow recurring patterns:

| Pattern | Example |
|---|---|
| `FU - <Name>` | `FU - [Person]` |
| `Send <Name> <thing>` | `Send [Person] agenda + Call Prep`, `Send [Person] FU email` |
| `Follow up with <Name>` | `Follow up with [Person]`, `Follow up with speakers` |
| `Prep for <thing>` | `Prep for 1:1 Training (PM)` |
| `<Name> - <session type>` | `[Person] - Check-in`, `[Person] - 1:1 Claude Workshop` |
| `Reply <Name>` | `Reply [person]` |
| `<verb> <object>` | `Update website messaging`, `Test new ABA copy` |

Prefer these patterns over verbose titles. If Shaw says "remind me to follow up with [Person]
tomorrow," the title is `FU - [Person]`, not "Reminder: Follow up with [Person] tomorrow."

## Step 3: Find related pages to link

If the request mentions a person's name, search Notion for:

- Their CRM entry (Active Leads data source: `collection://[page-id]`
  or Clients: `collection://[page-id]`)
- Their most recent call page (ABA Calls) or delivery page (ABA Trainings)

Use `notion-search` with the person's name. Pick the most relevant hits — typically the CRM
entry plus the most recent call/session page.

## Step 4: Check for duplicates and sample formatting

Before creating, query the target database view to check for likely duplicates and to confirm
Shaw's current naming/formatting conventions. Use `notion-query-database-view` with the
database's view URL (see SKILL.md → "Default View URLs").

Then:

- **Duplicate check**: If a page with the same (or very similar) title and date already exists,
  stop and tell Shaw — don't auto-create. Example: if `FU - [Person]` already exists for `2026-04-17`,
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
<mention-page url="https://www.notion.so/<call-or-session-page-id>"/>
```

Or, if two pages are clearly relevant:

```
Call: <mention-page url="https://www.notion.so/<call-page-id>"/>
CRM: <mention-page url="https://www.notion.so/<crm-page-id>"/>
```

Do NOT add agendas, next steps, context sections, or other prose unless Shaw explicitly asks
for them. The call/session page already has that detail — linking is enough.

## Step 6: Create via `notion-create-pages`

Use the data source ID for the target database. For FU-prefixed tasks, set `icon: "⭕"` on the
new page. For all other tasks, omit the icon. Example for ABA:

```json
{
  "parent": {"data_source_id": "[database-id]", "type": "data_source_id"},
  "pages": [{
    "icon": "⭕",
    "properties": {
      "Name": "FU - [Person]",
      "date:Date:start": "2026-04-17",
      "date:Date:is_datetime": 0
    },
    "content": "<mention-page url=\"https://www.notion.so/[page-id]\"/>"
  }]
}
```

**Icon note**: Use the bare emoji `⭕` (code point U+2B55). Do NOT append a variation selector
(U+FE0F) — Notion's API rejects that as an invalid icon URL.

## Step 7: Confirm back to Shaw

Keep it brief: confirm what was created, the date, and the linked page(s). Don't re-explain the
skill.
