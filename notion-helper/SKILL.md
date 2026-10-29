---
name: "notion-helper"
description: "Navigate Shaw's Notion workspace and create ad hoc tasks, follow-ups, and reminders across his databases and pages. Use whenever Shaw asks to add a task, schedule a follow-up, create a reminder, put something on his plate for a day, drop a note into a database, or find/reference pages. Triggers: \"add a task for X\", \"create a FU for tomorrow\", \"add this to ABA\", \"find me the page about X\", or any ad hoc Notion creation/navigation not covered by a more specific skill (CRM, executive briefing, SOPs). Also fires for follow-up tasks after calls, workshops, or meetings — dated ABA pages. Beyond explicit asks, this is the home for Notion connector mechanics (rate-limit, schema gotchas), body-writing conventions, and the canonical database catalog: read it before ANY Notion read or write — query, schema read, row update, or page body text — even as a sub-step of another skill and even when Shaw never says \"Notion\". Touching his workspace is the trigger, not the wording."
---

# Notion Helper Skill

Shaw's general-purpose Notion assistant — ad hoc Notion work that doesn't fall under a more
specialized skill: creating tasks, follow-ups, and notes in his databases, and navigating the
workspace to find and link related pages.

Notion-only. It does NOT create iOS Reminders, calendar events, or anything outside Notion — if
Shaw needs a cross-system action, another skill handles that part.

**This applies to anything you write into Notion, not just database calls.** Body prose is where
most mistakes land — see "Notes are a reminder, not an explanation" below.

Shaw schedules work as **dated pages**: a `Date` property marks the day he wants to *act* on a
page, and it then surfaces in his daily briefing for that date. Most task pages are just title +
date, with body content only when context is needed.

**This skill is the canonical catalog of Shaw's Notion databases and key pages.** Other skills
(`crm`, `executive-briefing`, `meeting-prep`, etc.) reference the tables below rather than
duplicating IDs, so updates happen in one place.

---

## Main Databases

| DB | Database Page ID | Data Source ID | What lives here |
|---|---|---|---|
| ABA | `[page-id]` | `[page-id]` | Business tasks, outreach, events, follow-ups |
| ABA Trainings | `[page-id]` | `[page-id]` | Delivery sessions — workshops, trainings, engagements |
| ABA Calls | `[page-id]` | `[page-id]` | Sales calls — notes, prep, scheduling. `Name`, `Date`, `Email`, `Call Type` (select — read its options off the data source; Shaw retunes them), `Company` (relation → Companies, dual), `CRM` (url), `Friend` (relation → Friends). Page bodies open with `## Context`; handled by `crm` + `meeting-prep` |
| ABN | `[page-id]` | `[page-id]` | Newsletter editions, email blasts |
| LFC | `[page-id]` | `[page-id]` | YouTube videos — script → film → edit → upload |
| SFC | `[page-id]` | `[page-id]` | LinkedIn / YT community / social posts |
| Companies | `[page-id]` | `[page-id]` | One row per account (Relationship: Prospect / Client), inline on the CRM page above Active Leads. Every people database, Engagements, and each `convo-mining` database link to it through a `Company` relation. Carries no dates — touches belong to people; handled by `crm` |
| Active Leads | — | `[page-id]` | Pipeline rows, one per person, linked to their company. Under CRM page; handled by `crm` |
| Clients (Nurture) | — | `[page-id]` | Active / nurturing / expansion clients; handled by `crm` |
| Reviews/Referrals | — | `[page-id]` | Testimonial + referral lifecycles (one row per person, two status tracks), linked to a company or a Friends row; handled by `reviews-referrals`. Formerly "Testimonials"; the old standalone Referrals DB (`[database-id]`) is frozen |
| Friends | `[page-id]` | `[page-id]` | Non-lead network — friends, affiliates, channels, partners, subcontractors. Under ABA (Master); handled by `crm` |

