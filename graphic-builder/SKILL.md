---
name: graphic-builder
description: Build single-image graphics (social stills, infographics, blog/slide diagrams, doc figures) and multi-page PDF carousels authored as HTML and rendered to a 2x retina PNG via a headless-Chrome pipeline included with this skill. An infographic is one mode; an embedded figure for a blog post or slide is another. Use whenever the user asks to make, design, build, render, or iterate on a graphic, diagram, figure, mockup, or visualization. Triggers include "make an infographic for X", "design a LinkedIn graphic", "turn this Notion brief into a visual", "make a diagram for this blog post", "build a figure for a slide", "draw a flow diagram", "how should I visualize X", "give me design directions for X", "mock up some options", "make a new version of that graphic", or any reference to producing a still PNG from a designed composition. This covers the exploration phase (deciding what to build) and iteration on an existing graphic, not only the final render. Palette defaults and brand-token handling are in the body.
---

# Graphic Builder

Author single-image graphics in HTML/CSS/SVG and render them at 2x retina to PNG with a headless-Chrome script. The engine is the same for every graphic; what changes by destination is the *packaging*.

This skill is the still-image sibling to `animation-builder` (MP4 B-roll for YouTube). Same stack, different deliverable.

A **clickable or interactive UI** (a demo someone drives live, a mock of a real app with working controls) is not a graphic: route it to `animation-builder` § "Interactive demos", which owns the app-mockup kits (`templates/gcal-ui/`, `templates/claude-ui/`) and the fluid-layout rules an interactive page needs. This skill's render pipeline only produces stills.

## What a graphic is — wordless by default

A graphic is a visual idea: marks, shapes, connectors, one relationship the eye reads in two seconds. By default it carries **no words** — no title, no caption, no footer. The post, slide, or doc the graphic sits in already supplies the language; the graphic's job is the part language does badly. When Shaw asks for a "simple graphic of X connected to Y," he means exactly that: the two marks and the connection. Adding a headline, a takeaway line, and a signature turns it into something he has to ask you to strip back twice.

Words are opt-in, and each one has to earn its place against the deletion pass in § Validation. Three things legitimately earn it: a brand mark's own wordmark, a short mono label that names a mechanism the shapes can't (`MCP`, `Connected`, a URL), and the infographic packaging below when the image genuinely has to stand alone.

**Infographics are a special case, not the starting point.** This skill grew out of an infographic builder, so a lot of its accumulated guidance (titles, scene sentences, eyebrows, footers) is about that packaging. Read that guidance as applying to the infographic sub-mode only. An infographic is a graphic that must carry its own argument because nothing around it will — a cheatsheet, a two-panel comparison shared without a post, a summary someone will save. Shaw asks for it by name ("infographic," "cheatsheet," "one-pager"). Otherwise, build the bare graphic.

## Destination — pick the packaging

The destination sets sizing, the project-folder location, and whether any packaging applies.

| If the graphic is… | Mode | Read |
|---|---|---|
| A still that accompanies a social post (LinkedIn, etc.) | social-graphic (default: wordless) | `references/modes/social-graphic.md` |
| A still that must stand alone with its own title and takeaway | social-graphic → infographic packaging | same file, § "Infographic packaging" |
| A figure embedded in a blog post, slide, or doc | embedded-graphic | `references/modes/embedded-graphic.md` |
| A multi-page PDF the reader swipes (LinkedIn document post) | carousel | `references/modes/carousel.md` |

Everything below this section is the shared engine and applies to every mode. The mode files cover only what differs: packaging, canvas sizing, and where the finished file goes.

## Core workflow (every mode)

1. **Read the brief and pick the mode** (table above). Confirm with the user: brand context (`aba-brand-system` or brand-agnostic?) and what *single* idea the graphic must land. One visual idea per graphic — if you can't name it in five words, it isn't ready to render.
2. **Pull brand tokens only** if a brand-system skill is in play. Colors, type, logo treatment, and the brand's composition reference (e.g. `aba-brand-system/references/infographic-composition.md`) — never the brand's web-composition or hero pattern.
3. **Create a project folder first** and author the HTML *inside* it from the first edit. While exploring, that folder is a scratch folder under `~/Downloads/<slug>/` (see § Ideating from scratch). The finished graphic's permanent home is decided by the surface skill it serves — `sfc-helper` owns where a LinkedIn post's graphic lives on disk — so file the winner there when done and don't guess the path from here.
4. **Author the HTML** from the matching `templates/` starter, **render via `scripts/render.sh`**, open the PNG, iterate.

