---
name: notion-helper
description: "Navigate Shaw's Notion workspace and create ad hoc tasks, follow-ups, and reminders across his databases and pages. Use whenever Shaw asks to add a task, schedule a follow-up, create a reminder, put something on his plate for a day, drop a note into a database, or find/reference pages. Triggers: \"add a task for X\", \"create a FU for tomorrow\", \"put this on my plate for Monday\", \"add this to ABA\", \"find me the page about X\", \"link the call page to Y\", or any ad hoc Notion creation/navigation not covered by a more specific skill (CRM, executive briefing, SOPs). Also fires for follow-up tasks after calls, workshops, or meetings — dated ABA pages. Beyond explicit asks, this is the home for Notion connector mechanics (rate-limit, timezone, schema gotchas) and the canonical database catalog: load it before any direct Notion database operation (query, schema read, row update), even as a sub-step of another task and even when Shaw never says \"Notion\". The trigger is touching his databases, not the wording."
---

# Notion Helper Skill

Shaw's general-purpose Notion assistant — ad hoc Notion work that doesn't fall under a more
specialized skill: creating tasks, follow-ups, and notes in his databases, and navigating the
workspace to find and link related pages.

Notion-only. It does NOT create iOS Reminders, calendar events, or anything outside Notion — if
Shaw needs a cross-system action, another skill handles that part.

Shaw schedules work as **dated pages**: a `Date` property marks the day he wants to *act* on a
page, and it then surfaces in his daily briefing for that date. Most task pages are just title +
date, with body content only when context is needed.

**This skill is the canonical catalog of Shaw's Notion databases and key pages.** Other skills
(`crm`, `executive-briefing`, `pre-call-research`, etc.) reference the tables below rather than
duplicating IDs, so updates happen in one place.

---

## Main Databases

| DB | Icon | Database Page ID | Data Source ID | What lives here |
|---|---|---|---|---|
| ABA | 🎓 | `[page-id]` | `[page-id]` | Business tasks, outreach, events, follow-ups |
| ABA Trainings | 🏫 | `[page-id]` | `[page-id]` | Delivery sessions — workshops, trainings, engagements |
| ABA Calls | 👨‍🏫 | `[page-id]` | `[page-id]` | Sales calls — notes, prep, scheduling |
| ABN | 🗞️ | `[page-id]` | `[page-id]` | Newsletter editions, email blasts |
| LFC | 📹 | `[page-id]` | `[page-id]` | YouTube videos — script → film → edit → upload |
| SFC | 📅 | `[page-id]` | `[page-id]` | LinkedIn / YT community / social posts |
| Active Leads | 💼 | — | `[page-id]` | Pipeline rows. Under CRM page; handled by `crm` |
| Clients (Nurture) | 🌱 | — | `[page-id]` | Active / nurturing / expansion clients; handled by `crm` |
| Testimonials | ⭐ | — | `[page-id]` | Testimonial workflow; handled by `testimonials` |
| Friends | 🫂 | `[page-id]` | `[page-id]` | Non-lead network — friends, affiliates, channels, partners, subcontractors. Under ABA (Master); handled by `crm` |

The six dated work DBs (ABA → SFC) use a `Date` property — expanded as `date:Date:start` (ISO,
e.g. `2026-04-17`) and `date:Date:is_datetime` (0 for date-only). The four relationship DBs
(Active Leads, Clients, Testimonials, Friends) use `Next Contact` instead — expanded as
`date:Next Contact:start`.

**Friends is titled `Partners` at the database level** but its data source is named `Friends`, so
a fetch shows `<ancestor-2-database title="Partners">` sitting above a data source named
`Friends`, and `notion-search` may surface it under either. Expect that mismatch when matching by
name, and anchor on the IDs above. Its `Type` taxonomy is documented in `crm`.

The nine work and relationship DBs above (ABA → Testimonials) have **Today / Tomorrow view URLs**
in `executive-briefing` (its briefing machinery is the only consumer). The full-scan default views
used for the ad-hoc duplicate check live in `references/create-task-workflow.md`.

