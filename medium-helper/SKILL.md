---
name: medium-helper
description: "Move a finished blog draft from Shaw's Notion (the LFC database, titled \"(Blog) …\") into a Medium draft for The Data Entrepreneurs, and make the graphics and data lookups the post needs. Use whenever Shaw mentions Medium, a blog post, The Data Entrepreneurs, or a \"(Blog)\" page: \"copy this over to Medium\", \"paste the blog into Medium\", \"what cover image should I use\", \"make a graphic for the blog\", \"turn these screenshots into one image\", \"chart my cohort revenue\", \"how many followers did I have when X happened\", \"what tags should I use\", \"write the SEO title and description\". Also fires when a Notion LFC page is being turned into prose anywhere, or when a figure is being built for a Medium post (DM collage, follower-count card, revenue chart). Not for LinkedIn posts (linkedin-voice / sfc-helper), newsletters (newsletter-writer), or writing the blog from scratch — this skill moves and illustrates a draft Shaw already wrote."
---

# Medium Helper

Shaw writes blog drafts in Notion (LFC database, page title `(Blog) <Title>`) and publishes them to
Medium under his publication **The Data Entrepreneurs** (`medium.com/the-data-entrepreneurs`). This
skill covers the trip from Notion draft to a saved Medium draft, the house format that trip has to
land in, the graphics a post usually needs, and where the numbers behind those graphics come from.
It stops at a saved draft: Shaw adds the cover, tags, SEO fields, and submits to the publication
himself, but he asks for a recommendation on each, and those recommendations come from his own
published posts rather than from general Medium advice (§2).

Four jobs, each its own section below. Most requests hit one; a full "copy this over" hits the first
two and usually seeds the third.

## 1. Notion → Medium draft