**When the user shares a sketch or mockup, read it for intent, not as a spec.** A rough sketch (Keynote shapes, Excalidraw, a phone photo of a whiteboard) communicates *composition* — what connects to what, relative placement, the relationships — not pixel dimensions, exact sizing, or icon style. Its placeholder clip-art (skeuomorphic OS icons, stock shapes) is almost never the intended treatment; it's whatever was one click away. Reproduce the *structure*, render it in the brand's flat icon and type system, and confirm the icon treatment rather than copying the placeholders. Over-fitting the literal mockup wastes a round — Shaw will say "that was just a sketch, not a per-pixel spec."

## Ideating from scratch

When the brief is a direction rather than a spec ("brainstorm graphic ideas for this post," "give me a few design directions"), don't iterate one composition toward an answer. Explore wide, review in bulk, narrow, then refine. This is the workflow Shaw rated as working well; the shape matters more than any single step.

1. **Scratch folder, not the final home.** Everything lands in `~/Downloads/<slug>/`, one subfolder per direction, each with its own `assets/` copy so parallel agents can't race on the library. Only the winner gets filed (step 6). Nothing from the exploration survives it.
2. **Fan out one subagent per design philosophy.** Seed each agent with a *way of thinking* — a Swiss reductionist who works in grid and scale contrast, an illustrator who thinks in physical metaphors (cable, chain, bridge), a product designer who thinks in interface idioms (a pairing screen, a toggle, a chat composer) — not with a list of elements. A philosophy produces 3–5 materially different mockups; an element list produces one mockup with five coats of paint. Brief each agent on what the graphic must *land* (the one idea) and the hard constraints (canvas, palette, which marks, wordless), tell it to *invoke* this skill and any brand skill rather than read them, and require it to open every rendered PNG before reporting. Agents that don't look at their output ship overlaps and collisions.
3. **Contact sheet per direction.** Run `scripts/contact-sheet.py <dir>` on each subfolder and open the sheets. Shaw reviews a whole direction in one image instead of clicking through a dozen files, and so do you: this is where you catch a set that read fine in the agent's report but sits small in the canvas or collapses to the same composition three times.
   Keep one master sheet across rounds. Every new version, even a one-line tweak, goes into a rebuilt master in the same turn, numbered row-major; "replace 6" swaps that slot; the superseded master is deleted.
   **When the round produces pairs (a before/after, a bad/good), build an index page instead.** A contact sheet shows one direction; a pair has to be judged with its partner beside it, across every direction at once. `scripts/build-index.py <root>` writes a local `index.html` in the scratch folder: sidebar nav, one section per direction, each pair left/right with links to the PNG and its HTML, and a toggle that stacks the pair at the host column width so he sees it as the reader will. Rebuild it after every round; a second round replaces the first on the index rather than appending to it (Shaw asked for the old round scrapped, not archived alongside). The script pairs files named `NN-<concept>-<side>.png` and tolerates a variant suffix (`-5p`), so a refinement file still shows up; an unnumbered or renamed variant silently drops off the index, which is how one interim file went missing on `abb-approach-figures`.
4. **Narrow to one direction, then produce three variants.** One agent (or inline, if the base HTML is simple) takes the chosen mockup and changes one move per variant: drop the tiles, change the connector rhythm, swap the node, bend the geometry, change the scale. Variants of a chosen idea, not new ideas.
5. **Refine the winner inline.** Once Shaw has picked, iterate directly: recolor, resize, swap an icon. Every requested change is a *new file* with a suffix (`-black`, `-mcp`), never an overwrite. He compares variants side by side and will ask for the earlier one back.
   A refinement request names one element; everything else is already approved, so solve it by moving that element or the box that holds only it, not by changing a shared container's size or nudging a neighbor, which silently shifts parts Shaw signed off on. Treat each visual group as its own unit: aligning a QR block with a text block usually means each centered in a fixed band with equal space above and below, not a baseline chase. Judge alignment from the rendered PNG's ink rather than CSS boxes. Line boxes carry slack above caps and below baselines, and glyph side-bearings differ across sizes, so box-aligned text often looks off. Measure ink edges with a PIL scan (as in § Iterative height tuning) and correct with a small offset, and when scaling a group, anchor `transform-origin` on the edge that must stay put.
