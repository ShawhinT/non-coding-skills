---
name: infographic-builder
description: Build single-image infographics for LinkedIn (and other social feeds) — two-panel comparisons, vertical lists, single-centerpiece concept stills. Each one is authored as an HTML file and rendered to a 2x retina PNG via a headless-Chrome pipeline included with this skill. Use whenever the user asks to make, design, build, or render an infographic, LinkedIn post graphic, social-feed still, concept image, or "graphic for [post idea]". Triggers include "make an infographic for X", "design a LinkedIn graphic", "build a post graphic", "turn this Notion brief into a visual", or any reference to producing a still PNG from a designed composition. Defaults to a brand-agnostic light palette with Manrope / Libre Franklin / JetBrains Mono type. If the graphic is for a specific brand, reference the relevant brand-system skill (e.g. `aba-brand-system`) for colors/type/voice — pull tokens only, do NOT import the brand's website composition.
---

# Infographic Builder

Author single-image LinkedIn infographics in HTML/CSS/SVG, render them at 2x retina to PNG with a headless-Chrome script. Each infographic lives in its own project folder under `~/Documents/_stv/_content/_SFC/linkedin/<year>/<category>/<slug>/`.

This skill is the still-image sibling to `animation-builder` (MP4 B-roll for YouTube). Same stack, different deliverable, different priorities — an infographic has ~2 seconds in a scroll to land one idea.

## What this skill is for

- Single PNG, sized for LinkedIn (landscape, portrait, or square).
- One visual idea per graphic. If you can't name it in five words, the graphic isn't ready to render.
- Not a website mockup, not a slide deck, not a B-roll clip.

**Recognized exception — composite cheatsheets.** A tall portrait (~1080×~2000) that bundles 3–6 standalone topics into one educational summary (e.g. `claude-skill-cheatsheet`). Each section is a labeled card group with its own self-contained visual idea — the *composite* doesn't violate "one idea per graphic," it stacks several. Use when the brief explicitly asks for a "cheatsheet," "guide," or "everything-you-need" piece that summarizes content already proven as individual graphics. Reuse the markup from those individual graphics (don't re-author from scratch).

## Workflow

1. **Read the brief.** Usually a Notion post idea. Confirm with the user: aspect ratio, brand context (`aba-brand-system` or brand-agnostic?), and what *single* idea the graphic must land.
2. **Write the scene sentence.** Before opening the template: who's scrolling LinkedIn, what they should understand in 2 seconds, what feeling it should leave. "A graphic comparing X and Y" is not a scene. "A founder scrolling at lunch realizes that 'connectors' and 'skills' aren't synonyms — one gives Claude access, the other gives it competence — and remembers it because the right side has a directory tree she's seen on her own machine" is.
3. **Pick aspect ratio.** Default landscape (1080×820). Portrait (1080×1350) for vertical lists or stacks. Square (1080×1080) for single centerpieces with symmetric margin. Don't reflexively pick square — landscape and portrait read fine in-feed.
4. **Create the project folder first.** See "Project folder convention" below. Author the HTML *inside* it from the first edit.
5. **Pull brand tokens only** if a brand-system skill is in play. Colors, type, logo treatment, and the brand's *infographic-composition* reference (e.g. `aba-brand-system/references/infographic-composition.md`) — never the brand's web-composition or hero pattern.
6. **Author the HTML** from the matching template in `templates/`, **render via `scripts/render.sh`**, eyeball the PNG, ship.

## Project folder convention

**Every infographic gets its own folder. Create it first, before writing any HTML.** No loose HTMLs or PNGs in shared directories.

- **Folder name:** kebab-case slug matching the topic — `connectors-vs-skills/`, not `infographic-2026-05/`.
- **Folder location:** under your content directory, organized as `<year>/<category>/<slug>/`. `<category>` is typically `AI-education`, `misc`, or a similar topical group. If the category isn't obvious from the brief, ask.
- **Folder contents (default — no external assets):**
  ```
  <slug>/
    <slug>.html
    <slug>.png        ← the rendered output
  ```
- **Folder contents (only when the HTML references external logo / image files):**
  ```
  <slug>/
    <slug>.html
    <slug>.png
    assets/           ← project-local copies of any logos used
      claude.png
      notion.svg
      …
  ```