Fetch the Notion page (`notion-fetch`; read `notion-helper` first per its own rule). Then in Chrome
(Shaw's real browser, signed in — read `chrome-browser` before the first browser step):

1. Open `https://medium.com/new-story`. Click the Title field and `type` the title. Medium assigns
   a draft URL (`medium.com/p/<id>/edit`) on first keystroke and autosaves from then on — report
   that URL at the end so Shaw can pick it up.
2. Click into the body ("Tell your story…") and paste the whole article as HTML with a synthetic
   clipboard event via `javascript_tool`. Medium's editor handles the paste and converts tags to
   its own blocks; typing it char-by-char is far slower and loses formatting. See
   `references/medium-paste.md` for the snippet and the exact tag → block mapping. The result
   should be `dispatched: false, defaultPrevented: true` — that means the editor consumed it.
3. Verify with one `javascript_tool` call that lists the first ~15 blocks (tag + text), then one
   screenshot of the top. Confirm the title is an `h3.graf--title`, the subtitle an `h4`, section
   headings `h3`, sub-headings `h4`. Scroll to the bottom to confirm the last paragraph landed.

Mapping the Notion markdown (details and the heading rules in `references/medium-paste.md`):

- `# Title` → typed into the Title field, not pasted
- first bold line after the title (`**What I learned.**`) → `<h4>` → Medium subtitle
- `##` → `<h1>` → big section heading · `###` → `<h2>` → small sub-heading
- `**bold**` / `*italic*` → `<strong>` / `<em>` · `…` divider lines → `<hr>` or drop
- `\{image\}` / `\{sales over time\}` style notes are **placeholders, not images** — the Notion
  draft has no pictures. Emit each as its own italic paragraph `[IMAGE: sales over time]`, keep
  the wording, and list them all back to Shaw at the end so he knows what to fill. Anything that
  reads like an embed (`\{data side hustles\}`) becomes `[EMBED: …]`.

Copy edits: fix objective errors (typos, dropped words, "lesson" → "lessons", punctuation) and
leave wording alone. Report every substantive change — a dropped word you restored, a figure whose
braces you removed — in the wrap-up so Shaw can veto it. Braces around a number
(`\{\$87,460.3\}`) mean "tentative"; strip the braces, round sensibly, and flag it.

Wrap-up to Shaw: the draft URL, the placeholder list, the edits made, and the things he still does
by hand (cover image, tags, SEO title and description, submit to the publication), each with the
recommendation from §2 attached so he isn't coming back to ask.

## 2. House format

Read `references/tde-format.md` before pasting or before advising on structure/cover. Short version:
title + one-line subtitle, 2–3 sentence intro that says what the article covers, cover image right
after the intro (Unsplash photo, "Photo by X on Unsplash" caption), big headings for sections and
small ones for numbered items ("Path 1: …", "Mistake 2: …"), every author image captioned
"… Image by author.", embedded links to his own earlier Medium posts where they fit, and a
sign-off that invites questions in the comments with a `:)`.

Cover-image asks get **search terms, not pictures**: Shaw searches Unsplash himself. Look at the
publication page in Chrome for the pattern (one literal, slightly wry visual metaphor per title —
a $100 bill, a lone figure on a cliff, a hand-drawn "AI?") and offer 3–4 groups of 3–5 search
strings with a recommended pick and the reason.

**Tags and SEO fields** get the same treatment: match the post to its closest published siblings
rather than reasoning from tag size. The generic answer (Business, Startup, Creator Economy) was
overruled with "look at previous posts": his five tags are a house set that keeps the founder
posts findable together, and the SEO description is a hand-written two-sentence form, not Medium's
auto-truncated first paragraph. `references/tde-format.md` § "Tags and SEO" has the observed
pattern, the tables, and the one-call JS that pulls tags and SEO fields for a dozen posts from a
medium.com tab. Present the pick, the alternates, and the sibling rows you matched against so he can
see the pattern himself.

## 3. Graphics for the post

Three kinds, all rendered to PNG at 2× so Medium's column scaling keeps them crisp. Wider than tall
— Shaw's phrase is "YouTube-thumbnail size, maybe a little wider", which in practice is ~2:1 to
3:1 (2000×640 to 2000×1040 CSS px, doubled on export).

Finished figures live with the post at `~/Documents/_stv/_content/_LFC/medium/<post-slug>/`
as flat PNGs named for what they show (`validation-dms.png`, `bad-approach.png`), with any HTML
source and fonts in a `<figure>-src/` subfolder beside them. Re-render from the filed source so the
folder is self-contained; a Downloads scratch folder is for exploring and goes once he's picked.

**Concept diagrams** (a before/after pair, a process, a tree) are `graphic-builder` work in its
embedded-graphic mode; this skill supplies the Medium constraints. White background rather than the
builder's cream, Medium green `#1a8917` for the good or forward side and a muted red `#B4473A` for
the bad or backward side, 1080px wide, no title or caption chrome because the Medium caption
carries the words. Real labels from his research (the Notion pain-points and ICP pages, call notes)
beat abstract placeholders: the figure is an argument about his actual business, and he will
supply the specifics if asked. When the brief is a direction rather than a spec, run the builder's
ideating workflow (subagents per design philosophy, contact sheets, narrow, variants) and give him a
local `index.html` master page in the scratch folder that shows every pair bad-left, good-right
with a toggle for Medium's 680px column; he browses an index, not a folder of PNGs. A pair must
render on one canvas size so the two images sit identically in the column; when the busier half
won't fit, cut its content (he dropped a branch) rather than growing the canvas or shrinking the
half he already likes.

**Screenshot-style collages** (DM cards, profile/follower cards): write a self-contained HTML page
and render it with `scripts/render_png.py`. Dark neutral background (`#1b1f23`) with platform-styled
cards; `assets/avatar.png` is Shaw's real profile photo (circular, transparent) — use it wherever a
card shows him, a blank circle reads as "obscured". Rules that came from Shaw directly:

- Other people's names are redacted (a gray block, not `[Name]`); **Shaw's own name, pronouns,
  timestamps and photo stay** — the point is that it's visibly him.
- Platform names as small text labels, never logos or wordmarks.
- A LinkedIn-card headline, location, or connection count that isn't from a real screenshot is a
  guess — say so in the wrap-up.

`references/graphics.md` has the two card layouts that have shipped (DM grid, follower cards) with
their CSS, so a repeat is a data swap rather than a redesign.

**Charts** (revenue by cohort, follower growth): matplotlib, white background, Medium green
`#1a8917` for the series, bold title + gray subtitle placed with `fig.text` (not `ax.set_title`, which
collides with a subtitle), `$Nk` y-ticks on round intervals, and value + series labels on every
point. The rules Shaw has asked for by name:

- Average as a dashed dark line at 80% opacity, labeled `Avg $N` just past the right edge.
- Labels go above a point by default; move a label below when it would sit on the average line or
  on a neighboring steep segment (he will tell you which ones are hard to read — pre-empt it).
- Start the x-axis a few weeks before the first tick so the first tick label clears the y-axis.

`scripts/cohort_chart.py` is the revenue-over-time chart as a function of a list of
`(label, value, iso_date)` — reuse it rather than re-deriving the styling.

Render, `Read` the PNG, fix what's wrong (overlapping labels, wrapped lines, empty card space),
then `SendUserFile` with `display: render`. Don't send intermediate renders.

## 4. Where the numbers come from

Read `references/data-sources.md` when a post needs a historical figure. The short map:

| Need | Source | Note |
|---|---|---|
| Cohort revenue, dates, lifetime total | Maven admin earnings page, scraped with one JS regex | Sums should equal the "lifetime earnings" tile — check |
| YouTube subs on a past date | YouTube Studio custom range: current subs − net change since that date | Exact; Wayback only brackets it |
| Medium / YouTube follower count on a past date | Wayback Machine snapshot nearest the date | Say which snapshot date you used |
| LinkedIn followers on a past date | **No archive** (auth wall) — bracket from milestone posts in SFC | Always an estimate; label it |
| Milestone dates ("10k subs", "40k subs") | SFC database in Notion, query `Name LIKE '%subs%'` etc. | Pages are often blank — the title and date are the data |

Historical counts land in the wrap-up as a small table with the source and whether each is exact or
estimated. A number Shaw can't trace is a number he can't publish.

## Style of the wrap-up

Bottom line first (the draft link, the file), then the handful of things only he can decide. He
reads the file, not a description of it. Edits you made to his words are the one thing to spell out.
