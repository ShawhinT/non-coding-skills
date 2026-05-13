# Thumbnails

The complete thumbnail strategy, visual identity, composition, and workflow.

## What thumbnails do

Thumbnails are the second half of the click. The title is the verbal hook; the thumbnail is the visual one. They have to work together, but the thumbnail shouldn't repeat the title — it should complement it by raising curiosity the title resolves (or vice versa).

Shaw's channel is shifting from "Technical Implementation" to "Strategic Authority" for a Founder/CEO audience. Thumbnails must shift with it — stop looking like tutorials, start looking like intelligence briefings.

## The strategic shift

Founders and CEOs value leverage, ROI, and market positioning. The thumbnail's visual language has to match.

| Element | Old (Technical/Builder) | New (Executive/Founder) |
|---|---|---|
| Primary hook | Functional ("How to build X") | Strategic ("Why X changes your business") |
| Visuals | Code snippets, VS Code, software UIs | Studio portraits, boardrooms, institutional logos |
| Emotional pull | Capability & learning | Authority, FOMO, & competitive edge |

## The 3-filter framework (applied to thumbnails)

Every thumbnail that ships passes all three filters in order:

1. **Would the avatar pause their scroll for this image?** Would they recognize the subject as relevant to their world?
2. **Does it capture attention with at least 2 click-driver principles stacked?**
3. **Is it specific enough to be ownable?** A generic robot brain dies. A specific Fortune 500 logo with a red downward arrow lives.

This is the visual application of the 3-filter framework. For sentence-level work on the thumbnail's hook text, the visualize / falsify / unsignable filter from `conversion-copy` still applies — same canonical home.

## Visual identity

### Color palette
Base in charcoal grey, navy, and deep slate. Accents in off-white and champagne gold for a premium "executive" feel. Use ONE saturated signal color (neon green or international orange) only for the primary hook or outlier data point — saturation everywhere = saturation nowhere.

### Lighting & aesthetic
High-contrast studio lighting with deep shadows (chiaroscuro). Prefer clean, minimalist office backgrounds or professional studio sets over abstract digital "circuit board" patterns. The aesthetic target is *Bloomberg / a16z*, not *AI hype YouTube*.

## Composition principles