- **Do not create `assets/` as boilerplate.** Inline-SVG-only graphics (Heroicons-style paths in the HTML itself) need no folder. Create `assets/` the moment a `<img src="assets/...">` lands in the HTML, not before.
- **Relative paths in the HTML** (`assets/notion.svg`) keep the folder portable when assets are present, so Shaw can zip and share it without dragging the skill along.
- Write the HTML *inside* the project folder from the first edit. Don't create it elsewhere and move it later.

## Treat it as an infographic, not a website

The single most important preference, and the easiest one to violate when a brand-system skill is loaded.

Brand systems are designed for **websites and apps**. Their layout DNA (full-bleed hero, gradient overlay, eyebrow + h1 + h2 + body + CTA, decorative dividers, hover states) does not transfer to a single still that has ~2 seconds to land one idea.

**Borrow only:**
- Color palette
- Type stack
- Logo treatment
- Occasional component primitives (button pill, badge)

**Strip on sight:**
- Gradient thumbnails / overlays
- Decorative dividers
- Multi-tier text hierarchies (eyebrow + h1 + h2 stacks)
- CTA buttons (an infographic isn't clickable)
- Background glows beyond one very faint one if any
- Hover/transition styles (the graphic is a still)

**Each card / panel = three elements max:** one heading word, one supporting line, one graphic. Same rule as section cards in `animation-builder`.

**Card-per-step is the canonical exception** to "no decorative card grids." When the visual idea is "N discrete steps you do in order," giving each step its own card (`rounded-2xl` or similar, low-opacity hairline border, light surface on the off-white bg) sharpens the beat structure and makes the step eyebrows + labels bottom-align cleanly. Still keep each card to graphic + step eyebrow + one-line label — the card adds structure, not extra elements. Live example: `four-step-framework`.

**When a brand-system skill is loaded, this rule gets *harder*, not softer.** ABA's canonical hero is eyebrow + 2-line H1 + 1-sentence subhead + CTA. Do not transfer that pattern to the infographic. A LinkedIn still gets a title and the body content; on a single-title composition, eyebrows and subtitles are dead weight that push the actual payload below the fold and make the graphic read as a website screenshot instead of a still. If you find yourself writing both a subtitle and a brand-system eyebrow on the top-level title, the subtitle is the one to delete, and probably the eyebrow too.

**Exception — eyebrows as parallel-card labels.** When two or more cards are being explicitly compared (`TYPE 1` / `TYPE 2`, `BEFORE` / `AFTER`, `FREE` / `PAID`), short mono eyebrows above the card heading work as discriminators — they carry structural meaning, not decoration. Used in `two-types-of-skills`. Still keep them tight: one or two words, mono, ~14px, uppercase.

**Exception — eyebrow as below-title metadata.** When the title carries the entire hook and you still want a small structural label (e.g. `4-STEP FRAMEWORK`), it can sit *below* the h1 in mono accent. Reads as a quiet caption rather than a website pre-roll. Used in `four-step-framework`. Keep it short and tight: one phrase, mono, ~16px, uppercase.

**Left-align body copy and headings** unless the composition is explicitly symmetric (single-centerpiece square graphics are the typical exception).

## Composition principles

- **One visual idea per graphic.** If a second idea wants in, it's a second graphic.
- **Pick the layout from the idea, not the format.** A vs B → landscape with two panels. Numbered list / progression → portrait. Single centerpiece → square.
- **Equal-width grid columns:** `grid-template-columns: 1fr 1fr` does NOT enforce equal width when a child overflows. Add `min-width: 0` to the children. This bit us on `connectors-vs-skills` and will bite again — codified here once.
- **Equal-bottom alignment for parallel cards.** When two cards have differently-sized graphics (left = numbered steps that fill the area, right = small tile grid), bottom-anchored rows like an `e.g.` footer drift to different y-positions and the cards look misaligned. Two working patterns:
  - **Fixed graphic height** (used in `connectors-vs-skills`): set `.graphic { height: 320px }` on both cards. Works when both graphics naturally fill that height.
  - **Flex graphic, anchored footer** (used in `two-types-of-skills`): `.card { min-height: 560px; display: flex; flex-direction: column }` + `.graphic { flex: 1 }`. The graphic absorbs slack; the row after it lands at the same y-position in both cards. Use this when one graphic is sparse and centering it would otherwise look top-heavy.
- **Optical vs. geometric symmetry, group composition, structural-behind-focal, namespace-classes-by-role** — these all apply identically here. See `~/.claude/skills/animation-builder/SKILL.md` § "Motion principles" and § "Composition and storytelling principles" for the canonical write-up; the same rules apply minus the motion-specific parts.
- **Footer:** `@shawhintalebi` in JetBrains Mono, ~14px, ~60% opacity, bottom-center. Quiet signature, not a brand stamp. Brand-system skills may override the handle (e.g. `aba-brand-system/references/infographic-composition.md` specifies `aibuilder.academy` for ABA-branded stills — same treatment, brand URL in place of personal handle).
- **Footer placement on variable-height canvases.** When the canvas is taller than its content (composite cheatsheets, in-progress drafts), the footer floats up just below the last section with dead space below — reads as broken. Anchor it to the lower third: `html, body { min-height: 100vh }`, `.canvas { min-height: 100vh; display: flex; flex-direction: column }`, `.footer { margin-top: auto }`, plus a small canvas `padding-bottom` (~28px). Footer sticks to the bottom regardless of content length, so mid-iteration renders stay readable and final renders look intentional. Pair with the iterative-height workflow under Rendering.
- **Fill the frame; don't pad a guess.** A list or catalog of full-width cards carrying one short line of body text under-fills both axes — whitespace pools to the right of each card and below the last one. Two fixes applied together: (1) scale the title, names, and icon tiles up until the body line carries most of the card width, and (2) size the canvas to the *measured* content height (see Rendering § "Iterative height tuning for tall composites") instead of a guessed `min-height`. With the height measured, a footer in normal flow (plain `margin-top` + bottom padding) removes bottom dead space directly; reserve the `margin-top: auto` footer trick above for drafts whose height is still in flux. On `non-coding-skills` this meant title 60→72px, names 32→42px, tiles 74→92px, and sizing to ~1555px of measured content rather than a fixed 1350 — which closed both the right-edge and bottom gaps.

## Type & color

- When a brand-system skill is loaded (`aba-brand-system`), use its tokens. Pull, don't fork.
- **Default brand-agnostic palette:**
  - `--bg: #FAFAF7` for light mode (the templates' default)
  - `oklch(0.16 0.01 250)` for dark mode
  - One accent doing the heavy lifting — whichever accent the loaded brand-system skill defines (e.g. ABA's Cerulean `#087CA7`), or, with no brand, a single muted accent chosen from the brief. Never two competing accents.
- **Default type stack:**
  - Display: **Manrope** 700/800, tracking `-0.02em` at large sizes
  - Body: **Libre Franklin** 400–600, line-height ~1.4
  - Labels / badges / footer / code: **JetBrains Mono** 400–600

## Icons — Heroicons first, never hand-drawn

**Default to Heroicons outline paths for every UI metaphor in the graphic.** Do not hand-draw SVG paths for user, document, chat-bubble, arrow-long-down / -up / -right / -left, arrows-right-left, plus, minus, arrow-path (refresh), computer-desktop, clock, sparkles, check, x-mark, etc. Heroicons covers ~90% of what an infographic needs, the paths are public, and a hand-drawn icon will always look slightly off next to a real one.

**Find one:** search `https://heroicons.com` (outline set, 24×24) by keyword and copy the path. The skill `aba-brand-system/references/icons.md` maintains a curated subset Shaw uses on the live ABA site — check there first; it already has `arrowRight`, `check`, `play`, `tools`, `bulb`, `rocket`, `clock`, `calendar`, `envelope`, `user`, `chart`, `chat-bubble`, `bolt`, `cog`, `light-bulb`, `academic-cap`, `sparkles`, `lock`.

**Inline the SVG** — don't fetch as a file. Heroicons paths are short. Pattern:

```html
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
    d="<heroicon path data>"
    style="color: var(--primary);"/>
</svg>
```

Use `stroke-width="1.5"` by default. **Bump to `2.75` for emphasis arrows** (connector arrows between icons, "step 1 → step 2" indicators) — at ~22–32px on-canvas, the default 1.5 reads as a render glitch.

**Only draw a custom path** when (1) no Heroicons / Lucide equivalent exists AND (2) the shape is essential to the idea — e.g., a specific diagram geometry, a labeled connector curve between two icons. Even then, the arrowhead should be a tiny triangle or `marker-end`, not a hand-tuned bézier with hard-coded coordinates.

**When this rule fires hardest:** any time you're about to write `<path d="M ..."` with multi-segment bezier coordinates for something that is "a person" / "a document" / "a chat bubble" / "an arrow." Stop and grab the Heroicon.

## Asset library — the bundled `assets/logos/`

The skill ships with a growing library of logos. **Before fetching anything from the web, `ls ~/.claude/skills/infographic-builder/assets/logos/` and read `assets/README.md`.** If the asset exists, copy it into the project's local `assets/` folder and reference it relatively.

### Workflow when an asset is missing

1. **Fetch it** (source priority below).
2. **Save to BOTH** `~/.claude/skills/infographic-builder/assets/logos/<name>.<ext>` (the library) AND the project's local `assets/` folder (the working copy).
3. **Append a one-line entry to `~/.claude/skills/infographic-builder/assets/README.md`** in the format `<name> — <source>, brand color (if any), <date>`. The README is the index; without an entry the file is invisible to future runs.

### Source priority

In order — try each before falling to the next.

**AI brand logos** (Claude, ChatGPT, Gemini, Cursor, Perplexity, Mistral, etc.) — lobehub CDN:

```bash
curl -sL -A "InfographicBuilder/1.0" \
  "https://unpkg.com/@lobehub/icons-static-png@latest/light/<name>-color.png" \
  -o "<name>.png"
```

Try `-color` first; fall back to the monochrome (`<name>.png` without `-color`) only if no color variant exists. **lobehub is AI-only — do not waste time asking it for Notion / Stripe / Slack / etc., it will return ASCII / 404.**

**Generic SaaS / app logos** (Notion, Stripe, Jira, Slack, GitHub, Linear, etc.) — simpleicons.org:

```bash
curl -sL "https://cdn.simpleicons.org/<slug>/<hex-no-hash>" -o "<name>.svg"
```

The hex after the slug is the official brand color (Stripe `635BFF`, Jira `0052CC`, Linear `5E6AD2`). simpleicons.org lists the canonical color on each icon's page.

**simpleicons is single-color only.** If the brand identity *is* the multicolor mark — Slack's four petals, Google Calendar's red/yellow/green/blue, Gmail's M — simpleicons gives you a one-tone version that loses the brand. Skip simpleicons and go straight to Wikimedia for these.

**Google products, Microsoft products, anything simpleicons lacks** — Wikimedia Commons. Pattern:

```bash
curl -sL -A "InfographicBuilder/1.0 (shawhintalebi@gmail.com)" \
  "https://upload.wikimedia.org/wikipedia/commons/thumb/<x>/<xy>/<File.svg>/500px-<File.svg>.png" \
  -o "<name>.png"
```

Two strict requirements:
- **Descriptive User-Agent with contact info.** Generic UAs and bare `Mozilla/5.0` get HTTP 400.
- **Restricted thumb widths only:** 20, 40, 60, 120, 250, 330, 500, 960, 1280, 1920, 3840. Arbitrary widths (600, 800) return HTTP 400 with a "use thumbnail steps" message. Use **500** or **960** for typical logo use.

**Last resort** — ask the user to paste the SVG.

### Verify the download

`file <path>` should report `PNG image data` or `SVG Scalable Vector Graphics`. If it says `HTML document` or `ASCII text`, you got an error page. Try a different source.

### Light vs. dark variants

For a light-bg infographic (`--bg: #FAFAF7`) the dark/color variant is correct. For a dark-bg infographic, fetch the white-stroke variant or recolor an SVG's `fill`. **Always open the file before inserting** — a "missing logo" is usually white-on-white or black-on-black.

### What goes in the library vs. what doesn't

- **In the library:** logos, brand marks, reusable iconography.
- **Project-only:** one-off graphics (hand-drawn diagrams, custom illustrations, screenshots specific to a single post). Don't pollute the library with single-use assets.

## Rendering — `scripts/render.sh`

The renderer is a thin Bash wrapper around headless Chrome. **Use it, not Playwright MCP.**

```bash
~/.claude/skills/infographic-builder/scripts/render.sh \
  /abs/path/to/<slug>.html [--size square|portrait|landscape|WxH] [--out <png-path>]
```

Defaults: `--size landscape` (1080×820), `--out <html-dir>/<basename>.png`.

Under the hood it invokes:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=<W>,<H> --force-device-scale-factor=2 \
  --screenshot=<output.png> "file://<absolute-html-path>"
```

`--force-device-scale-factor=2` gives 2x retina output (e.g. 1080×820 logical → 2160×1640 actual). LinkedIn's feed compression eats sharpness; ship at 2x always.

### Iterative height tuning for tall composites

Variable-height portraits (cheatsheets, long lists) need their canvas height matched to content. Don't guess in 100px steps — you'll burn 3–5 renders. Instead: render once with a generous height (`--size 1080x4000`), open the PNG, measure where content actually ends, then re-render at `content-end + ~40px`. One miss-render plus one final, instead of binary-searching.

Measure the content end programmatically instead of by eye. The renderer screenshots a fixed viewport, so the canvas height has to match the content exactly — eyeballing the last pixel still leaves you re-rendering. A quick PIL scan for the last non-background row makes the second render exact:

```python
from PIL import Image
im = Image.open(PATH).convert('RGB'); w, h = im.size; px = im.load()
bg = (250, 250, 247)   # match --bg exactly (#FAFAF7 here)
def has_content(y):
    return any(abs(px[x, y][i] - bg[i]) > 6 for x in range(0, w, 5) for i in range(3))
last = next(y for y in range(h - 1, -1, -1) if has_content(y))
print('content ends at', last / 2, 'logical px')   # /2 because render is 2x retina
```

Then re-render at `content-end + ~40px`. Two things to keep right: the PNG is 2x, so divide the pixel row by 2 to get logical px; and `bg` must match the canvas background (the off-white default or the brand bg) or every row reads as "content."

### Why not Playwright MCP

Both verified during the `connectors-vs-skills` build:
- Playwright MCP **blocks `file://` URLs** — `browser_navigate` returns a protocol error.
- `python3 -m http.server` as a workaround is **blocked by the sandbox classifier**.

Headless Chrome via Bash subprocess accepts `file://` directly. It's the working bypass.

## Validation

Open the rendered PNG before declaring done. Don't ship blind.

- For multi-element layouts (two cards, equal columns, parallel graphics), confirm column widths match and visual elements align — bugs only show up at full size.
- If something looks wrong, fix the HTML and re-render. Don't iterate on micro-tweaks the user didn't ask for.
- For spacing-sensitive work (gap equalization, optical balance), open the HTML in a regular Chrome tab and use the dev tools to read `getBoundingClientRect` on the elements you're balancing. CSS coordinates lie when text widths and padding affect the visible box.

## Absolute bans (match-and-refuse)

If you're about to write any of these, rewrite the element with different structure.

- **Gradient text** (`background-clip: text` with a gradient). Emphasize through weight, size, or solid color contrast.
- **Glowing AI orbs, sparkle particles, neon edges.** First-order training-data reflex. If the graphic is about AI, the visual idea must come from the specific point, not the topic's vocabulary.
- **Multiple competing *decorative* accent colors.** One accent does the chromatic work. A brand logo's native color (Claude coral, Stripe purple, Slack's four petals) doesn't count as a second accent — it's a brand mark. You can extend that brand's native color *semantically* into the composition when you're depicting that brand: e.g., Claude-speaker chat bubbles in coral alongside user bubbles in Cerulean reads as a speaker key, not as decoration. **What stays banned:** a second hue used for visual interest, gradient pairs, or "balance" — anything not tied to a brand mark already on the canvas.
- **Em dashes anywhere, display *or* body.** Use commas, colons, "and", or two short lines. Shaw reads em dashes as a tell of AI-generated copy and will flag them on sight, even at 18–20px inside card body. This applies to `—` (em dash) and `–` (en dash). At 70–84px display size an em dash *also* reads as a rendering glitch, which is the secondary reason.
- **Title Case in body copy.** Sentence case. Title Case is acceptable for a single dominant display title if the composition is heading-driven.
- **CTAs / buttons.** Infographics aren't clickable.
- **Stock-photo placeholder boxes**, "image goes here" gradient rectangles, decorative illustrations with no semantic role.
- **Pure `#000` or `#fff`.** Tint neutrals slightly toward the accent or the brand hue.

## The AI-slop check

Two altitudes — run both before declaring done.

- **First-order:** would a generic "AI tips" carousel slide look like this already? (Glowing orb, gradient background, generic icons in a 2×2 grid, "Unlock the power of AI" headline.) If yes, the visual idea has collapsed to the category default. Rework.
- **Second-order:** would a *non-generic* "anti-SaaS founder" LinkedIn graphic look like this? (Off-white bg, mono labels, one Cerulean accent, two minimal cards.) If indistinguishable from three other AI-founder posters' templates, break the pattern via structure or specificity — a directory tree, a real product UI, a named tool, a specific anecdote — not by adding decoration.

## Gotchas

Time-sinks that have actually happened. Read this list before debugging anything weird.

1. **Playwright MCP blocks `file://`** → use `scripts/render.sh` (headless Chrome subprocess). Don't try to spin up an HTTP server either — that's blocked too.
2. **`.playwright-mcp/` PNGs auto-delete** → never save final output there. Save into the project folder.
3. **CSS grid `1fr 1fr` doesn't enforce equal width** when a child has a wide non-wrapping word — add `min-width: 0` to the grid items.
4. **lobehub doesn't have non-AI logos** — Notion, Stripe, Jira, Slack, Gmail, etc. all 404 (or return ASCII). Go straight to simpleicons.org or Wikimedia.
5. **Don't fork an HTML for a "landscape variant."** When the user asks for landscape, they usually mean "make the existing one wider than tall." Adjust dimensions on the existing file rather than creating `<slug>-landscape.html`.
6. **Wikimedia thumb widths are restricted** to 20/40/60/120/250/330/500/960/1280/1920/3840. Arbitrary widths return HTTP 400. Use 500 or 960.
7. **Generic User-Agents get blocked by Wikimedia.** Use one with contact info.
8. **Logos squish when forced into square tiles.** Logos from mixed sources have mixed aspect ratios (Gmail is 4:3, Slack is 1:1, simpleicons SVGs vary). `.tile img { width: 56px; height: 56px }` stretches non-square logos to fit. Default for any logo `<img>` inside a fixed-size tile: add `object-fit: contain` so the logo scales proportionally inside the box.
9. **Heroicons stroke-width 1.5 reads as a render glitch at small sizes.** Default `stroke-width="1.5"` on a 22–32px on-canvas arrow looks like a hairline that didn't render. For arrows used as flow connectors between graphics, set `stroke-width="2.5"`–`"3"` directly on the SVG `<path>`. The icon's main subject can stay at 1.5–1.6; only the connector arrows need the bump.
10. **`flex: 1` on a grid below a heading leaves dead space.** When the canvas has a tall title block and the grid is set to `flex: 1`, the grid stretches but its *cards* (which only need their natural height) leave a band of empty bg below them. Fix: set an explicit `height` on the `.grid` matching how much vertical room the cards actually want, and let the canvas's bottom padding handle the rest. Saw this on `four-step-framework` — went from 380px → 470px to kill ~90px of dead space.
11. **Subagent / accessibility-snapshot review can't see decorative CSS-only graphics.** When you delegate visual review to a subagent that reads page snapshots (Playwright's `browser_snapshot`, anything based on the a11y tree), shapes built from `<div>` borders, backgrounds, and transforms — stacked papers, custom diagrams, painted hub graphics — report as missing or empty. The subagent will confidently say "this card has a blank where the illustration should be." Always verify against the rendered PNG before acting on a subagent's "the X is missing" claim — usually the X renders fine and only the a11y view is blind to it.

## Reference files

- `templates/landscape.html` — 1080×820, default starting point.
- `templates/portrait.html` — 1080×1350, for vertical lists.
- `templates/square.html` — 1080×1080, for single centerpieces.
- `scripts/render.sh` — render wrapper. Don't reinvent.
- `assets/README.md` — running index of bundled logos. Check before fetching, update after fetching.
- `assets/logos/` — the library. Copy out of here into project folders; don't reference directly from rendered HTML.
- `references/examples.md` — index of worked past infographics. The current canonical landscape example is `connectors-vs-skills` at `~/Documents/_stv/_content/_SFC/linkedin/2026/AI-education/connectors-vs-skills/`.

## What this skill reuses rather than restates

- **Logo-fetching patterns** are documented canonically in `~/.claude/skills/keynote/SKILL.md` § "Fetching assets from the web". The Asset library section above hits the essentials; the keynote skill has more gotchas (Wikimedia file lookup, ID conventions) if needed.
- **Composition principles** (group composition, optical symmetry, namespace-classes-by-role, structural-behind-focal) live canonically in `~/.claude/skills/animation-builder/SKILL.md`. The same rules apply minus the motion-specific parts.
- **Brand tokens** for ABA work live in `~/.claude/skills/aba-brand-system/`. Load it when needed; don't duplicate.
