# Dashboard scraping (fallback path)

Everything needed to scrape LinkedIn's creator-analytics dashboard. This is the **fallback** — the Voyager feed API (`scripts/scrape-feed-api.js`) is the primary source and is what the recurring report uses. Come here only when the API is unavailable, or when you specifically need LinkedIn's `totalEngagements` metric (reactions + comments + reposts + clicks + saves), which the API does not expose.

## URL system

Every parameter is in the URL, so you can navigate directly to any date range and metric view — no clicking through the UI.

**Base URL:** `https://www.linkedin.com/analytics/creator/top-posts/`

| Param | Value | Notes |
|-------|-------|-------|
| `startDate` | `YYYY-MM-DD` | First day of range |
| `endDate` | `YYYY-MM-DD` | Last day of range |
| `metricType` | `IMPRESSIONS` or `ENGAGEMENTS` | Controls sort order and which metric is primary |
| `timeRange` | `custom` | Always use this when specifying dates |

**Examples:**
- March 2026, impressions: `?startDate=2026-03-01&endDate=2026-03-31&metricType=IMPRESSIONS&timeRange=custom`
- Q1 2026, engagements: `?startDate=2026-01-01&endDate=2026-03-31&metricType=ENGAGEMENTS&timeRange=custom`

To compare periods, navigate to each URL in sequence and scrape each.

## What the two views actually give you

The most important thing to understand before scraping. The two views look similar but report different metrics in their "third column," and the difference matters.

**Impressions view** — third column is **impressions** (times the post was shown). The standalone numbers in each post card are `[reactions, impressions]`.

**Engagements view** — third column is **LinkedIn's totalEngagements metric**: reactions + comments + reposts + clicks + saves + other interactions. The standalone numbers are `[reactions, totalEngagements]`. This third number is *not* the repost count, even though earlier versions of this skill assumed it was. Treating it as reposts inflates "shares" dramatically — a post with 1 actual repost can show 167 here because it had 166 clicks/saves/other interactions on top of reactions and comments.

**Repost counts are not reliable from either view.** The dashboard sometimes surfaces a "X reposts" text span and sometimes doesn't. For a true repost count on a specific post, open its page (`https://www.linkedin.com/feed/update/urn:li:activity:<id>/`) and read the count there.

## Which script to use

| Goal | Script | URL metricType |
|------|--------|---------------|
| Impressions + per-post reaction/comment counts | `scrape-impressions.js` | `IMPRESSIONS` |
| LinkedIn's totalEngagements per post | `scrape-engagements.js` | `ENGAGEMENTS` |
| Content strategy analysis by post type | `scrape-with-types.js` | `IMPRESSIONS` |

Mismatching the scraper to the view silently swaps the metrics — this is the #1 source of bad data. Check `metricType` in the current URL before you run anything.

## How to run a scraper

1. Call `tabs_context_mcp` to get the current tab ID
2. Use `navigate` to go to the analytics URL
3. Read the appropriate script from `scripts/`
4. Pass the script content to `javascript_tool` with the tab ID

**Always use `javascript_tool`, never `read_page` or `get_page_text`.** The analytics page is too large — both return full page content that exceeds tool output limits. The JS approach targets exactly the data you need.

Each script includes a 3-second page-load delay, so there's no need to wait or retry manually. If a scraper still returns 0 posts, the page structure may have changed — see `troubleshooting.md`.

## Merging the two views

For engagement-rate analysis you need both: the impressions view for the denominator, the engagements view for `totalEngagements` as the numerator (reactions + comments alone would undercount, since clicks and saves often dominate).

Navigating between the two URLs wipes every `window.*` global, so don't hold the first result in a `window` variable. The bundled scrapers persist to `localStorage` (`__imprData`, `__engData`) for exactly this reason. After the second scrape, read both keys back and merge by activity ID — extracted from the post `href`, which is stable and identical across views, unlike truncated preview text:

```javascript
const impr = JSON.parse(localStorage.getItem('__imprData') || '[]');
const eng  = JSON.parse(localStorage.getItem('__engData')  || '[]');
const engById = Object.fromEntries(eng.filter(e => e.activityId).map(e => [e.activityId, e]));
const rows = impr.map(d => ({ ...d, totalEng: (engById[d.activityId] || {}).totalEng ?? null }));
```

## Two limits that shape what you can conclude

**The ~50-post cap.** LinkedIn renders only the top ~50 posts per page load, sorted by the selected metric. Note this in any analysis. For ranges with more posts, break into monthly chunks — though month-by-month still misses anything outside the top 50 of each month. The feed API has no such cap, which is the main reason it's preferred.

**Lifetime vs window metrics.** Reaction and comment counts are lifetime totals; impressions are window-specific. For a post created before the window opened, an engagement rate computed from these mixes lifetime numerator with window denominator and comes out garbage. Filter to posts published *within* the window by reading each card's age span.

When you parse that age span, watch the unit: LinkedIn writes months as `mo` and minutes as `m`, so a regex alternation listing `m` first reads `10mo` as 10 minutes and lets a months-old post through. Order it `mo|yr|s|m|h|d|w`. Full explanation and the sanity check are in `troubleshooting.md` under "Age unit."

The feed API sidesteps both problems — it returns every post and dates each exactly from its activity-ID timestamp.
