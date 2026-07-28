# Analysis Playbook

How to turn scraped LinkedIn data into actionable insights. Read this after scraping — the scraping skill handles getting the data, this handles making sense of it.

## The two numbers that matter

For every post, the headline pair is **impressions** (from the impressions view) and **totalEngagements** (from the engagements view — LinkedIn's all-up metric, includes reactions/comments/reposts/clicks/saves). The ratio `totalEngagements / impressions` is the engagement rate. Use that as the primary performance signal.

Reactions and comments are useful as a breakdown but are not the full picture — they leave out clicks and saves, which often dominate. Reposts specifically are not reliable from either dashboard view; if a particular post's repost count matters, visit the post page directly.

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

### Base reach is ~5K, breakout needs a trigger

Mid-tier posts cluster around 4,000–8,000 impressions. Breaking out above 20K+ requires a viral trigger: a shareable format, an emotional hook, or specific numbers in the opening line. The gap between top performers and the rest is large — there's no "doing slightly better," there's base reach and breakout.

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

## Cross-Referencing with linkedin-voice

When analyzing post performance, reference Shaw's `linkedin-voice` skill principles to connect data patterns to writing strategy:

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