Database icons are deliberately not cataloged here — they live in Notion and Shaw retunes
them, so a recorded copy drifts (a stale icon pair shipped in this very table, learned
8/20/26). When output needs a database's icon (e.g. emoji prefixes in a briefing), fetch the
database and read its `icon` attribute; if an inline database carries no icon of its own,
the parent page's icon is what Shaw sees.

The six dated work DBs (ABA → SFC) use a `Date` property — expanded as `date:Date:start` (ISO,
e.g. `2026-04-17`) and `date:Date:is_datetime` (0 for date-only). The four relationship DBs
(Active Leads, Clients, Reviews/Referrals, Friends) use `Next Contact` instead — expanded as
`date:Next Contact:start`. Companies carries no date property.

**Friends is titled `Partners` at the database level** but its data source is named `Friends`, so
a fetch shows `<ancestor-2-database title="Partners">` sitting above a data source named
`Friends`, and `notion-search` may surface it under either. Expect that mismatch when matching by
name, and anchor on the IDs above. Its `Type` taxonomy is documented in `crm`.

The nine work and relationship DBs above (ABA → Reviews/Referrals, Companies excluded) have **Today / Tomorrow view URLs**
in `executive-briefing` (its briefing machinery is the only consumer). The full-scan default views
used for the ad-hoc duplicate check live in `references/create-task-workflow.md`.

## Synthetic demo data — not real records

