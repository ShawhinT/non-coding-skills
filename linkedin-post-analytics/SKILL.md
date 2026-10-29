---
name: "linkedin-post-analytics"
description: Pull and analyze LinkedIn post performance data using Chrome tools. Use this skill whenever Shaw asks to check LinkedIn analytics, review post performance, compare posts across time periods, find top/bottom performers, compute engagement rates, or do any kind of LinkedIn content analysis. Triggers include "check my LinkedIn analytics", "how did my posts do", "LinkedIn performance", "post engagement", "top posts this month", "compare Q1 vs Q2 LinkedIn", or any mention of analyzing LinkedIn post data. Also trigger when Shaw wants to evaluate content strategy effectiveness on LinkedIn, even casually like "which posts worked best" or "what's getting reach on LinkedIn". Also covers top-vs-bottom split breakdowns (halves by default, quartiles on request), delivered as a standalone HTML dashboard, and pulling complete post history (every post, exact metrics) via LinkedIn's feed API.
---

# LinkedIn Post Analytics

Pull per-post performance data from LinkedIn using Chrome tools, then analyze it. LinkedIn offers no export or public API for per-post analytics — the data has to come out of the browser.

**Requires Chrome tools** (Claude in Chrome) — specifically `navigate`, `javascript_tool`, and `tabs_context_mcp`. If Chrome tools aren't available, tell Shaw to enable them.

## Skill Structure

```
linkedin-post-analytics/
├── SKILL.md                              ← You are here (feed API + the recurring split report)
├── scripts/
│   ├── scrape-feed-api.js                ← PRIMARY: every post, exact metrics, via the Voyager feed API
│   ├── scrape-impressions.js             ← Dashboard fallback: impressions view (top ~50)
│   ├── scrape-engagements.js             ← Dashboard fallback: engagements view (totalEngagements)
│   ├── scrape-with-types.js              ← Impressions scraper + post type categorization + aggregation
│   ├── build_split_config.py             ← The recurring report: posts.json + prose.json → dashboard (computes every number)
│   └── aba_dashboard.py                  ← Generic ABA dashboard renderer: JSON config → styled HTML (brand shell lives here)
└── references/
    ├── dashboard-fallback.md             ← The whole dashboard path: URLs, views, scripts, merging, caps
    ├── analysis-playbook.md              ← How to analyze data, present findings, common patterns
    ├── profile-baselines.md              ← Weekly profile viewers / followers / connection requests — baselines for off-LinkedIn CTAs
    └── troubleshooting.md                ← All known pitfalls and fixes
```

**Read the scripts before running them** — they have comments explaining the DOM patterns and metric interpretation. Read `references/analysis-playbook.md` before presenting findings. Consult `references/troubleshooting.md` if anything breaks.

## Two ways to get the data (pick based on the question)

1. **Voyager feed API — the default.** LinkedIn's own internal GraphQL feed returns *every* post you published, with exact `numImpressions`, `numLikes`, `numComments`, and `numShares` per post. Not capped at 50, not distorted by lifetime-vs-window mixing. Use `scripts/scrape-feed-api.js`. This is what the recurring report runs, and what any window / engagement-rate / split analysis should use.
2. **Dashboard scraping — the fallback.** Faster for a quick look, and the only source for LinkedIn's `totalEngagements` metric (which includes clicks and saves). But capped at the top ~50 by the selected metric, and it needs two views merged. See `references/dashboard-fallback.md`.

### Voyager feed API — how it works

Run `scripts/scrape-feed-api.js` on `https://www.linkedin.com/in/me/recent-activity/all/` (read it first). What it relies on:

