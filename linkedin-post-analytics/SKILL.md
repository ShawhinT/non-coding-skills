---
name: linkedin-post-analytics
description: Pull and analyze LinkedIn post performance data using Chrome tools. Use this skill whenever Shaw asks to check LinkedIn analytics, review post performance, compare posts across time periods, find top/bottom performers, compute engagement rates, or do any kind of LinkedIn content analysis. Triggers include "check my LinkedIn analytics", "how did my posts do", "LinkedIn performance", "post engagement", "top posts this month", "compare Q1 vs Q2 LinkedIn", or any mention of analyzing LinkedIn post data. Also trigger when Shaw wants to evaluate content strategy effectiveness on LinkedIn, even casually like "which posts worked best" or "what's getting reach on LinkedIn". Also covers top-vs-bottom split breakdowns (halves by default, quartiles on request) and pulling complete post history (every post, exact metrics) via LinkedIn's feed API.
---

# LinkedIn Post Analytics

Pull per-post performance data from LinkedIn's creator analytics using Chrome tools, then analyze it. LinkedIn doesn't offer an export or API for per-post analytics — the only way to get the data is to scrape the analytics dashboard in-browser.

**Requires Chrome tools** (Claude in Chrome) — specifically `navigate`, `javascript_tool`, and `tabs_context_mcp`. If Chrome tools aren't available, tell Shaw to enable them.

## Skill Structure

```
linkedin-post-analytics/
├── SKILL.md                              ← You are here (workflow + URL system + scraping strategy)
├── scripts/
│   ├── scrape-feed-api.js                ← PRIMARY: every post, exact metrics, via the Voyager feed API
│   ├── scrape-impressions.js             ← Dashboard fallback: impressions view (top ~50)
│   ├── scrape-engagements.js             ← Dashboard fallback: engagements view (totalEngagements)
│   └── scrape-with-types.js              ← Impressions scraper + post type categorization + aggregation
└── references/
    ├── analysis-playbook.md              ← How to analyze data, present findings, common patterns
    └── troubleshooting.md                ← All known pitfalls and fixes
```

**Read the scripts before running them** — they have comments explaining the DOM patterns and metric interpretation. Read `references/analysis-playbook.md` before presenting findings. Consult `references/troubleshooting.md` if anything breaks.

## Two ways to get the data (pick based on the question)

1. **Voyager feed API (preferred for any window / engagement-rate / split analysis, and the recurring report).** LinkedIn's own internal GraphQL feed returns *every* post you published, with exact `numImpressions`, `numLikes`, `numComments`, and `numShares` per post. Not capped at 50, not distorted by lifetime-vs-window mixing. Use `scripts/scrape-feed-api.js`.
2. **Dashboard scraping (`scrape-*.js`).** Faster for a quick look and the only source for the dashboard's `totalEngagements` metric (which includes clicks/saves). But capped at the top ~50 by the selected metric and needs two views merged. Use as a fallback.

### Voyager feed API — how it works

Run `scripts/scrape-feed-api.js` on `https://www.linkedin.com/in/me/recent-activity/all/` (read it first). What it relies on:

- **Auth:** the `csrf-token` header is the `JSESSIONID` cookie value; the profile URN is in the page HTML (`urn:li:fsd_profile:...`); the queryId is `voyagerFeedDashProfileUpdates.<hash>`. If the call 404s the hash has rotated — capture a live one from the network log (see troubleshooting).
- **Token-based pagination.** `start` alone does nothing; pass the `paginationToken` from the previous response (`data.data.feedDashProfileUpdatesByMemberShareFeed.metadata.paginationToken`). Page until the oldest post predates the window.
- **Per-post metrics** are in `SocialActivityCounts` entities in `included[]`, keyed by activity URN: `numImpressions`, `numLikes`, `numComments`, `numShares`.
- **Verbatim copy + media type, same response.** Each update's full post text is in `commentary.text.text` (the complete body, not just the preview), and any attached media shows up as the populated component under `content` — `imageComponent`, `linkedInVideoComponent`, `articleComponent`, or `documentComponent`. Handy when repurposing a post to another channel: carry the exact wording and flag whether the post needs its image re-attached.
- **Exact dates, no age-string parsing.** Creation time is encoded in the activity ID: `new Date(Number(BigInt(id) >> 22n))`. This replaces the fragile "2w/3mo" byline parsing the dashboard scrapers need.
- **Original vs. repost.** A repost of someone else's content has no matching `SocialActivityCounts` (null counts) — filter those out, they aren't your posts.