**Everything under the `Demo (Synthetic Data)` page (`[page-id]`) is
fake.** It holds mirror copies of the main databases (same names, same schemas) populated with an
invented cast for demos, videos, and workshops. Rules: exclude these rows from every real
workflow (CRM sweeps, briefings, syncs, searches on a person's name); never treat a row there as
a real lead, client, or task; never link real rows into the demo sandbox or vice versa. A fetched
demo row identifies itself by its ancestor path — check the ancestors when a search result looks
plausible but unfamiliar. The real databases are the ones in the Main Databases table above;
anything whose IDs aren't listed there deserves suspicion before acting.

## Other Key Pages

| Page | Page ID | When to use |
|---|---|---|
| CRM | `[page-id]` | Parent hub for Active Leads + Clients. Updates handled by `crm` |
| SOPs | `[page-id]` | Parent page for standard operating procedures. Structure + finding handled by `sop-helper` — fetch this page and match child pages by title; don't hardcode individual SOP IDs |
| ABA (Master) | `[page-id]` | Parent page for the ABA database and related resources |
| ABA Trainings (Hub) | `[database-id]` | Hub under ABA Master grouping all training/delivery sessions |
| Campaigns | `[page-id]` | Parent for per-campaign pages. Each carries its own campaign-local databases — fetch the campaign page for their `collection://` IDs rather than hardcoding |
| Demo (Synthetic Data) | `[page-id]` | Synthetic mirror databases for demos/videos — see "Synthetic demo data" section above. Never real records |

---

## Connector quirks (dates, views, caching, concurrency, schema)

Easy ways to get burned by the Notion connector, all learned from real debugging:

- **Shaw edits the same rows you're reading — re-read immediately before every write.** A read taken
  at the top of a conversation is stale by the time you act on it, and writing those values back
  silently clobbers whatever he changed in between (observed: a `UTM content` column reverted to
  conversation-start values on seven rows at once). Two habits prevent it: **re-query right before
  the write**, and **send only the fields you were asked to change** — passing a field back
  "unchanged" is still a write, and it's exactly the one that overwrites. The connector exposes no
  version history, so recovery means asking him to restore by hand from Notion's UI. Related: when
  a value he set differs from what you'd have chosen, that's a decision to surface, not to correct.
- **Cap parallel `query_data_sources` calls at 4.** The connector reliably serves 4 simultaneous
  SQL queries; a 5th trips a 429. Two limiters stack — Notion's own `collection_router_upstream_429`
  (backend overload) and the MCP layer's `mcp_tool_rate_limit` (concurrency cap). Batch queries in
  groups of ≤4 with a brief gap. Recovery is fast (~30–60s, matching the `retry_after: 30`), so a
  short wait beats the "few minutes" the message suggests. (`mode:view` queries are cheap and batch
  fine — this cap is SQL-mode only.)
- **Relative date filters resolve in UTC, not Shaw's timezone.** A "Date is today" / "Next day"
  view reads correctly in Shaw's Notion UI (Central) but, queried through the connector, resolves
  "today" in UTC — returning a different day during his evening (once UTC passes his local
  midnight). Either confirm `date -u +%F` matches the day you want, or filter on explicit ISO
  date strings (compared literally, timezone-safe).
- **`create_view` / `update_view` can only write fixed/exact dates, never relative ones.** The
  view DSL turns `"today"`/`"tomorrow"` into an `exact` literal (which matches nothing). Relative
  filters must be set in the Notion UI by hand.
- **When verifying a view's filter, trust the live view query over the fetched definition.** A
  `notion-fetch` can report a stale `advancedFilter` lagging a just-saved edit; a `mode:view`
  query reflects the current state.
- **A select/multi-select `ALTER COLUMN` restates the entire option set — including colors.** Because
  `ALTER COLUMN "Type" SET MULTI_SELECT('Friend':pink, ...)` declares the whole list rather than a
  delta, the API rejects the *entire* statement if any option you're keeping carries a different
  color than what's stored (`Cannot update color of select with name: X`). Fetch the data source
  first, carry every retained option's existing color forward verbatim, and let only genuinely new
  options pick a color. Restating options is also a write to every row holding them: even with
  names and colors unchanged, Notion can reissue an option (new ID in the result) and silently
  clear it from those rows while the call reports success. Count rows per option with a
  `GROUP BY` before and after, and restore anything that dropped.
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
- **Moving pages between databases extends the destination schema — invert that.** Notion (UI and
  connector alike) maps properties by name + type on a move and, rather than dropping what doesn't
  match, *adds* the source-only properties to the destination so no value is lost. Move LFC rows
  carrying `Date` into Content Ideas and a `Date` column appears there. Shaw's rule is the reverse:
  the destination schema is the contract for what belongs in that database, so incoming records
  conform to it — the database doesn't reshape itself around them. Before a cross-database move,
  diff the two schemas and name the source-only properties that actually carry values, so the drop
  is a decision rather than a surprise. After the move, fetch the destination and remove anything
  Notion added with `update_data_source` → `DROP COLUMN "<prop>"` (verified working; the property's
  values go with it, which is the point). A move isn't finished until the destination schema looks
  like it did before.
- **`delete_pages` trashes pages; nothing else does.** It moves up to 20 pages per call to Trash,
  where they stay restorable (`restore_pages`). Use it only for pages Shaw has named for deletion,
  and pass `user_confirmed: true` once he has. Don't reach for `move_pages` as a substitute: moving a
  row out of a database strips its properties.
- **A batched `update_content` can partially no-op and still report success.** When one
  search-and-replace in the array matches and another doesn't, the call returns a clean
  `{page_id}` — no error, no indication that half the edit was dropped. A *single* failing edit
  DOES raise `validation_error: No matches found`, so batching is precisely what costs you the
  signal. Treat success on a multi-edit call as "at least one edit landed," not "all of them
  did": either fetch and verify after, or split the edits when correctness matters. (Discovered
  when an invoice row silently kept saying "Draft" for a day after it had been sent, because the
  edit that was supposed to update it never matched.)
- **`update-page` runs one command per call — `properties` ride only on `update_properties`.**
  Passing `properties` alongside `update_content` (or any other body command) applies the body
  edit and silently drops the property change, still returning a clean `{page_id}`. A reschedule
  that edits both the `Date` property and the page's header line is two calls, and the date write
  is the one worth confirming with a quick query afterward.
