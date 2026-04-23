# Analysis Playbook

How to turn scraped LinkedIn data into actionable insights. Read this after scraping — the scraping skill handles getting the data, this handles making sense of it.

## Common Analysis Patterns

### Single Month Review

"How did March go?"

Scrape one month with both impressions and engagements views. Report:
- Total impressions and engagements
- Average impressions per post
- Engagement rate (total engagements / total impressions)
- Repost ratio (reposts / total engagements) — reposts are Shaw's primary reach amplifier
- Top 5 and bottom 5 performers
- Engagement breakdown: what % is reactions vs comments vs reposts

### Period Comparison

"Compare Q4 vs Q1"

Scrape each period separately. For each, compute the same aggregate metrics, then calculate deltas:
- Median impressions per post (median is more stable than mean when outlier posts skew things)
- Shift in engagement composition (e.g., "reposts went from 40% to 65% of all engagement")
- Changes in what content types perform best
- New patterns in top performers (e.g., "specific number hooks now dominate the top 5")

### Post Type Analysis

"Are promos underperforming?"

Use `scrape-with-types.js` to categorize and aggregate. Compare:
- Average impressions per type
- Which types over/under-index relative to their share of posts
- Type mix shifts between periods (e.g., "you posted 3x more promos in March but they got 2x fewer impressions each")

### Engagement Breakdown

"What's driving reach?"

Scrape the engagements view. Focus on:
- Repost ratio — reposts are the algorithmic amplifier. A high repost ratio means the content is getting shared, which feeds the LinkedIn algorithm and drives impressions
- Comment depth — are comments substantive or shallow? (Can't tell from numbers alone, but high comment counts relative to reactions suggest conversation-starting content)
- Reaction-to-impression ratio — a rough proxy for how often people who see the post actually engage

## Known Performance Patterns

Patterns that have been validated by real data across multiple analysis runs. Use these as baselines when interpreting new results — they're the "what we already know" that makes new findings meaningful.

### Curated listicles are Shaw's highest-ceiling format

Posts that curate resources with a specific number hook ("10 YouTube channels that...") consistently produce the most reposts and the highest total engagement. One curated listicle generated 1,400 reposts in a single year — more than most posts get in total engagement. These posts are save-worthy, repost-worthy, and have long shelf lives because people keep discovering and sharing them months later. When analyzing top performers, expect curated listicles to dominate.

### Reposts drive ~44% of all engagement

Reposts are the algorithmic amplifier and Shaw's primary reach mechanism. Posts optimized for reposts (curated lists, free resources, technical tutorials) compound reach in a way that reaction-heavy posts don't. When a post gets more reposts than reactions, that's the strongest signal of utility — people shared it more than they liked it.

### Personal milestones drive impressions differently

Milestone posts (moving, birthday recaps, career announcements) get massive reach through reactions and comments — people engage emotionally. But they generate fewer reposts. These are relationship-builders, not reach-extenders. They're still valuable (they can be top-3 by impressions) but they serve a different strategic purpose.

### Base reach is ~5K, breakout needs a trigger

Mid-tier posts cluster around 4,000–8,000 impressions. Breaking out above 20K+ requires a viral trigger: a repost-worthy format, an emotional hook, or specific numbers in the opening line. The gap between top performers and the rest is large — there's no "doing slightly better," there's base reach and breakout.

## Presenting Findings

Lead with the key insight, not the raw data. Shaw wants to know what to do differently — not just what the numbers are.

### Structure

1. **Headline finding** — the single most important thing (e.g., "Reposts drove 65% of all engagement in March — opinion posts are your reach engine")
2. **Supporting data** — 2-3 specific numbers that back up the headline
3. **Top/bottom performers** — with post previews so Shaw can recognize them and pattern-match
4. **Recommendations** — concrete changes to content strategy, if the data suggests any

### What Good Recommendations Look Like

- "Your opinion/thesis posts get 3x more impressions than promos. Consider framing more promos as opinion posts with a CTA buried at the end."
- "Posts with specific dollar amounts or numbers in the hook ($254, $160/mo, 29 days) consistently outperform abstract hooks."
- "Reposts are 60% of engagement. Your educational lists and framework posts get the most reposts — lean into those for reach."

Avoid vague advice like "post more engaging content" or "try different approaches." Ground everything in the actual data.

## Cross-Referencing with linkedin-post-writer

When analyzing post performance, reference Shaw's `linkedin-post-writer` skill principles to connect data patterns to writing strategy:

- High-performing hooks → which hook archetypes work best?
- Promo performance → does "lead with stance, bury the ask" hold up?
- Repost dominance → is "write for the repost" principle reflected in the data?
- Post type mix → are the right types getting the right share of output?

This closes the loop between analytics and content creation.