The DOM is not a viable fallback here: the feed virtualizes to ~5 nodes and the "Show more results" button resists synthetic clicks. Call the API.

### Two different engagement metrics — don't conflate them

- **API rate = (reactions + comments + shares) / impressions.** What the feed API gives you. Excludes clicks/saves.
- **Dashboard totalEngagements rate** (`scrape-engagements.js`) includes clicks/saves/other, so it is always higher.

Pick one and label it. The recurring split report uses the **API rate** (exact and complete). Never present an API rate beside a dashboard rate as if they were the same number.

### Recency caveat

Impressions accrue over several days. A post from the last ~2–3 days has immature reach and looks artificially low. When ranking or bucketing, exclude the last 2–3 days or flag those rows as "still maturing" — don't call a day-old post a loser.


## LinkedIn Analytics URL System

Every parameter is in the URL, so you can navigate directly to any date range and metric view — no clicking through the UI.

**Base URL:** `https://www.linkedin.com/analytics/creator/top-posts/`

**Parameters:**

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

This is the most important thing to understand before scraping. The two views look similar but report different metrics in their "third column," and the difference matters.

**Impressions view** — third column is **impressions** (the count of times the post was shown). The standalone numbers in each post card are `[reactions, impressions]`.

**Engagements view** — third column is **LinkedIn's total engagements metric**: reactions + comments + reposts + clicks + saves + other interactions. The standalone numbers are `[reactions, totalEngagements]`. This third number is *not* the repost count, even though earlier versions of this skill assumed it was. Treating it as reposts inflates "shares" dramatically (e.g., a post with 1 actual repost can show 167 in this column because it had 166 clicks/saves/other interactions on top of reactions and comments).

**Repost counts are not reliable from either view.** The dashboard sometimes surfaces a "X reposts" text span and sometimes doesn't. If you need a true repost count for a specific post, navigate to that post's URL (`https://www.linkedin.com/feed/update/urn:li:activity:<id>/`) and read the count from the post page itself.

## Scraping Strategy

**Always use `javascript_tool`, never `read_page` or `get_page_text`.** The analytics page is too large — both return full page content that exceeds tool output limits. The JS approach targets exactly the data you need and returns compact structured output.

### Which Script to Use

| Goal | Script | URL metricType |
|------|--------|---------------|
| Impressions + per-post reaction/comment counts | `scrape-impressions.js` | `IMPRESSIONS` |
| LinkedIn's totalEngagements per post | `scrape-engagements.js` | `ENGAGEMENTS` |
| Content strategy analysis by post type | `scrape-with-types.js` | `IMPRESSIONS` |

The metric interpretation differs between views — this is the #1 source of bad data. Match the right script to the right `metricType` and pay attention to what each "third column" number actually means (see the section above).

### How to Run a Scraper

1. Call `tabs_context_mcp` to get the current tab ID
2. Use `navigate` to go to the LinkedIn analytics URL
3. Read the appropriate script from `scripts/`
4. Pass the script content to `javascript_tool` with the tab ID

Each script includes a 3-second page-load delay, so there's no need to manually wait or retry. If a scraper still returns 0 posts, the page may have changed structure — see `references/troubleshooting.md`.