## Other Key Pages

| Page | Page ID | When to use |
|---|---|---|
| CRM | `[page-id]` | Parent hub for Active Leads + Clients. Updates handled by `crm` |
| SOPs | `[page-id]` | Parent page for standard operating procedures. Structure + finding handled by `sop-helper` — fetch this page and match child pages by title; don't hardcode individual SOP IDs |
| ABA (Master) | `[page-id]` | Parent page for the ABA database and related resources |
| ABA Trainings (Hub) | `[database-id]` | Hub under ABA Master grouping all training/delivery sessions |
| Campaigns | `[page-id]` | Parent for per-campaign pages. Each carries its own campaign-local databases — fetch the campaign page for their `collection://` IDs rather than hardcoding |

---

## Connector quirks (dates, views, caching, concurrency, schema)

Easy ways to get burned by the Notion connector, all learned from real debugging:

- **Cap parallel `query_data_sources` calls at 4.** The connector reliably serves 4 simultaneous
  SQL queries; a 5th trips a 429. Two limiters stack — Notion's own `collection_router_upstream_429`
  (backend overload) and the MCP layer's `mcp_tool_rate_limit` (concurrency cap). Batch queries in
  groups of ≤4 with a brief gap. Recovery is fast (~30–60s, matching the `retry_after: 30`), so a
  short wait beats the "few minutes" the message suggests. (`mode:view` queries are cheap and batch
  fine — this cap is SQL-mode only.)
- **Relative date filters resolve in UTC, not Shaw's timezone.** A "Date is today" / "Next day"
  view reads correctly in Shaw's Notion UI (Central) but, queried through the connector, resolves
  "today" in UTC — returning a different day during his evening (once UTC passes his local
  midnight). Resolve dates in Shaw's *current* timezone (read it from the session context — he
  travels), then either confirm `date -u +%F` matches, or filter on explicit ISO date strings
  (compared literally, timezone-safe).
- **`create_view` / `update_view` can only write fixed/exact dates, never relative ones.** The
  view DSL turns `"today"`/`"tomorrow"` into an `exact` literal (which matches nothing). Relative
  filters must be set in the Notion UI by hand.
- **When verifying a view's filter, trust the live view query over the fetched definition.** A
  `notion-fetch` can report a stale `advancedFilter` lagging a just-saved edit; a `mode:view`
  query reflects the current state.
- **A multi-select `ALTER COLUMN` restates the entire option set — including colors.** Because
  `ALTER COLUMN "Type" SET MULTI_SELECT('Friend':pink, ...)` declares the whole list rather than a
  delta, the API rejects the *entire* statement if any option you're keeping carries a different
  color than what's stored (`Cannot update color of select with name: X`). Fetch the data source
  first, carry every retained option's existing color forward verbatim, and let only genuinely new
  options pick a color.
- **Renaming a multi-select vocabulary takes three passes, not one.** Following from the above: a
  single `ALTER` that both adds new options and drops old ones leaves no moment where both
  vocabularies coexist — rows still holding a retired value lose it, and you can't write a new
  value that doesn't exist yet. Instead (1) `ALTER` to the *union* of old and new options, (2)
  retag every row, (3) `ALTER` again to drop the retired ones. Run a `SELECT` between steps 2 and 3
  to confirm nothing is still carrying a value about to disappear.
- **Option `description` isn't writable through the DDL.** `MULTI_SELECT('X':color)` takes a name
  and a color only. When a taxonomy needs its definitions recorded, put them in the data source's
  `description` field (`update_data_source`, `description` param) — it renders under the database
  title, which is where someone reading the database will actually look. An undefined label is how
  a catch-all value drifts back into existence.
- **No delete tool.** The connector can create, update, and move pages, but cannot trash them. Any
  real deletion (e.g. a moot follow-up for a canceled-and-not-rescheduled call) is a manual step —
  surface the page to Shaw rather than soft-closing it with a `✅`.