- **A `<page>` block is a real child page and cannot be rewritten as a `<mention>`.** A
  database row's body can contain an actual child page (e.g. a retired Active Leads record filed
  under the Friends row that superseded it). It looks like just another link in the fetched
  markdown, but replacing it with `<mention url=.../>` fails with a 400 — "Cannot replace a
  `<page>` block". Write it back verbatim as `<page url="..."/>` to preserve it. Genuinely
  re-filing it needs a `parent` change on the child, and *deleting* it is impossible through the
  connector, so surface it to Shaw instead.
- **Watch for corrupt link text left by earlier automation.** Some bodies carry literal
  `\<page url="<mention-page .../>" /\>` — one link tag nested inside another and escaped into
  plain text. It renders as garbage and fails `replace_content` with the same 400 as above. Write
  the tag back as a clean `<page url="..."/>`. Worth suspecting whenever a rewrite fails on a
  record nobody has hand-edited.
- **Prefer `replace_content` for a full-body rewrite, `update_content` for a surgical edit.** The
  partial-no-op quirk above makes batched search-and-replace the wrong tool for restructuring a
  whole page — one unmatched `old_str` silently drops that part of the edit. Conversely, when a
  body carries many `<mention>` links that must survive, a targeted `update_content` on one
  line is far safer than re-emitting the whole body and trusting every URL to come back. Either
  way, re-fetch and count the links afterward.
- **A data source's `description` is write-only through the connector.** `update_data_source`
  sets it, but neither `fetch` on the database nor on the `collection://` data source returns it —
  so you cannot read the current value to confirm a write landed, or to avoid clobbering what's
  already there. When the description holds something worth keeping (a documented taxonomy, say),
  write the *complete* text rather than an incremental addition, and ask Shaw to confirm it in the
  UI rather than reporting it verified.
- **Anchor `update_content` edits on plain text, not on a `<mention>`.** An `old_str` ending in a
  `<mention url="..."/>` copied verbatim from a fresh fetch can still fail with `No matches found`:
  mentions round-trip unreliably between the fetched form and what the matcher compares against.
  Anchor on an adjacent plain-text line instead and insert around it. (10/24/26: a Friends-row
  Context edit anchored on a `**Campaign:** <mention .../>` bullet failed to match;
  the same insert anchored on the plain `Constraints` sub-bullet above it landed first try.)
- **Markdown tables are normalized to `<table>`/`<td>` blocks on save.** Author a table with pipe
  syntax and it renders fine, but a later `update_content` whose `old_str` uses pipes will match
  nothing. Fetch the page first and target the XML form — `<td>manual</td>\n<td>Draft</td>` — when
  editing cells. The same applies to any block you wrote in a shorthand Notion expands: read
  before you edit rather than assuming your input survived verbatim. **Inline text is rewritten
  too** — `~` comes back escaped as `\~`, and a bare email becomes
  `[[email]](mailto:[email])` — so an `old_str` copied from what you *sent* will miss where one
  copied from a fresh `fetch` matches.
- **Date-property flags take bare numbers, not strings.** `date:<prop>:is_datetime` rejects a
  quoted `"0"` with `must be 0 or 1; wrote 0 instead of "0"` — a message that reads like the write
  half-landed. It didn't: the `create_pages` call is rejected atomically, so resend with a bare
  `0` rather than hunting for a partial row. The tool schema accepts strings for property values
  generally, which is exactly what makes this one easy to get wrong.
- **The read surface returns URLs; `update_page` demands a dashed UUID.** A SQL query hands back
  `url` values, but `notion-update-page` rejects them with `page_id should be a valid uuid` — so
  every read-modify-write loop over a database has to convert the 32 hex characters into 8-4-4-4-12
  form on the way through. `create_pages` and `move_pages` both accept URLs, and the tool's own
  schema says "with or without dashes," which is what makes this land as a surprise mid-batch rather
  than up front. Nothing partial gets written when it fires — the rejection happens at validation —
  so the cost is a retry cycle, not a corrupted row. Convert once when you build the work list, not
  per call.
