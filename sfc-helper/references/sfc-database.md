# Creating SFC pages

## Database

- **SFC** database page: `[database-id]`
- **Data source** (parent for new rows): `[page-id]`
- Table view (to list/scan existing rows): use `notion-query-database-view` on the SFC table view.

## Schema

| Property | Type | Notes |
|---|---|---|
| Name | title | The hook / working title |
| Date | date | Scheduled post date (`date:Date:start`, `YYYY-MM-DD`) |
| Channel | multi-select | `LinkedIn`, `YT Community` — usually `LinkedIn`; set `YT Community` for repurpose-mode pages |
| Tags | multi-select | `Thesis`, `How-to`, `Use case`, `Education`, `Builder Log`, `Resource`, `Share`, `Promo`, `Journey`, `Listicle` |
| Series | multi-select | Optional (existing content series) |
| Time | text | Optional |

The post **briefing goes in the page body**, not a property. (The `Copy (old)` text field is legacy — leave it alone.)

## The backlog parking convention

Unscheduled ideas are parked on a **single future date** (recently `2026-06-21`). That date is effectively the backlog, and it's where duplicates accumulate. Before creating anything, query the table view, look at what's parked there and what's recently posted, and **flag/reuse duplicates instead of adding new ones**. If an idea you want to schedule already exists in the backlog, reschedule and brief *that* page rather than creating a second copy.

## Briefing format (page body)

A briefing, not a finished post. Keep it terse:

```
**Angle:** <the hook / thesis in one or two lines>
**Audience:** Sponsor / Champion / Reach satellite
**Key points:**
- <2–4 bullets of substance>
**Source:** <anonymized origin — e.g. "[Company] ops session" or "VC CFO transcript">. <Honesty note on any number, e.g. "~1 hr is her estimate">
**CTA:** <only if relevant — e.g. AI Rollout Audit, link in comments>
**Close:** <closing-question idea>
```

## Repurpose pages (exact copy, not a briefing)

When a page re-runs a proven post on another channel (see the repurpose mode in SKILL.md), the body holds the **verbatim original copy in a fenced code block** instead of a briefing — the wording is what won, so preserve it exactly and keep it one-click copyable. If the source post carried an image/video/document, pin a one-line media note at the top of the page (`> 📷 Includes an image — pull it from the original before publishing`); text-only posts get none. Still set the ⬜ icon and the target `Channel`.

## Creating the rows

Use `notion-create-pages` with the data source as parent:

- `parent`: `{ "type": "data_source_id", "data_source_id": "[database-id]" }`
- `properties`: `{ "Name": "<hook>", "date:Date:start": "2026-MM-DD", "Channel": "[\"LinkedIn\"]", "Tags": "[\"Thesis\"]" }`
- `content`: the briefing markdown above.

You can create the whole week in one `notion-create-pages` call (pages array).

## Icon

Set the **⬜ icon** on every SFC post page (it marks an unwritten/queued post). On `notion-create-pages` you can pass `icon` per page; when reusing/updating an existing page, pass `icon: "⬜"` alongside the content/property update. This matches the convention Shaw uses on the backlog.

## Reusing an existing backlog page

If the idea already exists (from the dedupe scan): update that page instead of creating a new one — `notion-update-page` with `replace_content` for the briefing (plus `icon: "⬜"`), then a separate `update_properties` call to set `date:Date:start` and `Channel`/`Tags`. Don't stack a second duplicate.