- **Auth:** the `csrf-token` header is the `JSESSIONID` cookie value; the profile URN comes from the page HTML (`urn:li:fsd_profile:...`) when it's there and from `/voyager/api/me` when it isn't; the queryId is `voyagerFeedDashProfileUpdates.<hash>`. If the call 404s the hash has rotated — capture a live one from the network log (see troubleshooting).
- **Token-based pagination.** `start` alone does nothing; pass the `paginationToken` from the previous response (`data.data.feedDashProfileUpdatesByMemberShareFeed.metadata.paginationToken`). Page until the oldest post predates the window.
- **Per-post metrics** are in `SocialActivityCounts` entities in `included[]`: `numImpressions`, `numLikes`, `numComments`, `numShares`. A post's counts can be keyed by either of its two urns — `urn:li:activity:<id>` for most, `urn:li:ugcPost:<id>` for others (scheduled posts among them), and the update's `*socialDetail` names which one. Join on both. Joining on the activity urn alone once dropped four of twenty posts, the month's top post among them, and nothing errored — the scraper reports any original post still missing counts as `unmatched`, which should be empty.
- **Verbatim copy + media type, same response.** Each update's full post text is in `commentary.text.text` (the complete body, not just the preview), and any attached media shows up as the populated component under `content` — `imageComponent`, `linkedInVideoComponent`, `articleComponent`, `documentComponent`, or `pollComponent`. Handy when repurposing a post to another channel: carry the exact wording and flag whether the post needs its image re-attached. The scraper returns this as `media` on every row and rolls it up as `byMedia` in the summary, so format is something you aggregate, not something you eyeball.
- **Exact dates, no age-string parsing.** Creation time is encoded in the activity ID: `new Date(Number(BigInt(id) >> 22n))`. This replaces the fragile "2w/3mo" byline parsing the dashboard scrapers need.
- **Original vs. repost.** A repost of someone else's content carries `resharedUpdate`, or — for a repost with commentary — a `*socialDetail` thread pointing at a different activity id. A plain repost carries neither, and its thread is the original's ugcPost, indistinguishable by urn shape from an original's second urn — authorship gives it away (the update's actor isn't Shaw), so the scraper checks that too. Identify reposts by these signals, not by missing counts: missing counts is also what an original keyed by its other urn looks like.

The DOM is not a viable fallback here: the feed virtualizes to ~5 nodes and the "Show more results" button resists synthetic clicks. Call the API.

### Two different engagement metrics — don't conflate them

- **API rate = (reactions + comments + shares) / impressions.** What the feed API gives you. Excludes clicks/saves.
- **Dashboard totalEngagements rate** (`scrape-engagements.js`) includes clicks/saves/other, so it is always higher.

Pick one and label it. The recurring split report uses the **API rate** (exact and complete). Never present an API rate beside a dashboard rate as if they were the same number.

**Poll votes are in neither rate.** A vote is the response a poll asks for, so a poll's rate understates it — 58 votes on a 1.57% poll made it the month's most-answered post. The scraper carries the vote total (`votes`, from the poll's `PollSummary` entity) and the dashboard prints it in the format cell; read a poll by its rate *and* its votes rather than ranking it on rate alone.

### Recency caveat

Impressions accrue over several days. A post from the last ~2–3 days has immature reach and looks artificially low. When ranking or bucketing, exclude the last 2–3 days or flag those rows as "still maturing" — don't call a day-old post a loser.

**Reach and engagement mature on different clocks**, which matters when re-checking the same post over time. A campaign post tracked across Aug 9→11 went 413→457 impressions with *zero* new reactions, comments, or link clicks. So a later re-pull typically lowers the engagement rate without any new engagement — the denominator kept growing. When reporting a refresh, say which number actually moved rather than presenting a falling rate as a decline in performance.

### Single-post refresh

For campaign tracking, the question is usually "how is *this* post doing now," not "rank my month." Pull the feed API over the campaign's date range, then identify the post by its opening line (`preview`) rather than by position or date alone — Shaw often posts more than once a day.

Judge it against **his own recent median, not an absolute benchmark.** A post at 457 impressions means nothing until you know his August median was ~523 (below par) and that a milestone post the day before hit 8,748. Pull the surrounding window in the same call so the comparison is free. Report reach against the median and engagement rate against the median separately — a post can be strong on one and weak on the other, and for a campaign the actionable read is usually *distribution failed* vs *the hook failed*.

## Workflow

### Step 1: Clarify scope

Before scraping, understand what Shaw wants. Common patterns:

- **Single month review** → one month via the feed API
- **Period comparison** → pull multiple ranges, compute deltas
- **Top performers** → pull a wide range, sort and filter
- **Post type analysis** → aggregate the `byMedia` rollup, or use `scrape-with-types.js` on the dashboard
- **Engagement-rate ranking** → feed API, filter to posts created in the window
- **Campaign tracking — refresh one post's numbers** → feed API over a narrow window (the campaign's dates), then match the post by its opening line. See "Single-post refresh" below.
- **Top/bottom split (default for the recurring report)** → pull all posts via the feed API, split into top and bottom halves (50%) by engagement rate, and contrast them. The "Top/Bottom Split workflow" section below is the single source of truth for this report — follow it, don't restate it.