- **SQL-mode text is LOSSY — it silently drops link destinations.** A rich-text property
  containing `[Company](http://[company-site]/)` comes back from a SQL query as bare `Company`.
  Nothing errors and nothing warns; the URL is simply gone. **Never snapshot or back up a
  rich-text property with a SQL query.** Use `mode: "rows"` (faithful — preserves links,
  mentions, formatting) or a page `fetch`. Learned 9/18/26 the hard way: a SQL-built "backup"
  of 134 ABA Calls rows was about to gate an irreversible property deletion, and 12 records
  would have lost embedded URLs — including a 1,905-character field whose two links carried
  Calendly HMAC query strings that could not have been reconstructed. A second consequence:
  SQL output is also the wrong thing to diff agent work against, because it will show a
  faithful value as "wrong."
  Rows mode caps at 100 rows with no pagination cursor, so split larger pulls with date-range
  filters and verify no bucket comes back at exactly 100 (that means it was truncated).
- **Back up page *bodies* before a body-writing pass, not just the properties it will drop.**
  The two are not equally recoverable, and the gap is the whole reason to bother. A property
  mistake is enumerable: a mis-backfilled relation showed up as one count mismatch and diffed
  against the target list row by row, so "did every row get the right value" stayed a query.
  A body mistake is none of that — the connector exposes no block-level history, and Notion's
  page history restores the **whole page**, so reverting one bad paragraph also reverts every
  good edit made in the same pass, which usually makes the revert cost more than the defect.
  So snapshot the bodies (`mode: "rows"` or a per-page `fetch`) alongside the columns. Without
  one, "nothing else was touched" is an inference from structural agreement rather than a diff —
  and it is exactly the claim that cannot rest on the writer's own report. (9/18/26: two
  paragraphs were trimmed against an explicit instruction and the agent's tally said they were
  untouched; a reader noticing the prose had changed shape was the only detection.)
- **DDL type keywords are Notion's, not SQL's.** `ADD COLUMN "X" TEXT` fails with *Expected a type
  keyword* — the text type is `RICH_TEXT`. The valid set is in the `update_data_source` tool
  description; read it instead of reaching for SQL habits.
- **A type change is a claim about every existing value — query the outliers before proposing
  one.** A `RICH_TEXT` column that has been collecting addresses looks obviously retypeable to
  `EMAIL`, but Notion's email type holds exactly one address, and a single ABA Calls row carrying
  two comma-separated addresses was enough to make the retype wrong for all 134. The sampling
  instinct is the trap: the typical value always passes. Select the *extremes* instead — longest
  value, values containing separators, the empties — because a retype is only as safe as the
  worst row in the column.
- **Formula values can't be read back through the connector.** `notion-fetch` returns a
  `formulaResult://…` reference rather than the computed string, and formula columns appear in the
  data source's `notAvailableInQuerySql` list, so SQL can't select them either — the only way to
  see what a formula renders is to open the page in a browser. Factor that into the choice between
  a formula and a plain property: a derived value is DRY but unverifiable from here, while a plain
  URL/text property is duplicated but readable and directly editable. Shaw tends to want the one he
  can see and change, especially for a value he'll copy out and paste elsewhere.
- **Columns, callouts, toggles and databases have specific block syntax — read the spec.** For
  anything beyond text/lists/headings, read `notion://docs/enhanced-markdown-spec` (fetch it via
  `notion-fetch` with that URI) instead of guessing. Column layouts in particular use
  `<columns><column>…</column></columns>` with **tab** indentation for children, and engagement
  bodies now rely on them.
- **A newly created child page or database is auto-appended to the end of the parent, and you
  can't place it by writing the tag yourself.** `<page url="...">` and `<database url="...">` tags
  preserve or *move* existing blocks — inserting one for a page that already exists elsewhere
  moves it, and the connector rejects an attempt to add one that duplicates an appended block. To
  file a new child under a specific heading: create it, fetch the parent to get the tag verbatim,
  then make **one** `update_content` call with two edits — remove the appended tag, reinsert it at
  the target location. This is the case where batching is correct (both halves are required), so
  verify with a fetch afterward per the partial-no-op quirk above. Flipping a database to inline
  is the same move: reproduce the fetched tag exactly and change only `inline="false"` →
  `inline="true"`.
