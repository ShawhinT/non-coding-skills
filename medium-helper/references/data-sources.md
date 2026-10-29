# Where the numbers in a post come from

All of these run in Chrome (Shaw's signed-in browser). Open a fresh tab per source and close it
when done. Each entry: URL, the one call that extracts the data, what to cross-check.

## Maven — cohort revenue

`https://maven.com/shaw-talebi/admin/courses/ai-builders-bootcamp/earnings`

Top tiles: lifetime earnings, total students, cohorts run. Left column lists every cohort with
revenue and dates (scrollable; `innerText` has all of them without scrolling).

```js
const t=document.body.innerText;
[...t.matchAll(/COHORT (\d+)\s+\$([\d,]+) USD\s+([A-Z]+ \d+, \d{4}) - ([A-Z]+ \d+, \d{4})/g)]
  .map(x=>x.slice(1).join(' | ')).join('\n')
```

Check: the cohort sum must equal the lifetime tile (it did: 8 cohorts → $87,667). Plot at each
cohort's **start** date. The ABB cohorts, for reference: C1 Nov 8 2024 $10,798 · C2 Jan 10 2025
$6,058 · C3 Feb 6 2025 $6,775 · C4 Apr 4 2025 $9,244 · C5 Jun 6 2025 $15,592 · C6 Aug 15 2025
$17,945 · C7 Oct 17 2025 $7,455 · C8 Jan 16 2026 $13,800.

## YouTube Studio — subscribers on a past date (exact)

Channel ID `UCa9gErQ9AE5jT2DZLjXBIdA`. Dashboard
(`studio.youtube.com/channel/<id>`) shows **current subscribers** in the Channel analytics tile.

Then `…/analytics/tab-overview` → the period dropdown (top right) → **Custom** → triple-click the
start-date text field, type `MM/DD/YY`, Tab, **Apply**. The Subscribers tile shows net change for the
range; click it then **See more** for the exact figure in the Advanced-mode table ("Total" row).
Subscribers on the start date = current − net change. Verified this gives the same answer as the
nearest Wayback snapshot (Oct 10 2024: 103,124 − 66,632 ≈ 36.5K vs 35.5K on Sep 27 2024).

Don't build the period URL by hand (`period-YYYY_MM_DD-…` 404s); the picker writes
`period-<ms>,<ms>` itself.

## Wayback Machine — Medium and YouTube follower counts on a past date

Navigate to `https://web.archive.org/web/<YYYYMMDD>/<url>`; Wayback redirects to the nearest
capture — the final URL carries the actual snapshot timestamp, so always read `location.href` and
report that date, not the one you asked for.

- YouTube: `https://www.youtube.com/@ShawhinTalebi` → `/[\d.,]+K? subscribers?/`. Captures are
  roughly monthly; the page needs ~4 s to render.
- Medium: `https://medium.com/@shawhin` redirects to `shawhin.medium.com` → `/[\d.,]+K? ?Followers?/`.
  Hundreds of captures, so the nearest one is usually within days.
- **LinkedIn: not available.** Every profile capture redirects to `linkedin.com/authwall`. Bracket
  it from SFC milestone posts instead and label the number as an estimate. (The Mar 10 2025 SFC
  post: crossed 10,000 with 20% arriving in 2 days → ~8K just before.)

The CDX index (`web.archive.org/cdx/search/cdx?…`) and `archive.org/wayback/available` are
blocked cross-origin from the page and were "temporarily offline" when tried; the redirect form
above is the reliable path. The donation banner covers the top ~175px of screenshots — remove
`#donato` via JS or crop it off.

## Notion — milestone posts (SFC database)

Data source `collection://[database-id]` (SFC = LinkedIn / YT community
posts). Milestones are page **titles** with a date; the bodies are usually blank.

```sql
SELECT "Name","date:Date:start",url FROM "collection://[page-id]"
WHERE ("Name" LIKE '%follower%' OR "Name" LIKE '%subs%' OR "Name" LIKE '%k %')
  AND "date:Date:start" BETWEEN '2024-01-01' AND '2025-06-30' ORDER BY "date:Date:start"
```

Known milestones: YT 10k Jan 17 2024 · YT 25k May 20 2024 · Medium 10k Sep 23 2024 · YT 40k Nov 18
2024 · YT 50k Feb 28 2025 · LinkedIn 10k Mar 10 2025 · newsletter 1000 Apr 4 2025 · YT 60k May 26
2025 · YT 100k ~Aug 2026. The "0 to 70k" timeline graphic in his Mar 2025 post puts YT 10k at Jul
2024 — the SFC dates above are the ones to trust.

Blog drafts themselves live in LFC (`collection://[page-id]`), title
`(Blog) <Title>`; newsletters in ABN.

## Kit — not useful for history

Broadcast history only reaches back to Sep 2025 on the first page and Shaw has said not to bother
with it for this.