### Step 2: Pull the data

Default to `scripts/scrape-feed-api.js` on the recent-activity page, setting `window.__START` / `window.__END` for the window. Only drop to the dashboard path in `references/dashboard-fallback.md` if the API is unavailable or you need `totalEngagements`.

### Step 3: Analyze and present

Read `references/analysis-playbook.md` for detailed guidance on how to turn raw data into insights. The short version: lead with the key finding, back it up with specific numbers, show top/bottom performers, and give concrete recommendations tied to the data.

## Top/Bottom Split workflow (single source of truth for the recurring report)

This section is the one definition of the recurring report. The Saturday scheduled task and any ad-hoc "how are my posts doing" request both run this — they should point here, not restate the window, split, columns, or caveats. The contrast between best and worst is where the lesson lives — it beats a flat ranked table.

1. **Window:** trailing 28 days, ending today (Shaw's local timezone).
2. **Pull all posts** via the feed API (`scrape-feed-api.js`). Original posts only; date each from its activity-ID timestamp; keep those created inside the 28 days.
3. **Compute** engagement rate = (reactions + comments + shares) / impressions per post.
4. **Bucket twice — both splits run every time.** The report is not complete with one of them.
   - **Split A — by engagement rate.** Sort by rate, halve at the median.
   - **Split B — by reach.** Sort by impressions, halve at the median.

   Run both because they answer different questions and, on Shaw's account, tend to come out close to inverse: sorting by reach roughly sorts *against* rate. Presenting only Split A hides which posts actually got seen; only Split B hides which posts actually landed. The gap between the two orderings is itself the finding — it says reach and resonance are being produced by different kinds of post, and a single leaderboard would blur them into a ranking that recommends nothing. Quartiles are a tighter-contrast alternative for either split when Shaw asks.
5. **Present** — as a standalone HTML dashboard, not a chat message, and generated rather than hand-written. Dump the feed rows to `posts.json` (add a short `title` per post; a five-word title reads better than a clipped preview), write the prose that a number can't carry to `prose.json`, and run `scripts/build_split_config.py posts.json prose.json out.html`. It computes every number — rates, halves, medians, averages, max, shares, the dual-median intersection, the switch count — and prints them, so the sanity check is reading its output, not re-deriving figures by hand. The rendering itself is `scripts/aba_dashboard.py`, a generic JSON-config-to-HTML renderer that holds the brand shell in one place; it is the same renderer any other ABA dashboard should use, so a layout change is made there once. Save the output to the outputs folder and present the file, with two or three lines of summary in chat. It is meant to be opened in a browser rather than the in-app canvas — the canvas sandbox silently blocks `target="_blank"`, so the post links die there.

   Four things about the layout are load-bearing; the builder enforces them, and a change to the builder should preserve them:
   - **One table pair with a toggle between the splits**, rather than both splits printed in sequence. The two splits answer different questions and tend to come out near-inverse, so making the switch an action rather than a scroll is what surfaces the disagreement between the two orderings.
   - **The summary row swaps with the split.** Rate shows top-half and bottom-half averages (a rate is a bounded ratio, so its mean is meaningful); reach shows median, max, the top post's share of total impressions, and max/median. This is the fat-tail rule below enforced structurally: the dashboard has no slot in which to print an average reach.
   - **Tables stack vertically at a capped column width**, never side by side. The post title is the column doing the interpretive work, and two columns compress it into uselessness.

   - **The filter hides rows and never recomputes.** The bar above the tables takes a min/max on engagement rate and on impressions — the two metrics the splits sort by — and filters every table on the page, surviving the toggle. The summary row, medians and halves stay computed over the full window, because a post is in the top half by beating the *real* median; re-deriving them from whatever survived a filter would make the labels lie while the numbers drift under the reader. The counter states the visible subset (`showing 4 of 76 posts`) so the distinction is legible on screen, and a table emptied by the filter says so rather than rendering blank. `filters` in the config declares the metrics; each row carries its unformatted values in `_f`, because the cells hold formatted text.

   What the dashboard has to contain (the builder lays all of it out; the prose fields in `prose.json` are yours to write):
   - **Table columns**: date, eng %, impressions, reactions, comments, shares, format, repurposed, title linked to `https://www.linkedin.com/feed/update/urn:li:activity:<id>/`. Order the columns so the split's sort key comes first.
   - **Repurpose status rides on every row.** Whether a post has already been re-run on another channel (an SFC row whose `Channel` isn't LinkedIn) or carried into a newsletter send is a property of the post, not a decoration on the shortlist — "what should I run again?" is a question about every post in the window, and it is reliably the first question a table of them provokes. Reading it across the full table is also the only way to see *how* the repost queue is being fed: when the repurposed posts cluster in one half, the selection is running on reach or recency rather than on what actually landed, and a two-row shortlist cannot show you that. It costs one query against the SFC database plus a scan of recent sends. `sfc-helper` owns the repurposing itself; the *status* belongs here, next to the numbers that motivate it.

     The status is a **channel name or `No`** — `No`, `YTC`, `ABN`, `ABN/YTC` — keyed by activity ID under `repurposed` in `prose.json`, and it describes **the row's own post**. A repurpose of a different post is not this post's status, however adjacent: same theme, same week, or a neighbouring post in the same series still means `No` for this row. Hedge labels like "adjacent only" read as a partial yes and quietly break the decision the table exists to support, which is whether *this* post has been run again. Resolve an ambiguous match by opening the repurposed item and reading which activity ID it links back to — matching on theme is what produces the hedge. That link is strong evidence, not proof: a LinkedIn URL in the `.../posts/...-share-<id>-...` form carries a *different* urn than the `activity-<id>` form, so its id can resolve to no post in the pull at all. When the linked id matches nothing you fetched, fall back to a verbatim opening-line comparison against the candidate posts and say in the report which one you matched on — a link that points nowhere is a reason to check the text, not to record a miss.
   - A short "what separates them" read — hook type, audience, governance, format — grounded in the actual posts, never generic. Format is the one dimension you get for free: quote the `byMedia` rollup (avg rate by image/video/article/text) rather than asserting a format effect from impression.
   - The **reach-vs-rate check**: is high reach correlated with high engagement rate or decoupled? (In practice nearly decoupled — the single widest post is often the lowest-rate.) When a post's reach is an order of magnitude above the median, report its **absolute** engagement next to its rate and say which one you're reading. A post that escapes the immediate network is being shown to a colder audience, so a low rate there is measuring audience fit, not post quality — it can be the month's worst by rate while carrying more raw interactions than the entire top half. Ranking it last without that caveat is a wrong call dressed as a number.
   - A cross-read of the two splits: which posts changed halves, and what that says about which mechanism produced their numbers.
   - **The dual-median table** — the posts in the top half of *both* splits, presented every time rather than on request. It's small by construction (4 of 26 in a typical month) and that's what makes it useful: a post only lands here if it traveled past the median *and* resonated above it, which excludes the milestones that buy reach without argument and the in-network posts that earn rate without escaping. Same columns as Split A, sorted by rate. The read should name the mechanism that got a post into both halves — a contrarian claim people forwarded, a utility artifact people tagged someone on — because this is the shortlist of shapes worth running again, and "it scored well on both" isn't a shape. If the intersection is empty or a single post, say so plainly; that's a finding about the month, not a broken table.
   - **Prose earns its place only where a number can't.** The dashboard carries the numbers; keep it to the "what separates them" read per split, plus one paragraph and at most one bullet per post under the dual-median table. Don't restate what a column already shows — the date column carries recency, so a still-maturing post needs no flag, and a table sorted by rate needs no sentence explaining that it is sorted by rate.

### Reach is fat-tailed — investigate outliers, never strip them

Impressions are not normally distributed. A single post routinely takes 20-50% of a month's total reach, and max-over-median ratios above 10x are ordinary. That shape has a hard consequence for how you report:

**Never write "excluding the outlier, the average is X."** In a fat-tailed distribution the outlier is not contamination of the average — it *is* the month. Removing it deletes the only observation carrying information about the tail, and the tail is where nearly all the value sits. A sentence like "strip out the top post and average reach drops to 2,174" reads as rigor but is precisely backwards: it discards the signal and reports the noise. The same reflex to distrust the mean is right; the fix is to stop using the mean, not to trim the data until the mean behaves.

**Report the shape instead of the center.** For reach, give median (the typical post), max (the tail event), the top post's and top three's share of total impressions, and max/median. These describe a fat-tailed sample honestly; a mean does not. Rate is different — it's bounded above and much thinner-tailed, so averaging halves is fine there.

**Then interrogate the tail post rather than averaging it away.** Pull its full text (`commentary.text.text`) and ask:
- What belief did it contradict, and whose? Tail posts usually take a position the reader already holds an opposing view on — a decade of "SaaS beats services," a norm like "stuff your CLAUDE.md with rules" — and make the contradiction specific and falsifiable with a number or an artifact.
- Which mechanism carried it? Disagreement (people reply to argue), utility (people tag someone who needs it), and personal milestone (people congratulate) are different generators that all produce tail reach. Don't merge them into one lesson — a milestone post's reach doesn't transfer to your next thesis post.
- What's its comment-to-reaction ratio against the corpus baseline? Comments are the strongest distribution signal on LinkedIn, so a tail post running well above the month's baseline tells you the reach came from replies rather than passive impressions.
- Has this shape hit before? One tail event is an anecdote; the same shape twice is a repeatable format.

**Frame the strategy question correctly.** With fat tails the goal isn't raising the average post — most posts contribute almost nothing by construction and that is not a failure. It's how many genuine tail attempts were taken, and what the hits had in common. Report the count of tail-shaped posts, not just their outcomes.

For the deeper "why did these win/lose" content lens (sponsor vs champion, the barbell) and for turning findings into post ideas, that lives with Shaw's content strategy and the `sfc-helper` skill. This skill produces the numbers and the first-order read; idea generation is `sfc-helper`'s job.

### Profile-level series

For profile viewers, new followers, or connection requests by week (e.g. measuring a YouTube CTA that links to the profile), read `references/profile-baselines.md`.

### If something breaks

Read `references/troubleshooting.md`. The most common issues are: an un-awaited async IIFE returning `{}`, a rotated feed-API queryId, `javascript_tool` output truncating on long previews, and tab ID mismatch (re-run `tabs_context_mcp`).