- **Meeting-notes blocks fetch as summary only — and the summary mis-attributes speakers.** A
  `fetch` on a page with an embedded meeting note returns the AI `<summary>` and omits the
  transcript unless `include_transcript: true`. Treat the summary as an index, not a source: it
  compresses content reliably but attributes it unreliably, so anything that hangs on *who said
  what* — action-item owners, per-person use cases, quotes — must be verified against the full
  transcript before it drives an outbound draft or a database write. (8/29/26: a group follow-up
  assigned one attendee a use case another attendee had emailed in that morning, straight from a
  mis-attributed summary action item.) The transcript fetch usually overflows the tool-result
  limit and lands as a single ~100k-character line in a saved file; Read can't chunk one long
  line, so pull passages with Grep `-o` context windows (`.{200}phrase.{200}`, shrinking the
  window until the match isn't omitted) and chain backwards phrase-by-phrase. Transcripts carry
  no speaker labels — attribute via conversational cues ("[Name], go ahead", "she emailed you
  about this morning") cross-checked against pre-session notes and intake data.

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
  title + date, icon per the ABA work-type vocabulary below (a mirrored FU round is `✉️`), body =
  a single `<mention>` link back to the campaign row. The
  campaign DB stays source of truth; the ABA copy surfaces the work.
- **Find a page** — `notion-search` with the *content* term, not just a person's name (e.g.
  "[Person] workshop", not "[Person]"). Return the top 1-3 with links.
- **Link pages on an existing task** — fetch the page, then `notion-update-page` with
  `command: "update_content"` and a search-and-replace to inject `<mention url="..."/>` inline.
- **Mark a task done** — Shaw tracks status via page icon: any work-type icon (`⭕`/`✍️`/`✉️`)
  means open, `✅` means done. Just flip the icon
  (no property/content change) via `notion-update-page`, `command: "update_properties"`, empty
  `properties`, empty `content_updates`, `icon: "✅"`. To close several at once, fire the updates
  in parallel — but first confirm scope ("these follow-ups" usually means the ones already
  discussed, not every open task).
- **Delete a moot task** — when Shaw says a task shouldn't exist (e.g. the follow-up for a call
  that was canceled and not rescheduled), trash it with `delete_pages`. A task that's *done* gets
  `✅` instead; done and deleted aren't the same to him.
- **Capture a newsletter or email blast into an ABN page** — see `references/abn-capture.md`.
- **Link Meet transcripts to call pages** (batch page-freshness workflow) — see
  `references/transcript-linking.md`.

---

## Writing page bodies

Applies to every page body in the workspace — task pages, campaign rows, script pages, anything
you add content to.

**Notes are a reminder, not an explanation.** Shaw's pages are terse keyword bullets he wrote to
jog his own memory, not prose that conveys the information to a reader. He is the audience and he
already has the context, so writing past the reminder isn't thoroughness — it's a rewrite he now
has to trim. Anything richer belongs in chat, where he can pull what he wants into the page
himself.

**Write to the standard, not to what's already there.** Matching the surrounding density sounds
safe and is the mechanism by which drift spreads: a database that has bloated teaches the bloat to
every page written after it, and the instruction to blend in guarantees nobody ever writes the
page that breaks the pattern. When what's already there is denser than the standard below, it is
the thing that's wrong — write to the standard and say the existing pages need trimming.

Four checks, each of which has a wrong answer — unlike "keep it terse", which doesn't:

1. **Is it already in a property?** Then don't write it. A body that narrates `Status`, a date
   field, or a dated `Notes` log duplicates a field that stays current while the prose silently
   rots — and the prose is what someone reads first.
2. **Does the bullet contain "so", "because", "rather than", "presumably"?** Cut from there. State
   the fact; the implication is his to draw. `owns the reps who'd take the training` beats `owns
   the reps who would take the training, so he controls both the use cases and attendance`.
