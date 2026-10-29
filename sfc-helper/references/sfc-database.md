# Creating SFC pages

## Database

- **SFC** database page: `[database-id]`
- **Data source** (parent for new rows): `[page-id]`
- Table view (to list/scan existing rows): use `notion-query-data-sources` on the SFC data source. The date column is `date:Date:start`; querying `Date` errors out.

## Schema

| Property | Type | Notes |
|---|---|---|
| Name | title | The hook / working title |
| Date | date | Scheduled post date (`date:Date:start`, `YYYY-MM-DD`) |
| Channel | multi-select | `LinkedIn`, `YT Community` — usually `LinkedIn`; set `YT Community` for repurpose-mode pages |
| Tags | multi-select | `Thesis`, `How-to`, `Use case`, `Education`, `Builder Log`, `Resource`, `Share`, `Promo`, `Journey`, `Listicle` |
| Type | multi-select | `Reach`, `Engagement`, `Promo` — the post's *job*, as distinct from Tags (its content shape). Drives the reach/engagement alternation in `scheduling-principles.md` #2; `Promo` marks a post carrying a CTA (#9) |
| Campaign | multi-select | Set when the post belongs to a campaign sequence (e.g. `Aug 2026 Scorecard`). Campaign posts own their dates — the backlog fits around them, not through them |
| Series | multi-select | Optional (existing content series) |
| Time | text | Optional |

The page body holds **Shaw's unstructured notes on the idea, then a `---` divider, then the final post copy as plain paragraphs** — not a property. He often writes either half himself, so fetch and read the body before writing to it. Claude schedules straight from the page, so everything below the divider is the post exactly as it will publish, and notes, provenance, and reminders stay above it. Numbered items may become Notion list blocks; the schedulers type each item's real number, so that's fine. Older pages hold the copy in a fenced code block instead — read it the same way. (The `Copy (old)` text field is legacy — leave it alone.)

## Choosing a Tag

Tags mark a post's **content type**, and a post gets the single tag that matches its primary job. Judge the page body, not the title — a "Thesis:" prefix or a "How to" phrasing in the title isn't decisive if the body does something else. The distinctions:

- **Thesis** — argues a point of view: a belief, a contrarian take, or "here's how I see it," often opening with a claim someone could disagree with.
- **Education** — explains a concept or feature neutrally ("what is X?", "how does X work?"). No stance, no steps.
- **How-to** — actionable steps for doing a specific thing; the reader follows along and gets a result.
- **Use case** — a specific, concrete (anonymized) story of a real before → after.
- **Resource** — hands the reader a reusable asset (cheat sheet, template, checklist, prompt). The asset is the point.
- **Share** — points the reader to a piece of content (video, blog, podcast) to consume elsewhere.
- **Promo** — promotes an event or offer with a clear ask (register, attend, buy).
- **Listicle** — organized around an enumerated set ("X types of", "X ways to", "X levels of"); the list structure is the format.
- **Builder Log** — behind-the-scenes of something being built or shipped.
- **Journey** — a personal arc or transformation over time.

Two tie-breakers for posts that straddle categories:

- **Story vs. point.** A post that opens with a client anecdote but pays off in a reframe or belief is **Thesis**, not Use case — the takeaway decides, not the vehicle it rides in on.
- **Deliverable vs. pointer.** A "Share X" post is **Resource** when the reader keeps the asset (a cheat sheet they'll use), and **Share** when its job is to drive them to go watch or read something elsewhere.


## The backlog parking convention

Unscheduled ideas park on the **next upcoming Sunday** — a *rolling* backlog date, not a fixed one. **Compute it** (the nearest future Sunday from today); don't hardcode a value like `2026-06-21`, which goes stale. Each weekend Shaw reviews what's parked on that Sunday, schedules the good ones onto real weekday dates, and rolls the rest forward to the following Sunday. So the backlog always lives on the nearest future Sunday and advances a week at a time.

**Date is status.** Read a row's state from its Date, not from an empty Channel/Tags:

- A **past-dated** row is already **posted** — it's off the table.
- A **future-dated** row (sitting on the Sunday backlog, ⬜ icon) is **parked/unwritten**.

**Recycle after ~4 weeks.** A posted topic is off the table only while it's recent. Once it's more than ~4 weeks old it's fair game to renote and run again — don't treat every past post as permanently spent.

Before creating anything, query the table view and run the **dedupe scan on two windows**: what's parked on the upcoming Sunday, and what's been posted in the **last ~4 weeks**. **Flag/reuse duplicates instead of adding new ones** — if an idea you want to schedule already exists in the backlog, reschedule and build on *that* page rather than creating a second copy. A matching topic posted more than ~4 weeks ago doesn't count as a duplicate; it's eligible to rerun.

## Repurpose pages (copy only, no notes)

When a page re-runs a proven post on another channel (see the repurpose mode in SKILL.md), the body holds only the **verbatim original copy as plain paragraphs**, with no notes half — the wording is what won, so preserve it exactly. If the source post carried an image/video/document, pin a one-line media note at the top of the page, above a `---` divider (`> 📷 Includes an image — pull it from the original before publishing`); text-only posts get none. Still set the target `Channel` and the icon that matches it (see **Icon** below).

## Creating the rows

Use `notion-create-pages` with the data source as parent:

- `parent`: `{ "type": "data_source_id", "data_source_id": "[database-id]" }`
- `properties`: `{ "Name": "<hook>", "date:Date:start": "2026-MM-DD", "Channel": "[\"LinkedIn\"]", "Tags": "[\"Thesis\"]" }`
- `content`: Shaw's notes on the idea, then a `---` divider and the post copy once it exists.

You can create the whole week in one `notion-create-pages` call (pages array).

## Icon

The icon encodes the page's **channel**, so it's readable at a glance on the calendar: **⬜ for a LinkedIn page** (it marks an unwritten/queued post), **🔴 for a YT Community page**. On `notion-create-pages` you can pass `icon` per page; when reusing/updating an existing page, pass the matching icon alongside the content/property update. This matches the convention Shaw uses on the backlog.

## Reusing an existing backlog page

If the idea already exists (from the dedupe scan): update that page instead of creating a new one — `notion-update-page` with `insert_content` to append below whatever is already there (plus the icon matching its `Channel`), then a separate `update_properties` call to set `date:Date:start` and `Channel`/`Tags`. Don't stack a second duplicate.
