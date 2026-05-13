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

## Workflow

1. **Read the brief.** Usually a Notion post idea. Confirm with the user: aspect ratio, brand context (`aba-brand-system` or brand-agnostic?), and what *single* idea the graphic must land.
2. **Write the scene sentence.** Before opening the template: who's scrolling LinkedIn, what they should understand in 2 seconds, what feeling it should leave. "A graphic comparing X and Y" is not a scene. "A founder scrolling at lunch realizes that 'connectors' and 'skills' aren't synonyms — one gives Claude access, the other gives it competence — and remembers it because the right side has a directory tree she's seen on her own machine" is.
3. **Pick aspect ratio.** Default landscape (1080×820). Portrait (1080×1350) for vertical lists or stacks. Square (1080×1080) for single centerpieces with symmetric margin. Don't reflexively pick square — landscape and portrait read fine in-feed.
4. **Create the project folder first.** See "Project folder convention" below. Author the HTML *inside* it from the first edit.
5. **Pull brand tokens only** if a brand-system skill is in play. Colors, type, logo treatment. Not layout. Not hero composition.
6. **Author the HTML** from the matching template in `templates/`, **render via `scripts/render.sh`**, eyeball the PNG, ship.

## Project folder convention

**Every infographic gets its own folder. Create it first, before writing any HTML.** No loose HTMLs or PNGs in shared directories.

- **Folder name:** kebab-case slug matching the topic — `connectors-vs-skills/`, not `infographic-2026-05/`.
- **Folder location:** `/Users/shaw/Documents/_stv/_content/_SFC/linkedin/<year>/<category>/<slug>/`. `<category>` is typically `AI-education`, `misc`, or a similar topical group. If the category isn't obvious from the brief, ask.
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

**When a brand-system skill is loaded, this rule gets *harder*, not softer.** ABA's canonical hero is eyebrow + 2-line H1 + 1-sentence subhead + CTA. Do not transfer that pattern to the infographic. A LinkedIn still gets a title and the body content; eyebrows and subtitles are dead weight that push the actual payload below the fold and make the graphic read as a website screenshot instead of a still. If you find yourself writing both a subtitle and a brand-system eyebrow, the subtitle is the one to delete, and probably the eyebrow too.

**Left-align body copy and headings** unless the composition is explicitly symmetric (single-centerpiece square graphics are the typical exception).

## Composition principles

- **One visual idea per graphic.** If a second idea wants in, it's a second graphic.
- **Pick the layout from the idea, not the format.** A vs B → landscape with two panels. Numbered list / progression → portrait. Single centerpiece → square.
- **Equal-width grid columns:** `grid-template-columns: 1fr 1fr` does NOT enforce equal width when a child overflows. Add `min-width: 0` to the children. This bit us on `connectors-vs-skills` and will bite again — codified here once.
- **Optical vs. geometric symmetry, group composition, structural-behind-focal, namespace-classes-by-role** — these all apply identically here. See `~/.claude/skills/animation-builder/SKILL.md` § "Motion principles" and § "Composition and storytelling principles" for the canonical write-up; the same rules apply minus the motion-specific parts.
- **Footer:** `@shawhintalebi` in JetBrains Mono, ~14px, ~60% opacity, bottom-center. Quiet signature, not a brand stamp.

## Type & color

- When a brand-system skill is loaded (`aba-brand-system`), use its tokens. Pull, don't fork.
- **Default brand-agnostic palette:**
  - `--bg: #FAFAF7` for light mode (the templates' default)
  - `oklch(0.16 0.01 250)` for dark mode
  - One accent doing the heavy lifting — Cerulean `#087CA7` if ABA-aligned, otherwise whatever the brief names. Never two competing accents.
- **Default type stack:**
  - Display: **Manrope** 700/800, tracking `-0.02em` at large sizes
  - Body: **Libre Franklin** 400–600, line-height ~1.4
  - Labels / badges / footer / code: **JetBrains Mono** 400–600

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
- **Multiple competing accent colors.** One accent. Always.
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