**Always scrape both views for engagement-rate analysis.** Impressions view gives you the denominator (impressions). Engagements view gives you the correct numerator (LinkedIn's totalEngagements, which includes clicks/saves and is what you want — using just reactions + comments would undercount). Match posts across views by activity ID extracted from the post link, or by a normalized preview-text key.

Scraping both views means navigating between two URLs, and navigating wipes every `window.*` global on the page. Don't hold the first view's result in a `window` variable expecting it to survive — the bundled scrapers persist their output to `localStorage` (`__imprData`, `__engData`) for exactly this reason. After scraping the second view, read both keys back from `localStorage` and merge by activity ID:

```javascript
const impr = JSON.parse(localStorage.getItem('__imprData') || '[]');
const eng  = JSON.parse(localStorage.getItem('__engData')  || '[]');
const engById = Object.fromEntries(eng.filter(e => e.activityId).map(e => [e.activityId, e]));
const rows = impr.map(d => ({ ...d, totalEng: (engById[d.activityId] || {}).totalEng ?? null }));
```

**LinkedIn caps results at ~50 posts** per page load (the top 50 by the selected metric). Note this limitation in your analysis. For comprehensive data across long periods, break into monthly chunks.

**Lifetime vs window metrics.** Reaction and comment counts on the dashboard reflect lifetime totals for each post, but impressions are window-specific. For posts created before the analytics window opened, this distorts engagement-rate calculations (lifetime engagement / window impressions). When the goal is "engagement rate for the period," filter to posts published *within* the window — read each post card's age span (e.g., "2w", "3d") and exclude anything older than the window.

The age span lives inside the byline ("... posted this • 2w"), not a standalone span, and the unit is where this bites: LinkedIn writes **months as `mo`** and **minutes as `m`**. If you match units with a regex alternation, put `mo` and `yr` before `m` (e.g. `mo|yr|s|m|h|d|w`) — otherwise `10mo` matches the `m` branch first, gets read as `10m` (10 minutes), and a months-old post silently passes a same-week window filter and corrupts its rate. A post is in-window when its age is `now` or `Nd`/`Nw`/`Nh`/`Nm`; exclude `Nmo` and `Nyr`.

## Workflow

### Step 1: Clarify scope

Before scraping, understand what Shaw wants. Common patterns:

- **Single month review** → scrape one month, both views
- **Period comparison** → scrape multiple ranges, compute deltas
- **Top performers** → scrape a wide range, sort and filter
- **Post type analysis** → use `scrape-with-types.js`, aggregate by type
- **Engagement-rate ranking** → scrape both views, merge on activity ID, filter to posts created in the window
- **Top/bottom split (default for the recurring report)** → pull all posts via the feed API, split into top and bottom halves (50%) by engagement rate, and contrast them. The "Top/Bottom Split workflow" section below is the single source of truth for this report — follow it, don't restate it.

### Step 2: Navigate and scrape

Build the URL(s) from the parameters above. Run the matching script(s). If comparing periods, scrape each in sequence.

### Step 3: Analyze and present

Read `references/analysis-playbook.md` for detailed guidance on how to turn raw data into insights. The short version: lead with the key finding, back it up with specific numbers, show top/bottom performers, and give concrete recommendations tied to the data.

## Top/Bottom Split workflow (single source of truth for the recurring report)

This section is the one definition of the recurring report. The Saturday scheduled task and any ad-hoc "how are my posts doing" request both run this — they should point here, not restate the window, split, columns, or caveats. The contrast between best and worst is where the lesson lives — it beats a flat ranked table.

1. **Window:** trailing 28 days, ending today (Shaw's local timezone).
2. **Pull all posts** via the feed API (`scrape-feed-api.js`). Original posts only; date each from its activity-ID timestamp; keep those created inside the 28 days.
3. **Compute** engagement rate = (reactions + comments + shares) / impressions per post.
4. **Bucket:** sort by rate; split into the top 50% and bottom 50% — the two halves, split at the median (with an odd count, note where the middle post lands). This is the default. Quartiles (top/bottom 25%) are a tighter-contrast alternative when Shaw asks for one.
5. **Present:**
   - One-line summary: N posts, top-half avg rate vs bottom-half avg.
   - Two tables (top, bottom): date, eng %, impressions, reactions, comments, shares, preview linked to `https://www.linkedin.com/feed/update/urn:li:activity:<id>/`.
   - A short "what separates them" read — hook type, audience, governance, format — grounded in the actual posts, never generic.
   - The **reach-vs-rate check**: is high reach correlated with high engagement rate or decoupled? (In practice nearly decoupled — the single widest post is often the lowest-rate.)
   - Apply the recency caveat: flag any last-2–3-day posts whose reach is still maturing.

For the deeper "why did these win/lose" content lens (sponsor vs champion, the barbell) and for turning findings into post ideas, that lives with Shaw's content strategy and the `sfc-helper` skill. This skill produces the numbers and the first-order read; idea generation is `sfc-helper`'s job.


### If something breaks

Read `references/troubleshooting.md`. The most common issues are: page not loaded yet (retry after 2-3s), wrong scraper for the current view (check metricType in URL), tab ID mismatch (re-run tabs_context_mcp), and misinterpreting the engagements-view third column as reposts (it's totalEngagements).