### The 40% rule
The primary subject (Shaw's face or the main strategic symbol) must occupy at least 40% of the frame height. ~80% of YouTube views happen on mobile — if it's not readable at thumb-size, it doesn't exist.

### Visual hierarchy (1-2-3)
Build every thumbnail in three layers:
1. **The hook** — ONE high-contrast focal point (a "Hired" stamp, a competitor logo, a shocking data outlier).
2. **The text** — 3 words maximum. Clean, heavy sans-serif.
3. **The context** — subtle geometric grids or a professional environment in the background.

### The squint test
Squint at the design. If the core message is lost, it's too cluttered. Remove elements until only the click remains.

## Typography

- **3 words maximum.** No exceptions.
- **Never repeat the title.** The thumbnail text should *complement* the title by asking a question the title answers, or stating a claim the title qualifies.
  - Title: *"Claude Cowork Explained"* → Thumbnail: *"NO MORE INTERNS?"*
  - Title: *"Why 95% of AI Deployments Fail"* → Thumbnail: *"WHO'S LEFT?"*
- **Fonts.** Editorial, heavy sans-serif (Montserrat Black, Bebas Neue). Avoid digital/glitch or futuristic tech fonts — they signal "builder content," which actively repels the new avatar.

## Psychological hooks for thumbnails

The 19 click-drivers in `references/titles.md` apply visually too. The most relevant translations:

- **Curiosity gap** — Show a paradox the viewer needs to click to resolve. A "growth" chart that's actually a cost-reduction chart. A green arrow pointing *down*.
- **Counterintuitive subversion** — Visual contradiction. Tom Brady throwing a wobble. A CEO looking confused at a boardroom screen.
- **Specific real numbers** — One large, defensible number on the thumbnail (`$50M`, `95%`, `$2T`).
- **Stakes** — Visual symbols of consequence: red downward arrows, buildings in shadow, the word "ERASED" or "GONE."
- **Authority subversion** — Use institutional credibility: Fortune 500 logos, S&P 500 / Nasdaq tickers, clean white borders or "Intelligence Briefing" mastheads. Then break expectations with the headline.
- **Direct address** — Shaw looking directly into the camera, eye contact at portrait scale.

The institutional-credibility move (logos + index tickers + briefing-style mastheads) is the highest-leverage shift for the new avatar. It signals "high-value research" before the viewer even reads a word.

## Technical delivery

- **Resolution.** 1280x720 minimum. 1920x1080 preferred.
- **Export format.** `.png` to avoid compression artifacts on text edges. `.jpg` softens the typography enough to look amateur.
- **Contrast ratio.** Aim for 4.5:1 minimum between text and background.
- **Safe zone.** Keep all text, faces, and critical icons away from the bottom-right corner — that's where the YouTube duration timestamp lives and will obscure anything underneath.

## Thumbnail workflow

### Step 1 — Capture intent
Confirm:
- **What's the video about** in one sentence
- **The title** (if known) — thumbnail text complements it. If the title isn't decided, propose paired title + thumbnail concepts together.
- **Strongest visual asset available** — a specific company logo, chart, face, stamp/seal, screenshot of a real artifact?
- **Constraints** (face required vs. no face, on-screen number must be defensible, etc.)

If anything is unclear, ask one question.

### Step 2 — Generate 3-5 concepts
Each concept:
- Stacks 2-3 click-driver principles
- Has a different visual archetype from the others (one logo-led, one Shaw-portrait, one data-outlier, etc.)
- Passes the 3-filter framework
- Passes the squint test (one focal point, ≤3 words, readable thumb-sized)

### Step 3 — Annotate each
- **Subject** — primary image (Shaw's face / logo / chart / stamp)
- **Hook text** — the ≤3-word phrase
- **Principle stack** — which click-drivers are doing the work
- **Description** — one sentence on the visual: layout, signal color, paradox or contrast, what the eye lands on first

### Step 4 — Rank and recommend
Pick the top 1-2 to ship first. Strongest concepts usually combine institutional credibility (logos, tickers, masthead framing) with one specific defensible number or one shocking visual paradox.

## Output format

### Thumbnails only

```
**Topic:** <one-sentence restatement>
**Title (assumed):** <the title the thumbnail is paired with>
**Avatar:** <who's the target click>

**Thumbnail concepts:**

1. <Hook text> (≤3 words)
   - Subject: <primary image>
   - Principles: <stack>
   - Description: <1-sentence visual brief>

2. ...

**Top picks to ship first:** <1-2 concepts + brief reason>
```

### Paired (titles + thumbnails together)

```
**Topic:** <one-sentence restatement>
**Avatar:** <who's the target click>
**Outcome:** <what the viewer walks away with>

**Paired packages:**

1. **Title:** <Title>
   - Title principles: ...
   - Thumbnail hook text: <≤3 words>
   - Thumbnail subject: <primary image>
   - Thumbnail principles: ...
   - How they work together: <1 line on the title→thumbnail handoff>

2. ...

**Top pick to ship first:** <1 package + reason>
```

## Guardrails

- **Real numbers, not invented ones.** A fabricated number kills credibility on a thumbnail just as fast as in a title.
- **Avatar appropriateness.** Lean closer to Veritasium / a16z / Bloomberg aesthetic — serious, high-credibility, but still using every click-driver principle.
- **The thumbnail is not a title.** If the thumbnail text is longer than 3 words or repeats the title, it's broken. Cut.
- **One focal point.** If the squint test fails, the thumbnail is doing too much.
- **Mobile first.** ~80% of views are mobile. If it's not readable at thumb-size, it doesn't matter how good it looks at full size.
- **No jargon-as-authority.** Technical thumbnails featuring code editors or VS Code are search-bait for *builders*, not the EV-conscious CEO avatar.
- **Don't over-stack.** 2-3 principles per thumbnail is the sweet spot.

## Production note for end-screen pairing

When the video ends with a next-video CTA (see `references/script-body.md`), the thumbnail of that next video should be ready and visible at the moment the verbal CTA hits. Visual + verbal land at the same moment, or the click is lost.
