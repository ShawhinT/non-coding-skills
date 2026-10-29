# Analysis Playbook

How to turn scraped LinkedIn data into actionable insights. Read this after scraping — the scraping skill handles getting the data, this handles making sense of it.

## The two numbers that matter

Every post has **impressions** as the denominator, but there are two different numerators and they are not interchangeable:

- **API rate = (reactions + comments + shares) / impressions.** From the feed API. Excludes clicks and saves. This is the default and what the recurring split report uses — it's exact, complete, and available for every post.
- **Dashboard rate = totalEngagements / impressions.** From the engagements view. Includes clicks and saves, so it is always the larger number, and it's capped at the top ~50 posts.

Pick one per analysis and label which it is. Never place the two side by side as if they were the same metric — the dashboard rate will look like an improvement when it's just a wider definition. `SKILL.md` is the source of truth for this distinction.

Reactions and comments alone are a useful breakdown but not the full picture. Reposts specifically are unreliable from either dashboard view; if a particular post's repost count matters, visit the post page directly.

## Common Analysis Patterns

### Single Month Review

"How did March go?"

Scrape one month with both impressions and engagements views. Merge by activity ID. Report:
- Total impressions and total engagements (LinkedIn metric)
- Average impressions per post
- Engagement rate (total engagements / total impressions)
- Reactions-to-comments ratio — proxy for "did the post spark discussion vs just nods"
- Top 5 and bottom 5 performers by engagement rate AND by impressions (these often disagree)

Filter to posts published within the month — older posts that received impressions during the window will distort the math (their reaction/comment counts are lifetime, not month-specific).

### Period Comparison

"Compare Q4 vs Q1"

Scrape each period separately. For each, compute the same aggregate metrics, then calculate deltas:
- Median impressions per post (median is more stable than mean when outlier posts skew things)
- Engagement rate shift
- Changes in what content types perform best
- New patterns in top performers (e.g., "specific number hooks now dominate the top 5")

### Post Type Analysis

"Are promos underperforming?"

Use `scrape-with-types.js` to categorize and aggregate. Compare:
- Average impressions per type
- Which types over/under-index relative to their share of posts
- Type mix shifts between periods (e.g., "you posted 3x more promos in March but they got 2x fewer impressions each")

### Engagement-rate ranking

"Which posts had the highest engagement rate?"

This is the most-asked question and the easiest one to get wrong. Process:
1. Scrape impressions view → impressions per post
2. Scrape engagements view → totalEngagements per post
3. Match across views by activity ID
4. Filter to posts created within the analysis window (read the age span from each card)
5. Compute `totalEngagements / impressions`, sort descending

If you skip step 4, a post from a year ago with a few hundred recent impressions and lifetime reactions baked in will look impossibly high.

## Known Performance Patterns

Patterns that have been validated by real data across multiple analysis runs. Use these as baselines when interpreting new results — they're the "what we already know" that makes new findings meaningful.

### Curated listicles are Shaw's highest-ceiling format

Posts that curate resources with a specific number hook ("10 YouTube channels that...") consistently produce the most total engagement and have the longest shelf lives. These posts are save-worthy, repost-worthy, and people keep discovering and sharing them months later. When analyzing top performers, expect curated listicles to dominate the all-time tally even if they're not in this period's top posts.

### Personal milestones drive impressions differently

Milestone posts (moving, birthday recaps, career announcements) get massive reach through reactions and comments — people engage emotionally. These are relationship-builders. They can be top-3 by impressions but their utility for sustained reach is lower than curated lists.

### Base reach and breakout are separated by a wide gap

State this one in ratios, not absolute impression counts — Shaw's baseline moves with audience size and LinkedIn's distribution changes, so any hard number written here goes stale and makes ordinary months read as collapses. Compute the baseline from the current pull instead.

The durable shape: most posts cluster in a narrow band around the median, and breakout posts land an order of magnitude above it (max/median above 10x is routine, and the single top post commonly takes 20–50% of the window's total reach). There's no "doing slightly better" — there's base reach and there's breakout, and they're produced by different mechanisms. Breaking out takes a trigger: a shareable format, an emotional or milestone hook, or a specific falsifiable number in the opening line.

## Presenting Findings

Lead with the key insight, not the raw data. Shaw wants to know what to do differently — not just what the numbers are.

### Structure

1. **Headline finding** — the single most important thing (e.g., "Workflow posts about Claude had the highest engagement rate in May — 3 of your top 5 were 'how I use Claude for X' format")
2. **Supporting data** — 2-3 specific numbers that back up the headline
3. **Top/bottom performers** — with post previews so Shaw can recognize them and pattern-match
4. **Recommendations** — concrete changes to content strategy, if the data suggests any

### What Good Recommendations Look Like

- "Your opinion/thesis posts get 3x more impressions than promos. Consider framing more promos as opinion posts with a CTA buried at the end."
- "Posts with specific dollar amounts or numbers in the hook ($254, $160/mo, 29 days) consistently outperform abstract hooks."
- "Your top engagement-rate posts this period are all first-person workflow stories ('I delegated 15 hr/wk to Claude'). Lists and frameworks underperformed by ~2x."

Avoid vague advice like "post more engaging content" or "try different approaches." Ground everything in the actual data.

## Cross-Referencing with linkedin-post-writer

When analyzing post performance, reference Shaw's `linkedin-post-writer` skill principles to connect data patterns to writing strategy:

- High-performing hooks → which hook archetypes work best?
- Promo performance → does "lead with stance, bury the ask" hold up?
- Engagement-rate winners → what writing patterns do they share?
- Post type mix → are the right types getting the right share of output?

This closes the loop between analytics and content creation.

## Top/bottom split analysis (interpreting the recurring report)

The **procedure** for the recurring split report — window, the 50% top/bottom split (quartiles on request), engagement-rate definition, table columns, and presentation — lives in one place: the "Top/Bottom Split workflow" section of `SKILL.md`. Don't restate it here or in the scheduled task; follow it there. This section only covers how to *read* the contrast once you have the two tables.

What to look at when contrasting the top vs bottom halves:
- **Hook type** — POV/belief and status/FOMO openers vs abstract analogies or feature listicles.
- **Audience** — does the post speak to the decision-maker (status/strategic) or the practitioner (how-to/governance)?
- **Comments** — the biggest lever; bottom-half posts are usually comment deserts (0–1 each). Posts that end with a real question pull more.
- **Format** — quantified case studies and belief posts tend to top; feature roundups and off-thesis posts tend to sink.

### Reach and engagement rate are usually decoupled

Across runs, top-by-reach posts and bottom-by-reach posts have landed at nearly the same average engagement rate, and the single widest-reach post is frequently the *lowest* rate (broad/curiosity bait travels but doesn't resonate). So treat reach and rate as two separate axes, and when bucketing by rate, always sanity-check whether the widest posts are dragging the bottom.

### Recency distorts the bottom

Impressions build over days. A post from the last 2–3 days will look like a bottom-half loser purely because its reach hasn't matured. Exclude or flag the most recent few days before drawing conclusions.