---

## Core Workflow: Creating an Ad Hoc Task

Most requests are "add a task for X on [date]" or "create a FU for [person] [when]." For the full
step-by-step workflow — title parsing, naming conventions, duplicate checks, and the
`notion-create-pages` payload — see `references/create-task-workflow.md`.

## Other Common Asks

- **Create a page in another database** — when Shaw names it ("add to LFC", "put in SFC"), use
  that DB's data source ID from Main Databases. If it's not listed, fetch the database page and
  read the `<data-source url="collection://...">` tag, then create.
- **Mirror campaign tasks into ABA** — campaign-local databases don't feed the daily briefing.
  When Shaw needs to act on a campaign action item day-to-day, mirror it as an ABA task: same
  title + date, `⭕` icon, body = a single `<mention-page>` link back to the campaign row. The
  campaign DB stays source of truth; the ABA copy surfaces the work.
- **Find a page** — `notion-search` with the *content* term, not just a person's name (e.g.
  "[Person] workshop", not "[Person]"). Return the top 1-3 with links.
- **Link pages on an existing task** — fetch the page, then `notion-update-page` with
  `command: "update_content"` and a search-and-replace to inject `<mention-page url="..."/>` inline.
- **Mark a task done** — Shaw tracks status via page icon: `⭕` open, `✅` done. Just flip the icon
  (no property/content change) via `notion-update-page`, `command: "update_properties"`, empty
  `properties`, empty `content_updates`, `icon: "✅"`. To close several at once, fire the updates
  in parallel — but first confirm scope ("these follow-ups" usually means the ones already
  discussed, not every open task).
- **Delete a moot task** — the connector has no hard-delete/trash action (see Connector quirks).
  For a task that's *done*, flip the icon to `✅`. For a task that's *moot and should disappear* —
  e.g. the follow-up for a call that was canceled and not rescheduled — deletion is the right call,
  but the connector can't do it. Surface the page (title + link) to Shaw so he can delete it
  manually; don't fall back to marking it `✅`, since done and deleted aren't the same to him.
- **Capture a Kit / newsletter draft into an ABN page** — see `references/abn-capture.md`.
- **Link Meet transcripts to call pages** (batch page-freshness workflow) — see
  `references/transcript-linking.md`.

---

## Rules and Preferences

- **Default to ABA** for ad hoc tasks and FUs unless another database is clearly right.
- **Keep titles short and action-first** — match Shaw's patterns (see `references/create-task-workflow.md`).
- **Match formatting from recent examples** — before creating, sample 2-3 recent pages of the
  same type to confirm current conventions (title style, suffix patterns, etc.).
- **Check for duplicates** — don't auto-create if a similar page exists on the same date; surface
  it to Shaw first.
- **Default icons by type** — ABA task pages `⭕`; event/training pages (ABA Calls, ABA Trainings)
  `⭐`; other DBs (ABN, LFC, SFC) no icon unless asked. `⭕` flips to `✅` when done.
- **Minimal body content** — default to just a link; add structure only when Shaw asks.
- **Use `<mention-page url="..."/>`** for internal links (not Markdown `[text](url)`) — it creates
  a proper Notion page reference with the correct title.
- **Don't duplicate specialized work** — CRM updates → `crm`; SOP create/edit/reference →
  `sop-helper`; "what's on my plate today" → `executive-briefing`. This skill is *ad hoc*
  task/page creation and navigation that sits alongside them.

---

## Quick Reference: Notion Tools

Assume these are loaded via `tool_search` before first use.

| Need | Tool |
|---|---|
| Find pages by keyword | `notion-search` |
| Read a page or database | `notion-fetch` |
| Create one or more pages | `notion-create-pages` |
| Edit a page's properties or content | `notion-update-page` |
| Query a database view (all items) | `notion-query-database-view` |
| Query a data source (SQL) | `notion-query-data-sources` |
| Change a schema / property / option set | `notion-update-data-source` |

