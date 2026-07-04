---
name: graphic-builder
description: Build single-image graphics — social infographics, blog/slide diagrams, doc figures — authored as HTML and rendered to a 2x retina PNG via a headless-Chrome pipeline included with this skill. An infographic is just one mode; an embedded figure for a blog post or slide is another. Use whenever the user asks to make, design, build, or render an infographic, LinkedIn post graphic, social-feed still, concept image, "graphic for [post idea]", or a diagram/figure for a blog post, slide, or doc. Triggers include "make an infographic for X", "design a LinkedIn graphic", "build a post graphic", "turn this Notion brief into a visual", "make a diagram for this blog post", "build a figure for a slide", "draw a flow diagram", or any reference to producing a still PNG from a designed composition. Defaults to a brand-agnostic light palette with Manrope / Libre Franklin / JetBrains Mono type. If the graphic is for a specific brand, reference the relevant brand-system skill (e.g. `aba-brand-system`) for colors/type/voice — pull tokens only, do NOT import the brand's website composition.
---

# Graphic Builder

Author single-image graphics in HTML/CSS/SVG and render them at 2x retina to PNG with a headless-Chrome script. The engine is the same for every graphic; what changes by destination is the *packaging*.

This skill is the still-image sibling to `animation-builder` (MP4 B-roll for YouTube). Same stack, different deliverable.

## Graphic types — pick your mode first

Decide where the graphic will live *before* composing. The destination sets the packaging, the folder location, the footer, and the default sizing.

| If the graphic is… | Mode | Read |
|---|---|---|
| A standalone still for a social feed (LinkedIn, etc.) | social-infographic | `references/modes/social-infographic.md` |
| A figure embedded in a blog post, slide, or doc | embedded-graphic | `references/modes/embedded-graphic.md` |

**The destination determines the packaging.** A social still is self-contained: it carries its own editorial title, a takeaway line, and a footer signature, because nothing around it will frame it and it has ~2 seconds in a scroll to land one idea. An embedded figure carries none of that by default — the surrounding prose, slide, or doc already supplies the title and the explanation, so the graphic is *just the diagram*. Re-adding a title to an embedded figure is the author's explicit call, not a default.

Everything below this section is the shared engine and applies to every mode. The mode files cover only what differs: packaging, project-folder location, footer convention, and canvas sizing.

## Core workflow (every mode)

1. **Read the brief and pick the mode** (table above). Confirm with the user: brand context (`aba-brand-system` or brand-agnostic?) and what *single* idea the graphic must land. One visual idea per graphic — if you can't name it in five words, it isn't ready to render.
2. **Pull brand tokens only** if a brand-system skill is in play. Colors, type, logo treatment, and the brand's composition reference (e.g. `aba-brand-system/references/infographic-composition.md`) — never the brand's web-composition or hero pattern.
3. **Create the project folder first** (location is mode-specific — see the mode file) and author the HTML *inside* it from the first edit. Don't create it elsewhere and move it later.
4. **Author the HTML** from the matching `templates/` starter, **render via `scripts/render.sh`**, open the PNG, iterate.

**When the user shares a sketch or mockup, read it for intent, not as a spec.** A rough sketch (Keynote shapes, Excalidraw, a phone photo of a whiteboard) communicates *composition* — what connects to what, relative placement, the relationships — not pixel dimensions, exact sizing, or icon style. Its placeholder clip-art (skeuomorphic OS icons, stock shapes) is almost never the intended treatment; it's whatever was one click away. Reproduce the *structure*, render it in the brand's flat icon and type system, and confirm the icon treatment rather than copying the placeholders. Over-fitting the literal mockup wastes a round — Shaw will say "that was just a sketch, not a per-pixel spec."

## Composition principles

