---
name: night-transcript-linker
description: Auto-link Google Meet transcripts to today's ABA Calls and ABA Trainings pages
---

Auto-link Google Meet transcripts to today's call/training pages in Notion. This implements the notion-helper "Linking Meet transcripts to call pages" workflow on a schedule. It must be IDEMPOTENT — safe to re-run, skip anything already linked.

**Timezone rule (read first).** This task fires at 9 PM Central daily, AFTER all of the day's calls have wrapped and Meet transcripts have had time to land. EVERYTHING in this skill — the Notion date filter and the Drive search window — uses **Central time (America/Chicago)** to define "today." Do NOT use UTC. By 9 PM Central, UTC has already rolled to the next day, so any UTC-based filter will miss the day's calls.

## Step 0 — Compute today's Central-time date and the matching UTC window

Compute the Central day and its UTC bounds with Python's `zoneinfo` — do NOT use `date -d` with a `TZ` prefix. Some runtimes' `date` (non-GNU/busybox) ignore `TZ` when parsing `-d`, silently dropping the offset and producing a wrong, sub-24-hour window (e.g. `T00:00:00Z` → same-day `T23:00:00Z`). `zoneinfo` does timezone-aware arithmetic portably and handles CDT/CST (DST) automatically. Run this in bash and reuse the values throughout:

```bash
python3 -c "
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
tz = ZoneInfo('America/Chicago')
today = datetime.now(tz).date()
start = datetime(today.year, today.month, today.day, tzinfo=tz)
end = start + timedelta(days=1)
u = ZoneInfo('UTC')
print('TODAY_CENTRAL=' + today.isoformat())
print('WINDOW_START_UTC=' + start.astimezone(u).strftime('%Y-%m-%dT%H:%M:%SZ'))
print('WINDOW_END_UTC=' + end.astimezone(u).strftime('%Y-%m-%dT%H:%M:%SZ'))
"
```

`TODAY_CENTRAL` is the date string to match against Notion (`date:Date:start`).
`WINDOW_START_UTC` / `WINDOW_END_UTC` are the Drive `createdTime` bounds — the full 24-hour Central day expressed in UTC. (During CDT this is `T05:00:00Z` → next-day `T05:00:00Z`; during CST it's `T06:00:00Z` → next-day `T06:00:00Z`.) Sanity check: the two bounds should always be exactly 24 hours apart and carry a `05`/`06` hour, never `00`/`23` — if they don't, the offset was dropped and the window is wrong.

## Step 1 — Get today's call pages (Central-time today)

Query the two **unfiltered** table views (NOT the server-side "Today" views — those filter by UTC and miss calls late in the Central day):

- ABA Calls (table): https://www.notion.so/[page-id]?v=[page-id]
- ABA Trainings (table): https://www.notion.so/[page-id]?v=[page-id]

Use `notion-query-database-view`. For each result row, keep only rows where `date:Date:start == $TODAY_CENTRAL`. If `has_more` is true, paginate with `start_cursor` until you've covered all rows. If both databases yield zero matching pages, stop and report "No calls today ($TODAY_CENTRAL) — nothing to link."

## Step 2 — For each page, check if it already has a transcript

Fetch each page with `notion-fetch`. If the page body already contains a `## Transcript` heading (or any docs.google.com link in a Transcript section), SKIP it — already done.

## Step 3 — Find the matching transcript in Google Drive

For each page that needs a transcript, search the Meet transcripts folder. Use the `google-drive-helper` skill's pattern:

Folder ID: `14fmJnjIU0Dj5xL9trSxOJe_vUTdhQOyV` (Meet transcripts)

Search query (substitute `$WINDOW_START_UTC` / `$WINDOW_END_UTC` from Step 0 and the attendee/company name from the Notion page title — strip suffixes like " - Intro Call", " - Check-in", " - Workshop", " - 1:1 Claude Workshop", and use just the first/given name):

```
parentId = '14fmJnjIU0Dj5xL9trSxOJe_vUTdhQOyV' and title contains '<name>' and createdTime > '<WINDOW_START_UTC>' and createdTime < '<WINDOW_END_UTC>'
```

Notes:
- Transcripts are titled `[Name or Company] / Shaw - [Type] (YYYY/MM/DD HH:MM TZ) - Transcript` — the date inside the title uses slash format (`YYYY/MM/DD`) and is already Central-local. The Drive search above matches on `createdTime`, so it doesn't depend on this; only use slashes if you ever match the date in the title directly.
- Only meetings Shaw organized are transcribed. Unscheduled instant meetings show a meeting code (e.g. `gdm-xxxx-xxx`) — those won't name-match; skip and surface.
- If multiple transcripts come back for one page, prefer the one whose time in the title is closest to the page's expected slot (if you can infer it from page content); otherwise list all candidates in the report and don't link.

## Step 4 — Link the transcript on the Notion page

Use `notion-update-page` with `command: insert_content`, `position: {"type": "end"}`, and this content (substitute the transcript title and viewUrl):

```
---
## Transcript
[<Transcript Title>](<viewUrl>)
```

The viewUrl is the `viewUrl` field returned by the Drive search — use it as-is, do NOT hand-rewrite. Use a plain external Markdown link, NOT `<mention-page>` (that's for internal Notion pages only).

## Step 5 — Report

Render the report with the `skimmable-summary` skill — it owns the title, stat line, one-sentence linked items, always-render empty states, and the action closer. Declare only the section map below. (Early exit: if Step 1 found no calls, just print "No calls today ($TODAY_CENTRAL) — nothing to link.")

Title: `# Transcript Linker — {Weekday, Mon D} (Central)`.
Stat line: `{N} linked · {N} skipped · {N} no-match`.

Sections, in order:
- ✅ Linked — [{Page title}]({page url}) → {transcript title}; empty: "Nothing new to link."
- ⏭️ Skipped — {Page title} — already had a transcript; empty: "None already linked."
- 🔴 Needs Your Attention [closer] — pages with no transcript in Drive yet, or ambiguous/multiple matches, so Shaw can investigate.

## Tools to load via ToolSearch on each run

- `mcp__[page-id]__notion-query-database-view`
- `mcp__[page-id]__notion-fetch`
- `mcp__[page-id]__notion-update-page`
- `mcp__[database-id]__search_files`

If any tool errors or the search returns unexpected shape, stop and report rather than guessing.