6. **File and clean up.** Copy the winner (HTML, PNG, `assets/`) to its permanent home under the slug name, re-render there to confirm the relative paths hold, then delete the scratch folder. Log the graphic in `references/examples.md` if it introduced a pattern.

Used on `youtube-mcp` (three philosophies × 4–5 mockups, then three variants of the pick, then two inline refinements), earlier on `demo-discovery-call` (six directions, then six variants of the winner), and on `abb-approach-figures` (four philosophies × 4–5 abstract pairs, then a second round of three directions re-labeled with the real customer, problem, and solution names from his research, browsed on an index page, then the tree refined inline from six problems to four). That second round is the lesson: abstract placeholders are fine for choosing a composition, but the figure only lands once it carries the user's actual labels, so ask for the real story before the refinement round, not after.

## Composition principles

- **One visual idea per graphic.** If a second idea wants in, it's a second graphic.
- **One channel owns each meaning.** A graphic is an argument about what matters, so every element that doesn't carry the argument dilutes it. If color already encodes a category, a label repeating it is redundant; if a group bracket names the group, per-item tags restating it are noise; if an icon and a chip both say "scheduled", one goes. The trap is that each addition is individually defensible ("the color needs explaining", "the icon needs a label") — defensible per element is how you arrive at an indefensible whole. Words are free to write and expensive to read: one costs you a line and costs the viewer a fixation plus a decision about whether it mattered.
- **Separate text doing visual work from text apologizing for the visual.** A 17-row list of manual steps is *texture* — its volume is the message, and it survives intact. A caption glued to a diagram element is usually a hedge against the composition not landing. Caption density is therefore diagnostic: it marks where the layout is weakest, so the fix is to strengthen the layout there rather than keep the caption. On `demo-discovery-call`, one trigger card encoded "runs daily at 6:45" four ways (clock icon, "Every morning", "Scheduled · daily", and a `6:45 AM` chip) before a pass cut it to three elements that each carry something the others don't.
- **Pick the layout from the idea, not the format.** A vs B → two panels side by side. Numbered list / progression → a vertical stack. Single centerpiece → a symmetric square. Left-to-right cause/effect → a horizontal flow with connector arrows.
- **A matched pair shares one canvas, and the half the user already likes sets the geometry.** Two figures that will sit one above the other in a column (bad approach / good approach) must be the same width and height, or they read as two unrelated images. Once the user has approved one half ("I actually like how the good side looks"), that half is fixed: its canvas size, where its root or anchor sits, its pitch. Lay the other half out *to* those numbers (same root y, same total height) rather than designing it independently and reconciling later. When the busier half won't fit in that canvas, cut its content, not the canvas: on `abb-approach-figures` the bad tree went from six problems to four so both halves rendered at one 1080×553, which also made each wider than tall as Medium prefers. Growing the canvas to fit the busy half, or shrinking the approved half to match, both undo the approval.
- **Equal-width grid columns:** `grid-template-columns: 1fr 1fr` does NOT enforce equal width when a child overflows. Add `min-width: 0` to the children. This bit us on `connectors-vs-skills` and will bite again — codified here once.
- **Equal-bottom alignment for parallel cards.** When two cards have differently-sized graphics (left = numbered steps that fill the area, right = small tile grid), bottom-anchored rows like an `e.g.` footer drift to different y-positions and the cards look misaligned. Two working patterns:
  - **Fixed graphic height** (used in `connectors-vs-skills`): set `.graphic { height: 320px }` on both cards. Works when both graphics naturally fill that height.
  - **Flex graphic, anchored footer** (used in `two-types-of-skills`): `.card { min-height: 560px; display: flex; flex-direction: column }` + `.graphic { flex: 1 }`. The graphic absorbs slack; the row after it lands at the same y-position in both cards. Use this when one graphic is sparse and centering it would otherwise look top-heavy.