- **One visual idea per graphic.** If a second idea wants in, it's a second graphic.
- **Pick the layout from the idea, not the format.** A vs B → two panels side by side. Numbered list / progression → a vertical stack. Single centerpiece → a symmetric square. Left-to-right cause/effect → a horizontal flow with connector arrows.
- **Equal-width grid columns:** `grid-template-columns: 1fr 1fr` does NOT enforce equal width when a child overflows. Add `min-width: 0` to the children. This bit us on `connectors-vs-skills` and will bite again — codified here once.
- **Equal-bottom alignment for parallel cards.** When two cards have differently-sized graphics (left = numbered steps that fill the area, right = small tile grid), bottom-anchored rows like an `e.g.` footer drift to different y-positions and the cards look misaligned. Two working patterns:
  - **Fixed graphic height** (used in `connectors-vs-skills`): set `.graphic { height: 320px }` on both cards. Works when both graphics naturally fill that height.
  - **Flex graphic, anchored footer** (used in `two-types-of-skills`): `.card { min-height: 560px; display: flex; flex-direction: column }` + `.graphic { flex: 1 }`. The graphic absorbs slack; the row after it lands at the same y-position in both cards. Use this when one graphic is sparse and centering it would otherwise look top-heavy.
- **Cross-column icon-row alignment: absolutely-position the captions.** In a horizontal diagram where some columns are a labeled box (title + icons) and others are an icon cluster *with a caption underneath*, `align-items: center` on the row aligns the *whole-element* centers — so the captioned cluster's icons float ~30–40px higher than the box's icons (the caption drags the cluster's center down). Fix: make the caption `position: absolute; top: calc(100% + 18px); left: 50%; transform: translateX(-50%)`. Now only the icons drive flow-centering, so every column's icon row lands on one horizontal line. Used on `vm-isolation` to align the "untouched files" cluster with Claude and the VM's own icons (all at y=306, measured).
- **Hang an annotation under a box without shifting the box's center.** When a box must stay vertically centered in its frame (e.g. so an external element like a globe aligns to *the box*, not the frame center) but also needs a labeled element beneath it (a downward arrow + icon + caption), don't put the annotation in normal flow — it pushes the box's center upward. Instead wrap the box in a `position: relative` column and give the annotation `position: absolute; top: calc(100% + 6px); left: 50%; transform: translateX(-50%)`. The box stays centered (so cross-figure alignment holds) and the annotation tracks its center automatically. The frame `min-height` must be large enough to contain the hanging annotation inside the border — budget `frameH/2 + boxHalf + annotationH < frameH - margin`. Used on `vm-isolation` for the "Folder-specific Access" element under the VM.
- **Optical vs. geometric symmetry, group composition, structural-behind-focal, namespace-classes-by-role** — these all apply identically here. See `~/.claude/skills/animation-builder/SKILL.md` § "Motion principles" and § "Composition and storytelling principles" for the canonical write-up; the same rules apply minus the motion-specific parts.
- **Each card / panel = three elements max:** one heading word, one supporting line, one graphic. Same rule as section cards in `animation-builder`.
- **Left-align body copy and headings** unless the composition is explicitly symmetric (single-centerpiece squares, or a centered horizontal flow, are the typical exceptions).
- **Fill the frame; don't pad a guess.** A list or catalog of full-width cards carrying one short line of body text under-fills both axes — whitespace pools to the right of each card and below the last one. Two fixes applied together: (1) scale the title, names, and icon tiles up until the body line carries most of the card width, and (2) size the canvas to the *measured* content height (see Rendering § "Iterative height tuning") instead of a guessed `min-height`. On `non-coding-skills` this meant title 60→72px, names 32→42px, tiles 74→92px, and sizing to ~1555px of measured content rather than a fixed 1350 — which closed both the right-edge and bottom gaps.

## Type & color

- When a brand-system skill is loaded (`aba-brand-system`), use its tokens. Pull, don't fork.
- **Default brand-agnostic palette:**
  - `--bg: #FAFAF7` for light mode (the templates' default)
  - `oklch(0.16 0.01 250)` for dark mode
  - One accent doing the heavy lifting — whichever accent the loaded brand-system skill defines (e.g. ABA's Cerulean `#087CA7`), or, with no brand, a single muted accent chosen from the brief. Never two competing accents.
- **A semantic color-key is the sanctioned exception to "one accent."** The one-accent rule bans color used for *decoration or balance* — not color used to *carry meaning*. When the user wants to color-code object or entity types (files vs. folders vs. programs; safe vs. danger; read vs. write tools), that's a legitimate key, not a rainbow: assign each type a distinct hue, pull every hue from the brand palette rather than inventing one, keep them at consistent saturation so they read as a system, and reuse the same assignment everywhere those types reappear. On `vm-isolation` this was files=Cerulean, folders=Goldenrod, programs=gray, approved-domains=green — five colors, all semantic, all on-brand, repeated identically inside and outside the VM. (Same principle as the "second hue carrying genuine semantic meaning" allowance in Absolute bans, extended to a multi-type key.)
- **Cream reads as warm only against white.** `--bg: #FAFAF7` is nearly white on its own — it only reads as the intended warm off-white when it frames a white `--surface`. A full-bleed cream graphic with no white card looks flat white, and sits inconsistently beside sibling figures that do use cards. When a graphic is essentially one content block (a table, a list, a single panel), seat it on a `--surface` card and let the cream show as a margin; that contrast is what makes the background look intentional. This bit us on `cowork-control-matrix` — three rounds to find that "the background changed" was really "there's no white card for the cream to read against."
- **Default type stack:**
  - Display: **Manrope** 700/800, tracking `-0.02em` at large sizes
  - Body: **Libre Franklin** 400–600, line-height ~1.4
  - Labels / badges / footer / code: **JetBrains Mono** 400–600

## Icons — Heroicons first, never hand-drawn

**Default to Heroicons outline paths for every UI metaphor in the graphic.** Do not hand-draw SVG paths for user, document, chat-bubble, arrow-long-down / -up / -right / -left, arrows-right-left, plus, minus, arrow-path (refresh), computer-desktop, clock, sparkles, check, x-mark, etc. Heroicons covers ~90% of what a graphic needs, the paths are public, and a hand-drawn icon will always look slightly off next to a real one.

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

**A brand logo sharing a row with monochrome icons should be monochrome too.** When the icon set is a single accent (Heroicons tinted with the accent), a full-color brand PNG in the same row reads as a sticker. Fetch the brand's single-path simpleicons SVG — its `<path>` carries no `fill`, so it inherits `currentColor` — and tint it like any other icon (`fill="currentColor"` on the SVG, accent on the tile). The library keeps both variants for some brands: the full-color raster (`claude.png`) for when the logo stands alone as the brand mark, the mono SVG (`claude.svg`, `chrome.svg`) for when it's one icon among many. simpleicons' single-color output — a downside when you actually want the real multicolor mark (§ "Asset library") — is exactly what you want here. Used on `cowork-control-matrix` for the Chrome logo in a Cerulean icon column.

## Asset library — the bundled `assets/logos/`

The skill ships with a growing library of logos. **Before fetching anything from the web, `ls ~/.claude/skills/graphic-builder/assets/logos/` and read `assets/README.md`.** If the asset exists, copy it into the project's local `assets/` folder and reference it relatively.

### Workflow when an asset is missing

1. **Fetch it** (source priority below).
2. **Save to BOTH** `~/.claude/skills/graphic-builder/assets/logos/<name>.<ext>` (the library) AND the project's local `assets/` folder (the working copy).
3. **Append a one-line entry to `~/.claude/skills/graphic-builder/assets/README.md`** in the format `<name> — <source>, brand color (if any), <date>`. The README is the index; without an entry the file is invisible to future runs.

### Source priority

In order — try each before falling to the next.

**AI brand logos** (Claude, ChatGPT, Gemini, Cursor, Perplexity, Mistral, etc.) — lobehub CDN:

```bash
curl -sL -A "GraphicBuilder/1.0" \
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
curl -sL -A "GraphicBuilder/1.0 (shawhintalebi@gmail.com)" \
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

For a light-bg graphic (`--bg: #FAFAF7`) the dark/color variant is correct. For a dark-bg graphic, fetch the white-stroke variant or recolor an SVG's `fill`. **Always open the file before inserting** — a "missing logo" is usually white-on-white or black-on-black.

### What goes in the library vs. what doesn't

- **In the library:** logos, brand marks, reusable iconography.
- **Project-only:** one-off graphics (hand-drawn diagrams, custom illustrations, screenshots specific to a single post). Don't pollute the library with single-use assets.

## Rendering — `scripts/render.sh`

The renderer is a thin Bash wrapper around headless Chrome. **Use it, not Playwright MCP.**

```bash
~/.claude/skills/graphic-builder/scripts/render.sh \
  /abs/path/to/<slug>.html [--size square|portrait|landscape|WxH] [--out <png-path>]
```

Defaults: `--size landscape` (1080×820), `--out <html-dir>/<basename>.png`. The `WxH` escape hatch covers everything the presets don't: content-fit embedded figures (`--size 1080x4000` then trim, below) and 16:9 slides (`--size 1920x1080`).

Under the hood it invokes:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=<W>,<H> --force-device-scale-factor=2 \
  --screenshot=<output.png> "file://<absolute-html-path>"
```

`--force-device-scale-factor=2` gives 2x retina output (e.g. 1080×820 logical → 2160×1640 actual). 2x keeps the output crisp wherever it lands — feed compression, blog image scaling, projector scaling all eat sharpness; ship at 2x always.

### Iterative height tuning

Variable-height graphics (embedded figures sized to content, cheatsheets, long lists) need their canvas height matched to content. Don't guess in 100px steps — you'll burn 3–5 renders. Instead: render once with a generous height (`--size 1080x4000`), open the PNG, measure where content actually ends, then re-render at `content-end + ~40px`. One miss-render plus one final, instead of binary-searching.

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
- **Delegating the polish loop to a subagent works — but give it numeric acceptance criteria, not "make it look good."** A subagent can run the measure→adjust→re-render loop autonomously when you hand it explicit, checkable targets: "arrow's left head within 10–16px of the VM's right border", "globe center y == VM center y within 6px", "equal left/right margins within 12px", "access caption clears the frame's bottom border by 20–30px". It must measure via `scripts/render.sh` + PIL pixel-scans of the rendered PNG — *not* Playwright or a11y snapshots, which block `file://` and are blind to CSS-only shapes (see Gotchas). Vague briefs drift; numeric ones converge. Tell it to report the final measured value for each criterion so you can verify without re-deriving. Used on `vm-isolation`.
- **When a graphic asserts a factual claim about a product or tool** (e.g. "this connector drafts but cannot send", "web search is read-only"), verify it against the real source — the actual tool list, the docs, the product UI — rather than assuming. A confident-but-wrong capability claim in a diagram is worse than a vague one. (This came up building the prompt-injection pipeline: the Gmail connector genuinely has `create_draft` and no send tool, which made "drafts it, cannot send" accurate rather than a guess.)

## Absolute bans (match-and-refuse)

If you're about to write any of these, rewrite the element with different structure.

- **Gradient text** (`background-clip: text` with a gradient). Emphasize through weight, size, or solid color contrast.
- **Glowing AI orbs, sparkle particles, neon edges.** First-order training-data reflex. If the graphic is about AI, the visual idea must come from the specific point, not the topic's vocabulary.
- **Multiple competing *decorative* accent colors.** One accent does the chromatic work. A brand logo's native color (Claude coral, Stripe purple, Slack's four petals) doesn't count as a second accent — it's a brand mark. You can extend that brand's native color *semantically* into the composition when you're depicting that brand: e.g., Claude-speaker chat bubbles in coral alongside user bubbles in Cerulean reads as a speaker key, not as decoration. A second hue carrying genuine semantic meaning (danger red vs. safe cerulean) is also allowed. **What stays banned:** a second hue used for visual interest, gradient pairs, or "balance" — anything not tied to a brand mark or a semantic role.
- **Em dashes anywhere, display *or* body.** Use commas, colons, "and", or two short lines. Shaw reads em dashes as a tell of AI-generated copy and will flag them on sight, even at 18–20px inside card body. This applies to `—` (em dash) and `–` (en dash). At 70–84px display size an em dash *also* reads as a rendering glitch, which is the secondary reason.
- **Title Case in body copy.** Sentence case. Title Case is acceptable for a single dominant display title if the composition is heading-driven.
- **CTAs / buttons.** A still graphic isn't clickable.
- **Stock-photo placeholder boxes**, "image goes here" gradient rectangles, decorative illustrations with no semantic role.
- **Pure `#000` or `#fff`.** Tint neutrals slightly toward the accent or the brand hue.

## The AI-slop check

Two altitudes — run both before declaring done.

- **First-order:** would a generic "AI tips" carousel slide look like this already? (Glowing orb, gradient background, generic icons in a 2×2 grid, "Unlock the power of AI" headline.) If yes, the visual idea has collapsed to the category default. Rework.
- **Second-order:** would a *non-generic* "anti-SaaS founder" graphic look like this? (Off-white bg, mono labels, one Cerulean accent, two minimal cards.) If indistinguishable from three other AI-founder posters' templates, break the pattern via structure or specificity — a directory tree, a real product UI, a named tool, a specific anecdote — not by adding decoration.

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
12. **A monospace sub-label that starts with `(` looks indented under the line above.** Stacking a parenthetical line (`DIRECT CONTROL` over `(admin sets)`) in JetBrains Mono leaves the `(` visually inset from the cap letter above — the glyph carries left side-bearing, and letter-spacing doesn't touch the first glyph. The text boxes are actually flush; only the ink looks off. Pull it back with `text-indent: -0.2em` on the sub-line. Same fix for any mono line led by a narrow punctuation glyph.
13. **A `position:relative` container paints over an unpositioned connector, regardless of DOM order.** A connector arrow placed *after* a bordered card in the DOM still renders *behind* it when the card has `position:relative` — positioned elements paint above non-positioned siblings, so source order doesn't save you. The arrow looks clipped, hidden, or "behind the box." Fix: give the connector its own stacking context with `position:relative; z-index:<n>` so it joins the positioned layer and paints on top. Bit us on `vm-isolation` — the VM↔domains arrow disappeared behind the "Your Computer" frame until the arrow got a z-index.

## Reference files

- `references/modes/social-infographic.md` — packaging, folder convention, footer, and aspect presets for social-feed stills.
- `references/modes/embedded-graphic.md` — packaging, folder convention, and content-fit sizing for blog / slide / doc figures.
- `templates/landscape.html` — 1080×820, social-infographic starting point.
- `templates/portrait.html` — 1080×1350, for vertical lists (social).
- `templates/square.html` — 1080×1080, for single centerpieces (social).
- `templates/embedded.html` — content-fit, no footer, for embedded blog/slide/doc figures.
- `scripts/render.sh` — render wrapper. Don't reinvent.
- `assets/README.md` — running index of bundled logos. Check before fetching, update after fetching.
- `assets/logos/` — the library. Copy out of here into project folders; don't reference directly from rendered HTML.
- `references/examples.md` — index of worked examples, grouped by mode.

## What this skill reuses rather than restates

- **Logo-fetching patterns** are documented canonically in `~/.claude/skills/keynote/SKILL.md` § "Fetching assets from the web". The Asset library section above hits the essentials; the keynote skill has more gotchas (Wikimedia file lookup, ID conventions) if needed.
- **Composition principles** (group composition, optical symmetry, namespace-classes-by-role, structural-behind-focal) live canonically in `~/.claude/skills/animation-builder/SKILL.md`. The same rules apply minus the motion-specific parts.
- **Brand tokens** for ABA work live in `~/.claude/skills/aba-brand-system/`. Load it when needed; don't duplicate.
