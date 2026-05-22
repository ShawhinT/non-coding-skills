---
name: linkedin-post-analytics
description: Pull and analyze LinkedIn post performance data using Chrome tools. Use this skill whenever Shaw asks to check LinkedIn analytics, review post performance, compare posts across time periods, find top/bottom performers, compute engagement rates, or do any kind of LinkedIn content analysis. Triggers include "check my LinkedIn analytics", "how did my posts do", "LinkedIn performance", "post engagement", "top posts this month", "compare Q1 vs Q2 LinkedIn", or any mention of analyzing LinkedIn post data. Also trigger when Shaw wants to evaluate content strategy effectiveness on LinkedIn, even casually like "which posts worked best" or "what's getting reach on LinkedIn".
---

# LinkedIn Post Analytics

Pull per-post performance data from LinkedIn's creator analytics using Chrome tools, then analyze it. LinkedIn doesn't offer an export or API for per-post analytics — the only way to get the data is to scrape the analytics dashboard in-browser.

**Requires Chrome tools** (Claude in Chrome) — specifically `navigate`, `javascript_tool`, and `tabs_context_mcp`. If Chrome tools aren't available, tell Shaw to enable them.

## Skill Structure

```
linkedin-post-analytics/
├── SKILL.md                              ← You are here (workflow + URL system + scraping strategy)
├── scripts/
│   ├── scrape-impressions.js             ← Ready-to-run scraper for impressions view
│   ├── scrape-engagements.js             ← Ready-to-run scraper for engagements view
│   └── scrape-with-types.js              ← Impressions scraper + post type categorization + aggregation
└── references/
    ├── analysis-playbook.md              ← How to analyze data, present findings, common patterns
    └── troubleshooting.md                ← All known pitfalls and fixes
```

**Read the scripts before running them** — they have comments explaining the DOM patterns and metric interpretation. Read `references/analysis-playbook.md` before presenting findings. Consult `references/troubleshooting.md` if anything breaks.

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

**LinkedIn caps results at ~50 posts** per page load (the top 50 by the selected metric). Note this limitation in your analysis. For comprehensive data across long periods, break into monthly chunks.

**Lifetime vs window metrics.** Reaction and comment counts on the dashboard reflect lifetime totals for each post, but impressions are window-specific. For posts created before the analytics window opened, this distorts engagement-rate calculations (lifetime engagement / window impressions). When the goal is "engagement rate for the period," filter to posts published *within* the window — read each post card's age span (e.g., "2w", "3d") and exclude anything older than the window.

## Workflow

### Step 1: Clarify scope

Before scraping, understand what Shaw wants. Common patterns:

- **Single month review** → scrape one month, both views
- **Period comparison** → scrape multiple ranges, compute deltas
- **Top performers** → scrape a wide range, sort and filter
- **Post type analysis** → use `scrape-with-types.js`, aggregate by type
- **Engagement-rate ranking** → scrape both views, merge on activity ID, filter to posts created in the window

### Step 2: Navigate and scrape

Build the URL(s) from the parameters above. Run the matching script(s). If comparing periods, scrape each in sequence.

### Step 3: Analyze and present

Read `references/analysis-playbook.md` for detailed guidance on how to turn raw data into insights. The short version: lead with the key finding, back it up with specific numbers, show top/bottom performers, and give concrete recommendations tied to the data.

### If something breaks

Read `references/troubleshooting.md`. The most common issues are: page not loaded yet (retry after 2-3s), wrong scraper for the current view (check metricType in URL), tab ID mismatch (re-run tabs_context_mcp), and misinterpreting the engagements-view third column as reposts (it's totalEngagements).