- **Cross-column icon-row alignment: absolutely-position the captions.** In a horizontal diagram where some columns are a labeled box (title + icons) and others are an icon cluster *with a caption underneath*, `align-items: center` on the row aligns the *whole-element* centers — so the captioned cluster's icons float ~30–40px higher than the box's icons (the caption drags the cluster's center down). Fix: make the caption `position: absolute; top: calc(100% + 18px); left: 50%; transform: translateX(-50%)`. Now only the icons drive flow-centering, so every column's icon row lands on one horizontal line. Used on `vm-isolation` to align the "untouched files" cluster with Claude and the VM's own icons (all at y=306, measured).
- **Hang an annotation under a box without shifting the box's center.** When a box must stay vertically centered in its frame (e.g. so an external element like a globe aligns to *the box*, not the frame center) but also needs a labeled element beneath it (a downward arrow + icon + caption), don't put the annotation in normal flow — it pushes the box's center upward. Instead wrap the box in a `position: relative` column and give the annotation `position: absolute; top: calc(100% + 6px); left: 50%; transform: translateX(-50%)`. The box stays centered (so cross-figure alignment holds) and the annotation tracks its center automatically. The frame `min-height` must be large enough to contain the hanging annotation inside the border — budget `frameH/2 + boxHalf + annotationH < frameH - margin`. Used on `vm-isolation` for the "Folder-specific Access" element under the VM.
- **In a repeating card set, anchor elements at fixed positions rather than centering a variable-height block.** A vertically-centered block is positioned by its own height, and that height moves with the content: a longer heading drops to a smaller size in the type ramp, body copy wraps to a second line, one card carries an optional subtitle. Every element inside then sits at a different y on every card. On a single still nobody notices; in a sequence the reader swipes, the whole composition twitches. Give each slot a fixed offset and a reserved height — including for the optional element, whether or not that card uses it — and bottom-align type inside its box so the baseline holds as the size changes. Caught on `claude-terms-carousel`, where the term, its number, the rule, and the definition all drifted between cards.
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

Then re-render at `content-end + <bottom-margin>`. Two things to keep right: the PNG is 2x, so divide the pixel row by 2 to get logical px; and `bg` must match the canvas background (the off-white default or the brand bg) or every row reads as "content."

**The render height sets the bottom margin, not CSS.** The PIL scan lands on the *last painted pixel* — a card's bottom border, the last row of text — so anything below it (canvas `padding-bottom`, a trailing margin) is invisible cream that the content-fit render simply excludes. Editing `padding-bottom` to "add breathing room" does nothing once you refit height to content; the only lever is `content-end + <margin>` in the render command. Set the margin there.

**Don't trim flush — match an existing internal gap.** "Kill the dead space below the table" rarely means *flush* (a figure whose content touches the bottom edge looks cramped and cropped). It means make the bottom margin echo a gap the composition already establishes — most often the title→content gap. Read that gap (e.g. the title's `margin-bottom`, 36px) and render at `content-end + that-value` so top and bottom breathing room are symmetric. Bit us on `cowork-control-matrix-titled`: trimmed to ~12px, then re-did it at 36px to match the title gap.

### Why not Playwright MCP

Both verified during the `connectors-vs-skills` build:
- Playwright MCP **blocks `file://` URLs** — `browser_navigate` returns a protocol error.
- `python3 -m http.server` as a workaround is **blocked by the sandbox classifier**.

Headless Chrome via Bash subprocess accepts `file://` directly. It's the working bypass.

## Validation

Open the rendered PNG before declaring done. Don't ship blind.

