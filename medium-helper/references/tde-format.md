# The Data Entrepreneurs — house format

Publication: `https://medium.com/the-data-entrepreneurs` ("Data Science + Entrepreneurship",
~1.1K followers, Shaw is an editor). His own profile is `shawhin.medium.com`. Posts are usually
member-only ("Member-only story") and 5–7 minute reads.

Read a recent post in Chrome (`get_page_text` on the article URL) if anything here seems stale — the
pattern is consistent across the last two years, but Shaw will have the final say on his own style.

## Skeleton

```
Title                      – "Why I Blew Up My $87,667 AI Cohort" — a number or a verb with teeth
Subtitle                   – one line, lowercase-ish, often a parenthetical: "What I learned."
Intro paragraph            – 2–3 sentences: the situation, then "In this article, I'll break down…"
Cover photo                – Unsplash; caption "Photo by <name> on Unsplash"
(optional) hook paragraph  – the "Last year I was living the dream…" opener
## Section heading         – big heading
### Numbered sub-heading   – "Path 1: Freelancing", "Mistake 2: No Clear Customer", "Lesson 3: Focus"
   2–4 short paragraphs each, 1–3 sentences per paragraph
   figures with caption "<what it is>. Image by author."
   embedded link cards to his own earlier Medium posts where a topic was covered before
## Conclusions / What Now? / What's Next?
Sign-off                   – one paragraph of hope/encouragement, then
                             "If you have any questions … let me know in the comments :)"
```

## Voice markers (don't rewrite to add these; recognize them so you don't edit them out)

- Parenthetical asides every few sentences: "(largely)", "(painful)", "(pun unintended)", "😅".
- First-person, past tense for the story; present tense for the lesson.
- Numbers are exact, not rounded, in the title and body ($87,667, $10,798) — a rounded figure in
  his draft wrapped in braces is a placeholder waiting for the real one.
- "IMO", "i.e.", "e.g." inline; "Here's why." as its own sentence.
- Ends sections with a one-line takeaway rather than a summary paragraph.

## Covers

One literal visual metaphor for the title, uncluttered, one subject, usually a photo:

| Post | Cover |
|---|---|
| How to Monetize Your AI Skills | a $100 bill on white |
| 7 Skills I Had to Learn to Make $100k/yr | lone figure at sunset |
| From 0 to 70k | man arms-out on a cliff edge |
| 30 AI Buzzwords Explained | hand-drawn "AI?" |
| Breaking Down My First $10k Month | the revenue bar chart itself |

So for a cover ask: 3–4 groups of Unsplash search strings (literal title metaphor, the post's core
metaphor, "starting over", the money angle), a recommended pick, one sentence why. He downloads it.

## Figures that recur

- A collage of real LinkedIn DMs or messages, names redacted (validation stories).
- Follower/subscriber counts at a point in time (audience-size stories).
- Revenue over time per cohort / per month (income stories).
- Funnel or process diagrams, hand-drawn-ish, captioned "Image by author".
- A before/after concept pair (bad approach vs. good approach), same canvas, red vs. green,
  captioned "Bad approach: solution → problem → customer. Image by author." and the mirror.
- "Income vs effort" style scatter with a raw-data table underneath.

Section 3 of the skill and `graphics.md` cover how the first three are built; the concept pair is
graphic-builder work with the constraints in section 3.

## Tags and SEO

Both are chosen to match the post's closest published siblings, not from general Medium advice.
Pull the live pattern before recommending: from any medium.com tab, this one `javascript_tool`
call reads tags, SEO title, and SEO description for a list of post URLs (same-origin fetch, so it
sees them as Shaw does):

```js
const urls = [/* post URLs from the publication page: a[href] matching /the-data-entrepreneurs/<slug>-<hex> */];
const out = [];
for (const u of urls) {
  const html = await (await fetch(u, {credentials: 'include'})).text();
  const g = re => (html.match(re) || [])[1];
  out.push({
    slug: u.split('/').pop().slice(0, 40),
    tags: [...new Set([...html.matchAll(/href="(?:https:\/\/medium\.com)?\/tag\/([a-z0-9-]+)/g)].map(m => m[1]))],
    seoTitle: g(/"seoTitle":"([^"]*)"/),
    seoDesc: g(/"seoDescription":"([^"]*)"/),
    claps: g(/"clapCount":(\d+)/),
    date: (g(/"datePublished":"([^"]+)"/) || '').slice(0, 10),
  });
}
out
```

Clap counts are lifetime totals, not reach; use them to spot outliers, not to rank tags.

**Tags** (5 per post). Observed across 12 founder-story posts, Oct 2026:

| Tag | Posts of 12 | Role |
|---|---|---|
| entrepreneurship | 11 | on every founder post, non-negotiable |
| data-science | 8 | the audience tag; used even when the post isn't about data science |
| ai | 5 | every 2025 post |
| solopreneur | 3 | the "my journey" posts |
| entrepreneur, side-hustle | 2 each | the two highest-clap 2025 posts |
| founder-stories, founders, startup, business | 1 each | |

So a founder post-mortem gets entrepreneurship + ai + solopreneur + data-science + one genre tag
(founder-stories was the pick for the ABB post, with startup or business as the reach-first swap).
Niche tags only outperform when the niche is the hook (the Taleb post rode nassim-taleb and
risk-taking to 2.7k claps).

**SEO title** is the headline unchanged. Medium appends "| by Shaw Talebi" itself.

**SEO description** is hand-written on the 2025 posts (the older ones left it on auto, which just
truncates the first paragraph): two sentences, ~150 characters, one line of stakes then
"Here, I share …" with the payoff.

| Post | SEO description |
|---|---|
| What I Learned Launching an AI SaaS (in 30 days) | I launched my 2nd AI SaaS as a solo founder. Here I share key lessons learned on coding, GTM, and shipping faster, and what I'd do differently next time. |
| 7 Skills I Had to Learn to Make $100k/yr | Technical skills aren't enough to build a sustainable business. Here, I share the 7 skills I needed to learn to make $10k/mo working for myself. |
| How to Monetize Your AI Skills | A side hustle mitigates the risks of having a single source of income. Here, I share 5 AI side hustles that technical professionals can start today. |
| Why I Blew Up My $87,667 AI Cohort | After 8 cohorts and $87,667 in sales, I shut down the AI course paying my bills. Here, I share the 3 mistakes that led me there and what I'm doing instead. |

Offer one recommended description and two alternates (lesson-first, question-style), plus the
sibling rows matched against.