3. **Is it a judgment that expires** — "warmest", "strongest", "best fit"? Cut. It was true the
   day it was written and is quietly false a week later.
4. **Does it ask the reader to decide something?** That's a chat message, not a note. A question
   filed in a page body is asked somewhere he won't see it in time to answer.

What survives is what no property can hold: the artifact itself (a drafted message, a quote in
their own words) and a live warning that changes the next action.

---

## Rules and Preferences

- **Default to ABA** for ad hoc tasks and FUs unless another database is clearly right.
- **Keep titles short and action-first** — match Shaw's patterns (see `references/create-task-workflow.md`).
- **Match formatting from recent examples** — before creating, sample 2-3 recent pages of the
  same type to confirm current conventions (title style, suffix patterns, etc.).
- **Check for duplicates** — don't auto-create if a similar page exists on the same date; surface
  it to Shaw first.
- **ABA icons say what kind of work a task is** — `⭕` generic task (the default), `✍️` prep or
  build work (deck, agenda, game plan), `✉️` an email to send (precall, follow-up, nudge). All three
  flip to `✅` when done. ABA holds tasks only — calls and events live in ABA Calls and ABA
  Trainings, so `⭐` never appears in ABA. Other DBs (ABN, LFC, SFC) get no icon unless Shaw asks.
- **The icon follows the work, not the title** — two tasks both named `Precall - X` can differ:
  `✉️` when the work is sending the pre-call email, `✍️` when it's building the agenda. Read what
  the task actually does.
- **The icon on a Calls/Trainings page is its delivery state, not decoration** — `⭐` booked,
  `✅` held, `⚠️` in limbo, `❌` booked but never happened and not rebooked.
  A dated page is not evidence the session occurred; the icon is what says so. Anything reading
  these tables to decide what was delivered has to read the icon.
- **`⚠️` and `❌` differ by whether the session is still alive** — `⚠️` means the session is in
  limbo: rescheduled, at risk, or otherwise unconfirmed, usually with the ball in the other
  person's court. The page keeps its slot — flip the icon, leave the date as-is until a real one
  exists, then re-date that same page and flip it back to `⭐` once it firms up. `❌` means the
  session is dead — a no-show or decline that isn't rebooked. A `❌` page that later gets rebooked
  is the same commitment coming back to life: re-date that page, flip it to `⭐`, and note the old
  date on its call line rather than creating a second page. The question to ask is whether the
  same commitment is still pending, not whether a date moved.
- **Minimal body content** — default to just a link; add structure only when Shaw asks.
- **Prep and FU tasks link the call they serve** — a prep or follow-up task exists for one call
  or session, so its body links that ABA Calls / ABA Trainings page, not the engagement or CRM
  row above it; that's the page Shaw opens to act. Recurring prep/FU tasks are often batched
  weeks before their call page exists, so the link is owed: whoever creates the call page later
  adds it to that call's open prep/FU tasks.
- **A call page is never created alone** — creating an ABA Calls or ABA Trainings page means
  running its SOP's Setup in the same pass (the `FU - [First Name]` task, the backlink on the
  relationship record) or confirming those already exist. Setup is owed by whatever brings the
  page into existence — a booking, a sync, a prep run, an ad hoc ask — so a page created down any
  path other than `calendar-helper` otherwise ships without its follow-up.
- **Use `<mention url="..."/>`** for internal links (not Markdown `[text](url)`) — it creates
  a proper Notion page reference with the correct title. The connector's markup changes over
  time (this tag replaced `<mention-page>`, which other skills still show), so its own warnings
  and its markdown spec outrank any example in a skill: when a write comes back flagging a
  deprecated tag, use the form it names.
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
| Query a database view (all items) | `notion-query-data-sources` (`mode: "view"`) |
| Query a data source (SQL) | `notion-query-data-sources` |
| Change a schema / property / option set | `notion-update-data-source` |