- For multi-element layouts (two cards, equal columns, parallel graphics), confirm column widths match and visual elements align — bugs only show up at full size.
- **Run a deletion pass before declaring done.** Take each text element in turn — subtitle, caption, role line, legend row, per-item tag — remove it and ask what a reader actually loses. Whatever costs nothing stays removed. Do this against the rendered PNG rather than the HTML: in source every string looks load-bearing, and only at full size can you see the layout already saying it. This is what catches redundant encoding, which otherwise survives precisely because each element passed its own review.
- If something looks wrong, fix the HTML and re-render. Don't iterate on micro-tweaks the user didn't ask for.
- For spacing-sensitive work (gap equalization, optical balance), open the HTML in a regular Chrome tab and use the dev tools to read `getBoundingClientRect` on the elements you're balancing. CSS coordinates lie when text widths and padding affect the visible box.
- **Delegating the polish loop to a subagent works — but give it numeric acceptance criteria, not "make it look good."** A subagent can run the measure→adjust→re-render loop autonomously when you hand it explicit, checkable targets: "arrow's left head within 10–16px of the VM's right border", "globe center y == VM center y within 6px", "equal left/right margins within 12px", "access caption clears the frame's bottom border by 20–30px". It must measure via `scripts/render.sh` + PIL pixel-scans of the rendered PNG — *not* Playwright or a11y snapshots, which block `file://` and are blind to CSS-only shapes (see Gotchas). Vague briefs drift; numeric ones converge. Tell it to report the final measured value for each criterion so you can verify without re-deriving. Used on `vm-isolation`.
- **When a graphic asserts a factual claim about a product or tool** (e.g. "this connector drafts but cannot send", "web search is read-only"), verify it against the real source — the actual tool list, the docs, the product UI — rather than assuming. A confident-but-wrong capability claim in a diagram is worse than a vague one. (This came up building the prompt-injection pipeline: the Gmail connector genuinely has `create_draft` and no send tool, which made "drafts it, cannot send" accurate rather than a guess.) The same applies to real places: take map positions from an authoritative source (the user's map, real addresses), not recall.

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
14. **Remote web fonts can render as blank text.** Headless Chrome may screenshot before a Google Fonts stylesheet loads — `display=block` especially leaves every glyph invisible, and the PNG shows empty boxes with no error. Load fonts from local files via `@font-face` (Inter etc. live in `~/Library/Fonts`; copy them next to the HTML). Hit by two parallel agents on the same thumbnail job.
15. **Parallel agents sharing a scratch folder overwrite each other.** Render scripts and temp files with generic names collide silently. When fanning out, give each agent its own working folder and say so in the brief.
16. **Cutting a person out of a photo (thumbnails, composites).** No rembg needed — macOS Vision does clean foreground masks: a short Swift script using `VNGenerateForegroundInstanceMaskRequest` + `generateMaskedImage(ofInstances:from:croppedToInstancesExtent:false)` written out via `CIContext.writePNGRepresentation`. Put each `import` on its own line. Check the result composited on magenta before using it; light-background photos leave a faint halo that shows on dark canvases.
17. **Handing a graphic off to Canva as editable layers.** When the user wants to finish a graphic in Canva (e.g. add their own photo), don't send one flat PNG. Export each element as its own transparent PNG: inject CSS into a copy of the HTML that hides everything (`body *{visibility:hidden!important}`), re-shows one element (`.sel, .sel *{visibility:visible!important}`), and makes `html,body,.canvas` transparent. Render with Chrome directly — `render.sh` has no transparency flag — adding `--default-background-color=00000000`. Render the background as its own layer, then crop each PNG to its alpha bbox and keep the offset. Upload with Canva's `create-upload-url` (one raw-bytes POST per file; each URL works once). Place the layers into the user's design with `edit-design` `insert_fill`, in back-to-front order, at bbox ÷ render scale. Show the page previews and get a yes before `commit`.

## Reference files

- `references/modes/social-graphic.md` — the wordless default for social stills, aspect presets, and the infographic packaging sub-mode (title, footer, eyebrow rules).
- `scripts/contact-sheet.py` — labeled grid of every PNG in a folder, for reviewing a direction in one image.
- `references/modes/embedded-graphic.md` — packaging and content-fit sizing for blog / slide / doc figures.
- `references/modes/carousel.md` — page-sized sections, print-to-PDF pipeline, and design-comparison workflow for multi-page LinkedIn carousels.
- `templates/landscape.html` — 1080×820, social starting point (strip the title/body/footer blocks for a wordless graphic).
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
