---
name: animation-builder
description: Build short motion-graphic animations (1–6 seconds) as B-roll overlays for talking-head YouTube videos — icon morphs, label fade-ins, diagrams that draw themselves, side-by-side comparisons, simple flow charts. Use this skill whenever the user asks to create, design, or render an animation, motion graphic, B-roll clip, explainer overlay, or any short visual that needs to be exported as an MP4. Triggers include "make an animation for X", "build a motion graphic", "I need B-roll for this script", "animate the [icon/label/curve/flow]", "render this as a video", "create a short clip that shows X morphing into Y", or any reference to producing a video file from a designed animation. Also fire when the user pastes a video script that contains `[ANIMATION]` callouts and asks to build them. Each animation is authored as a self-contained HTML file (CSS/SVG animations) and rendered to MP4 via a Playwright + ffmpeg pipeline included with this skill. Defaults to Heroicons outline icons. If the animation is for a specific brand, reference the relevant brand-system skill (e.g. aba-brand-system) for colors/type/voice — this skill itself is brand-agnostic.
---

# Animation Builder

Author short motion graphics in HTML/CSS/SVG, render them frame-accurate to MP4 with a Playwright + ffmpeg pipeline. The output drops directly into a video editor as B-roll over talking-head footage.

## Why HTML/CSS, not Manim or Remotion

- **HTML/CSS** gives full control over typography, colors, and brand tokens. CSS keyframes + SVG cover 95% of B-roll motion (fades, scales, draws, morphs, slides).
- **Manim** has a strong "3Blue1Brown" aesthetic that often reads as off-brand on a personal channel.
- **Remotion** is great but heavier setup (Node + React project). Reach for it only when the user is generating many composable animations per video and wants reusable components.

## Workflow

1. **Read the brief.** If the user pasted a script with `[ANIMATION]` callouts, treat each one as a separate clip. Confirm scope — which animation(s), how long each, target aspect ratio (default 1920×1080 / 16:9).
2. **Write the scene sentence.** Before opening the template, write one sentence stating: what the voice-over is saying when this clip is on screen, what idea the clip must reinforce, and what feeling it should leave. "An icon morphs" is not a scene. "Under the line *'…and that's when the wrench becomes a screwdriver'*, a wrench rotates and resolves into a screwdriver — quick, confident, no theatrics" is. If the sentence doesn't force the timing and the motion, add detail until it does.
3. **Check for brand context.** If the animation belongs to a specific brand (e.g. AI Builder Academy), invoke the matching brand-system skill (e.g. `aba-brand-system`) and use its colors/type/voice. Otherwise default to a tinted-neutral dark palette (see "Color hygiene") and system-ui fonts.
4. **Gather assets.** See "Asset library" below. If a needed logo/icon isn't already in `assets/`, fetch it (see "Fetching new assets") and save it into `assets/` so future animations can reuse it.
5. **Author the HTML** using `templates/starter.html` as the base for animations, or `templates/card.html` for static section/chapter cards. See "Folder and naming convention" below for where the file goes.
6. **Render to MP4** with `scripts/render.py`. Don't roll your own render — the script handles frame-accurate seeking, a Playwright bug, and YouTube-safe encoding.
7. **Verify** by reporting the output path, duration, and one or two sentences on what was animated. Don't repeatedly re-render unless the user asks for changes.

## Folder and naming convention

A video typically has many B-roll clips (a single talking-head video might call for 6–15). Without convention, the rendered MP4s end up scattered, named ad-hoc, and the editor can't tell which clip plays when. Use this layout for every video:

```
<video-folder>/
  assets/
    1-animation-split_screen.mp4
    2-card-mindset_shift.mp4
    3-animation-effort_curve.mp4
    …
    src/
      01-split-screen/
        01-split-screen.html
        claude-color.png       ← per-clip assets sit alongside the HTML
      02-mindset-shift/
        02-mindset-shift.html
      03-effort-curve/
        03-effort-curve.html
      …
```

**Always create an `assets/` folder** when starting on a new video. The rendered MP4s live there.

**`src/` lives *inside* `assets/`**, not as a sibling. This keeps source HTML, supporting PNGs, and the rendered outputs as one portable bundle — the editor only ever opens `assets/`, but if anything needs re-rendering or tweaking, the source is one folder deeper.

**Each clip's HTML lives in its own subfolder inside `src/`.** Per-clip assets (logos, supporting PNGs) live alongside the HTML in that subfolder. The HTML references them by relative path (`./claude-color.png`), and the renderer resolves them from the subfolder naturally.

### Why each clip gets its own subfolder

The renderer (`scripts/render.py`) writes per-frame PNGs to a `.frames-*/` directory *sibling to the HTML*. If two clips render in parallel from the same flat `src/`, their staging dirs collide and the encoded MP4s end up with cross-contaminated content (clip 5 ending up with clip 4's frames, etc.). Putting each HTML in its own subfolder makes the collision structurally impossible. (The renderer also UUID-suffixes its own staging dir as a safety net — see "Rendering pitfalls" below — but the subfolder convention is the right human-facing default.)

### Naming convention

**MP4s:** `N-type-human_readable.mp4` where:

- `N` — the clip's order of appearance in the video (1, 2, 3, …). No zero-padding on the MP4 name. The number IS the editor's index; `ls assets/` should read in playback order at a glance.
- `type` — `animation` or `card` (or another category if the video introduces one — `lower-third`, `overlay`, etc.). Keeps animated B-roll visually distinguishable from chapter slates.
- `human_readable` — 1–3 underscore-separated words. The thing the clip IS, not the thing it's about. (`split_screen` not `motivation_open`; `effort_curve` not `step_3_visual`.)

Examples: `1-animation-split_screen.mp4`, `2-card-mindset_shift.mp4`, `12-animation-distill_funnel.mp4`.

**HTML sources:** `NN-short-name/NN-short-name.html` (zero-padded `NN`) inside `assets/src/`. The zero-pad on the subfolder name matters because directory listings in `src/` are alphabetical — `01`, `02`, … sorts correctly; `1`, `2`, …, `10`, `11` doesn't. Subfolder name matches the HTML basename for navigability.

Pair the numbers: `01-split-screen/01-split-screen.html` renders to `1-animation-split_screen.mp4`. The HTML name doesn't need the `type` segment — the `assets/src/` location already implies "source."

### Why this convention

- The `N` prefix gives the editor a sortable playback order. No metadata lookup, no script-cross-referencing — `ls assets/` is the storyboard.
- The `type` segment lets the editor filter at a glance (`ls assets/ | grep card`) and signals which clips are chapter slates vs. concept animations.
- The shared `assets/` folder means everything an editor needs to import lives in one place.
- The nested `src/<clip-name>/` subfolders isolate each clip's render workspace and supporting assets, so parallel renders are safe and per-clip iteration doesn't pollute siblings.

## Section cards (chapter slates) — minimal by default

Section cards (full-bleed chapter slates marked `[CARD]` in a script, file type `card` in the naming convention) are a different deliverable than concept animations. They're on screen for 1–2 seconds while the voice-over names the next section. Viewers don't read them — they pattern-match.

Strip to three elements max:

1. **Eyebrow** (e.g. `STEP 0`, `PART 01`, `THE MINDSET`) — small, accent-colored, generously tracked.
2. **Title** — large, the section name, Title Case.
3. **(Optional) thin progress rail** at the bottom — only if the card is part of a numbered series of three or more.

Don't add: logos, frame marks ("Chapter 01 / 05" in the corner), pagination, signatures, body copy, supporting glyphs, decorative dividers. If a brand-system skill (`aba-brand-system`, etc.) is loaded, use its color and type tokens, but **don't import its hero composition** — landing-page chrome doesn't translate to a 1-second slate.

Author cards from `templates/card.html` (static — no keyframes), not `templates/starter.html` (which has animation scaffolding).

**Render cards at 6 seconds by default** (`--duration 6`). Since the card is static, the rendered length is just slack for the editor — the editor cuts to whatever the VO actually needs (typically 1–2s). Giving them 6s of held frame means they can extend the card if the VO runs long, freeze on it during a pause, or trim freely without running out of footage. Shorter renders (2–3s) regularly turn out to be too tight in the edit and force a re-render.

### Series-of-cards principles

When a video has multiple section cards (typical for step-by-step structures), three things have to be planned across the series before the first one renders:

- **Eyebrow numbering is single-digit.** `STEP 0`, `STEP 1`, `PART 1`. Zero-padding (`STEP 00`, `STEP 01`) is for file names so listings sort alphabetically; on screen it reads as bureaucratic.
- **Title-internal visual marks are not the accent color.** When a title contains a structural element (e.g. `Tool → Intern` — the arrow is part of the title's reading), color it with the title color (bone/white), not the brand accent. The accent belongs to elements *outside* the title: the eyebrow and the progress rail. One saturated accent per card, and the title is not where it goes.
- **Progress rails need a counting scheme decided up front.** Common pitfall: an intro/framework card and the first numbered step both render at "1 of N" — visually identical, narratively distinct, and viewers read it as a glitch. Options for an intro card that precedes a numbered sequence:
  - Omit the rail entirely (the intro isn't a step).
  - Show the rail with zero fill (the journey hasn't started).
  - Roll the intro into the count: intro = 1/(N+1), step 1 = 2/(N+1), …
  
  Don't have two sequential cards display the same fill percentage.

## Authoring an animation (the HTML)

Copy `templates/starter.html` into the working folder and edit. The template gives you:

- A 16:9 `.stage` that fills any viewport at the right aspect ratio.
- Optional radial glow background (delete if not wanted).
- A `.scene` centering container.
- Sample CSS keyframes with the canonical timing pattern (see below).
- `prefers-reduced-motion` fallback.

### Timing pattern that works

B-roll clips for talking-head edits **do not loop** — the editor cuts in, holds, and cuts out. The composed final state IS the asset. Build elements in, settle them, and hold. No tail fade-out, no reset-to-start.

The pattern, for a build-in clip with N elements:

```
0.00s             : first element begins fading in
…                 : subsequent elements stagger in (100–200ms apart)
[last beat]       : final element reaches its destination state
[last beat] + 2s  : minimum end of clip (the held final frame)
```

Two rules that follow from this:

- **Hold the final frame for at least 2 seconds.** Total clip duration = (time of the last build-in beat) + ≥2 seconds of held composed state. Anything shorter forces the editor to time-stretch or cut before the viewer absorbs the composition.
- **`animation-fill-mode: forwards` on every element.** Without it the element snaps back to its `0%` state after the keyframe ends. The composed final frame IS the deliverable — protect it.

For a morph-style clip (icon A → icon B), the same logic: state B is the destination, and it should hold for ≥2 seconds after the transition completes. State A only needs the briefest pre-roll (200–400ms) to be readable before the morph; the asset's job is to leave the viewer on state B, not on the transition itself.

If the script's voice-over names elements in a specific order, the build-in must match that order. The first thing the narrator says becomes the first thing on screen; reversing the order forces the viewer to re-resolve what they just heard.

### Motion principles

- **Subtle.** No bounces, no spring physics, no theatrical rotates. The motion should feel inevitable, not performative.
- **Easing by role.** Use ease-out (e.g. `cubic-bezier(0.16, 1, 0.3, 1)` — exponential out) for elements *entering* or settling into place; the deceleration reads as confidence. Use `cubic-bezier(0.4, 0, 0.2, 1)` (Material "standard" in-out) for A→B morphs and cross-fades where both sides need symmetry. Default `ease-in-out` is fine for short pulses. Linear is almost always wrong.
- **Transform and opacity only.** Animate `transform` (translate/scale/rotate) and `opacity`. Don't animate `width`, `height`, `top`, `left`, `margin`, or `padding` — they trigger layout, look mushy, and read as amateurish even when rendered offline.
- **Short distances.** A 4–8px translate is more sophisticated than a 40px slide. Large travel reads as ad-tech.
- **Cross-fade with scale.** When morphing A→B, fade A out at scale 0.85, fade B in at scale 0.85→1. The slight scale change reads as transformation, not just dissolve.
- **One thing at a time.** If two elements move simultaneously, the eye misses both. Stagger by 100–200ms.
- **If two elements must look identical, they must be the same component.** Parallel arrows, mirrored connectors, repeated chips — author one SVG (or CSS class) and instance it. Hand-duplicated markup drifts: stroke widths diverge, arrowheads end up subtly different, and the eye catches it even when the geometry is "close enough." The skill check: if you find yourself copy-pasting markup and then editing the copy, stop and factor it.
- **Glow follows the visual subject.** The starter template ships one centered radial glow, which is right for single-focus compositions. When the composition has two or more focal points (split-screen, before/after, multi-column), use one narrower glow per focus rather than a single wide center wash — the wash sits in dead space between artifacts and weakens both. Mirror the layout's structure in the background, not the canvas's geometric center.
- **Optical vs. geometric symmetry.** Equal *center-to-center* spacing can still read as unequal when adjacent elements have very different chrome (a bordered chat bubble next to a borderless icon, a logo with soft rays next to a hard rectangle). Balance on visual *edges* and *weight*, not just on coordinates. If math says it's even but it looks wrong, trust the eye and adjust. This bites every horizontal flow row (`A → arrow → B → arrow → C`) where A, B, and C have different visible widths: centering each arrow equidistant from B's center doesn't produce visual symmetry — the gap that matters is from A's right *edge* to the arrow's start, and from the arrow's end to B's left edge. There are four such edge-gaps in a five-element flow; balance those, not the centers. CSS coordinates won't tell you the widths (text bubbles, padding, icon rendering all affect the visible box), so the reliable workflow is to load the page in a browser and read `getBoundingClientRect` for each element.

### Color hygiene

- **Never `#000` or `#fff`.** Pure black crushes under YouTube's H.264 encoder and produces banding around glowing edges; pure white blooms. Tint every neutral slightly toward the brand hue (or warm/cool by a few percent). A dark B-roll background should be something like `oklch(0.16 0.01 250)`, not `#000`.
- **One accent does the heavy lifting.** A motion clip has just a few seconds to land — a five-color palette competes with itself. Pick one accent for the thing being emphasized; let everything else be tinted neutral.
- **Mind the codec.** Very thin strokes on saturated backgrounds (e.g. 1px cyan on near-black) shimmer after compression. If a stroke is critical, use ≥1.5px or add a faint glow rather than relying on a hairline.

### Absolute bans (match-and-refuse)

If you're about to write any of these, rewrite the motion or the element with different structure. These aren't style preferences — they are the things that make a B-roll clip read as AI-generated or asset-store-bought.

- **Spring/elastic/bounce easing.** `cubic-bezier` curves with overshoot (y > 1 or y < 0), or any easing named `back`, `bounce`, `elastic`. Reads as Lottie-template motion.
- **Theatrical rotation.** Anything that spins more than ~15° as a transition. Icons that flip, gears that whirl 360°, "loading" rotations as decoration. A subtle 4–8° tilt during a morph is the ceiling.
- **Gradient text.** `background-clip: text` with a gradient fill. Use a single solid color; emphasize through weight, size, or color contrast.
- **Glowing AI orbs / sparkle particles for "AI" topics.** First-order training-data reflex. If the clip is about AI, the visual idea must come from the *specific* point being made (a tool changing shape, a chain of steps, an annotation appearing on a doc) — not the generic vocabulary of "AI-ness."
- **Counting-up numbers with bounce.** The dashboard cliché. Numbers should appear in their final state or cross-fade between values; they should not tick up like a slot machine.
- **Drop shadows on flat illustration.** A flat icon with a soft drop shadow is uncanny. Either commit to depth (consistent light source, multiple shadow layers) or stay flat.
- **Layout-property animation.** See above — `width`/`height`/`top`/`left` transitions. Always rewrite as `transform: scale()` or `translate()`.

### Text and copy in animations

- **Every word earns its place.** A label that just restates what the icon already shows is noise. If the icon is a wrench, the label isn't "Wrench" — it's the *role* the wrench plays in the point being made.
- **No em dashes.** Use commas, colons, parentheses, or two short labels. Em dashes in 80px display type look like glitches at distance.
- **Sentence case for labels, not Title Case.** Title Case in motion graphics reads as PowerPoint.
- **Section/chapter card titles are the exception — use Title Case.** Full-bleed chapter slates are read as titles, not labels, and Title Case matches how the script's section headings are written (so the editor doesn't retype anything), reads faster at the 1-second glance, and lands like a title card rather than a sentence fragment. Keep the rest of the card in sentence case (eyebrows, sub-labels). This overrides any brand-system skill that prefers sentence case for headings — brand-system casing rules are scoped to the brand's website/app surfaces, not to YouTube chapter slates. See the "Section cards" section above for the full minimal-card pattern.

### The AI-slop check

Before rendering, ask: if someone saw this clip with no context, could they say "AI made that" without doubt? Common tells:
- **First-order:** the visual idea is the category's vocabulary (AI = orb/sparkles, data = bars/lines, security = shield/lock). Rework until the visual idea comes from the specific point, not the topic.
- **Second-order:** the motion is the genre's default (everything floats up and fades, everything has a sheen). If a stock-footage site would already have ten clips like this, change either the structure or the timing — not just the color.

### Composition and storytelling principles

These are principles, not rules. Each forces a judgment call. When the first instinct violates one, the second pass should ask *why* before committing.

- **Compose the group, not the element.** A scene with two or more focal elements needs both positions chosen together — anchor one element to an edge and the visual center drifts. "Center the conversation" means the whole thread, not just one column's bubbles. Test: if you removed one element, would the remaining composition still look balanced? If not, you were balancing one element, not the group.

- **Only animate what should pull focus.** Build-in animations communicate "look at this." Context — the setup, the framing, the world the transformation happens inside — can be present from t=0. The viewer doesn't need a fade-in on every element. Reserve motion for the focal change. Test: name the one thing you want the viewer to remember; that's what gets the build-in. Everything else can just be there.

- **Read distance matters.** B-roll is on screen 2–4 seconds. Elements need to read at a glance. When you're unsure about size, scale up. A label that's "definitely readable" in your design tool may be illegible at playback distance. The cost of slightly-too-big is "looks bold"; the cost of slightly-too-small is "viewer doesn't see it." Asymmetric.

- **Motion is the metaphor.** If A becomes B, A should visibly transform into B — translate, scale, fade in concert. Don't show A then show B alongside it. Static juxtapositions blur in memory; transitions stick. (Pills migrating into a SKILL.md body and then the body's instruction lines fading in *as the pills fade out* communicates "the pills are the body" better than rendering the final state directly.)

- **Recurring motifs earn each appearance.** A visual reused across clips in a series must serve a distinct narrative beat each time. If the second appearance can't justify itself ("this is what a skill is" → "here's a skill being born" → "the skill is alive now"), simplify the repeat: a small representative element instead of the full anatomy. Viewers register repetition as "I've seen this already" before they register "this is the callback you intended."

- **Honor platform conventions.** When the metaphor is a real UI (chat thread, file explorer, code editor), match the convention the viewer already knows. Chat: bot left, user right. Continuity markers (`…`) are not styled as bubbles — they're meta UI signaling "the conversation goes on." Inventing a novel arrangement burns ms of comprehension the clip can't afford.

- **For real products, use real assets.** Approximated brand SVGs (a 4-rect "Slack-ish" hashmark, a calendar shape with stripes) read amateur and weaken credibility. If the clip references a specific product, use the real logo from the asset library or fetch one (see "Asset library"). The exception is when the product is being parodied or abstracted on purpose — then commit to the abstraction.

- **Generate curve geometry; don't hand-tune it.** For any chart of an analytical relationship (trend, effort, learning, decay), sample y(x) in JavaScript and emit the SVG path procedurally. Hand-drawn cubic-beziers look lumpy because they ARE lumpy — every control point is an approximation. See `templates/math-curve.html` for the pattern.

- **Namespace classes by their role in this animation, not the concept they represent.** Generic class names (`.user`, `.claude`, `.icon`) collide when the same word appears in two unrelated DOM trees (a Claude logo *element* and a Claude *chat row*). The CSS shorthand silently applies the wrong rules and the bug is invisible in source. Prefer scoped names: `.chat-row.bot`, `.claude-mark`, `.connector-icon`.

- **Layer order: structural elements sit behind focal elements.** In any flow / network / constellation diagram, connecting lines, grids, axes, and background rails belong behind the nodes they anchor. They establish *that* things are related; the nodes are *what's* being related, and viewers parse nodes first. Lines crossing on top of icons reverses the figure/ground — the line draws attention; the icon becomes a backdrop. Use `z-index` explicitly rather than relying on DOM order, since later authoring (adding an element, reordering markup) silently flips the stack and the bug is invisible in source.

- **Proximity signals grouping.** When two elements together form one semantic unit — label + thing, prompt + attachment, icon + filename, before/after pair — they need tight visual proximity so the eye reads them as one. Wide gaps signal independence. The test: if a viewer described what's on screen, would they say "X with Y" or "X and also Y"? You want the first; the spacing has to do that work without a label. This is independent of *where* the group sits in the composition — that's covered by "Compose the group, not the element."

### Defaults

- Viewport: 1920×1080 (`aspect-ratio: 16/9`).
- Default duration: sized to the content — (last build-in beat) + ≥2s hold. There is no fixed default; a one-element fade-in might be 2.5s total while a six-element build might be 5s+.
- Default fps: 30 (60 only if there's fast motion — adds file size with no perceptual gain for fades).
- Background: dark (most YouTube channels keyed with white text need dark B-roll for contrast). Override per brand.

## Icons — default to Heroicons

Heroicons outline is the house style for this skill:

- 24×24 viewBox
- `stroke="currentColor"`, `stroke-width="1.5"`
- `stroke-linecap="round"`, `stroke-linejoin="round"`
- `fill="none"` on outline variants

Source: https://heroicons.com — copy the SVG markup directly. The user can paste the SVG into chat or ask Claude to look one up. Common icons (wrench, screwdriver, sparkles, arrow-right, check, plus, x-mark, light-bulb, document-text, cog-6-tooth, user, users, briefcase) are in `assets/icons/heroicons.md`.

**Don't draw new SVGs from scratch.** If a needed icon isn't a Heroicon, find the closest match. If the user provides their own SVG markup, use it verbatim — don't redraw it.

## Asset library

Assets are bundled with this skill at `assets/` and grow over time. Whenever an animation needs a new logo, icon, or media file, fetch it once, save it under `assets/`, and reuse it forever after.

### Current contents

```
assets/
├── README.md                 ← index — keep this updated as new assets are added
├── logos/
│   ├── claude-color.png      ← Anthropic Claude sparkle (orange, transparent, 640×640)
│   ├── gmail.png             ← Gmail icon, color (500×375)
│   ├── google-calendar.png   ← Google Calendar icon, color (500×500)
│   └── slack.png             ← Slack four-color hashmark (500×500)
└── icons/
    └── heroicons.md          ← quick-reference paths for common Heroicons outline icons
```

When the working `animations/` folder needs a logo or icon, **copy it from `~/.claude/skills/animation-builder/assets/` into the animation's local folder** (e.g. `animations/assets/`) so the rendered HTML can reference a relative path. Don't reference the skill's bundled assets directly from the rendered HTML — keep each animation self-contained so it's portable.

### Fetching new assets

When a needed asset isn't in `assets/` yet:

- **AI/tech brand logos** (Claude, ChatGPT, Gemini, Cursor, Notion, etc.) — use the lobehub CDN:
  ```bash
  curl -sL -A "AnimationBuilder/1.0" \
    "https://unpkg.com/@lobehub/icons-static-png@latest/light/<name>-color.png" \
    -o "<dest>.png"
  ```
  Names follow the pattern `<brand>-color.png` for full-color variants. If the brand has only a monochrome mark, drop the `-color` suffix.
- **Generic brand logos** (Google products, Microsoft, Slack, Notion, etc.) — Wikimedia Commons via WebSearch/WebFetch. Use a descriptive User-Agent including contact info (e.g. `LogoFetcher/1.0 ([email])`). The pattern: find the SVG file on Wikimedia Commons, then construct the thumb URL `https://upload.wikimedia.org/wikipedia/commons/thumb/<x>/<xy>/<File.svg>/500px-<File.svg>.png`. See the keynote skill (`~/.claude/skills/keynote/SKILL.md` § "Fetching assets from the web") for the canonical pattern and gotchas (thumb widths are restricted to specific values like 500/960/1280).
- **Icons not in Heroicons** — try simpleicons.org for brand marks, or ask the user to paste the SVG.

After fetching, **save into `~/.claude/skills/animation-builder/assets/logos/` (or `icons/`) AND update `assets/README.md` with a one-line entry**. This is how the library grows.

Verify the download is a real image: `file <path>` should report `PNG image data` (not `HTML document` — that's an error page).

## Rendering — the script

`scripts/render.py` is the rendering pipeline. It:

1. Opens the HTML in headless Chromium at 1920×1080.
2. Waits for fonts to load.
3. **Pauses all animations** via `document.getAnimations()`.
4. For each frame, sets `currentTime` on every animation, then screenshots.
5. Stitches frames with ffmpeg into a YouTube-ready MP4 (H.264, yuv420p, faststart).

### Critical bug to avoid

When taking the per-frame screenshot, **do NOT pass `animations="disabled"`** to `page.screenshot()`. Playwright's `disabled` option treats animations as not started — it overrides the manual `currentTime` seek and freezes every frame at the initial state. (Symptom: the rendered MP4 shows only state A; the transition never happens.)

The `render.py` script omits this option on purpose. If editing the script, leave the screenshot call free of the `animations` kwarg.

### Setup — one-time, lives in the skill folder

The skill's own folder is the uv project. The Python deps and venv live there, **not** in the user's working folder. No copying scripts into per-project directories.

One-time on a fresh machine:

```bash
cd ~/.claude/skills/animation-builder
uv sync
uv run playwright install chromium    # ~92MB one-time download
```

Use **uv**, not pip.

### Rendering — invoke the central script

From anywhere on the filesystem:

```bash
uv run --project ~/.claude/skills/animation-builder \
  ~/.claude/skills/animation-builder/scripts/render.py /abs/path/to/animation.html
```

Output MP4 lands **next to the input HTML** by default. For the standard video layout (HTML in `assets/src/`, MP4 in `assets/`), pass `--out` to point one folder up:

```bash
uv run --project ~/.claude/skills/animation-builder \
  ~/.claude/skills/animation-builder/scripts/render.py \
  ./assets/src/01-split-screen.html \
  --duration 5 --fps 30 --out ./assets/1-animation-split_screen.mp4
```

If the user uses this skill often, suggest a shell alias:

```bash
alias animrender='uv run --project ~/.claude/skills/animation-builder ~/.claude/skills/animation-builder/scripts/render.py'
# then: animrender ./assets/src/01-split-screen.html --out ./assets/1-animation-split_screen.mp4
```

**Don't copy `render.py` or `pyproject.toml` into the user's working folder.** One canonical environment, invoked centrally. The working folder should only contain the HTML files (and any per-animation assets like a logo PNG referenced via a relative path).

### Render command

```bash
uv run render.py <file>.html
# Optional flags:
uv run render.py <file>.html --duration 5 --fps 60 --out custom.mp4
```

Defaults: `--duration 3.6`, `--fps 30`, output is `<file>.mp4` next to the HTML. Override `--duration` to match the clip — it should equal the time of the last build-in beat plus ≥2 seconds of hold.

### Verifying the output

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,duration,codec_name,pix_fmt \
  -of default=nw=1 <file>.mp4
```

Should report `width=1920 height=1080 r_frame_rate=30/1 codec_name=h264 pix_fmt=yuv420p`.

### Visual validation (when the composition is non-trivial)

`ffprobe` confirms the file is technically right; it can't tell you whether the spacing, proportions, or alignment look correct. For multi-element compositions — split-screens, flow diagrams, anything with parallel/symmetric elements — screenshot the final held frame in a browser and look at it before declaring the asset done. This catches issues the prose brief doesn't surface (optical asymmetry, off-balance gradients, mismatched-by-a-pixel components).

Workflow with Playwright MCP:

1. Serve the HTML over local HTTP — `file://` URLs are blocked in the Playwright MCP environment:
   ```bash
   cd <folder-with-html> && python3 -m http.server 8765 >/dev/null 2>&1 &
   ```
2. `browser_resize` to 1920×1080, then `browser_navigate` to `http://localhost:8765/<file>.html`.
3. `browser_wait_for` with `time` set to (last build-in beat + 0.3s) so the composition settles before the screenshot.
4. `browser_take_screenshot` into `.playwright-mcp/<name>.png` and read it.
5. `browser_close` and kill the server.

Inspect for: unequal spacing between symmetric elements, gradients sitting in dead space rather than behind the subject, build-in order mismatching the VO order, components that should be identical but aren't. Re-render only if something jumps out — don't loop on aesthetic micro-tweaks unless the user asks for them.

For spacing/balance work specifically — arrow symmetry, group alignment, gap equalization — dispatch a subagent to run the measure→adjust→re-measure loop. It can inject JS to read `getBoundingClientRect` for each element, balance the gaps numerically, edit the source CSS, re-screenshot, and iterate. Keeps the iteration screenshots out of the main context and forces a measurement-driven loop instead of pixel-eyeballing (which tends to converge on "looks ok" without ever getting balanced). Pass the agent the file path, the specific selectors to balance, the gaps to equalize, and a max iteration cap (4 is usually enough).

### Alternative: extract a frame from the rendered MP4

When Playwright MCP is unavailable or unreliable (a parallel job is hogging the browser, the tab keeps redirecting, etc.), pull frames straight from the encoded MP4 with ffmpeg:

```bash
ffmpeg -y -ss <t-seconds> -i <clip>.mp4 -frames:v 1 -update 1 <out>.png
```

The MP4 is the canonical source of truth anyway — what's encoded is what the editor will see. Use this for verifying multiple time points (`t=0.5s`, `t=2.0s`, `t=4.5s`) when you suspect a clip is mid-build at the wrong time, or to confirm a re-render actually changed anything.

## Rendering pitfalls (read before debugging a weird MP4)

Three failure modes have actually shipped broken MP4s. If a clip looks wrong, suspect these before suspecting the HTML.

### 1. Parallel renders collide when HTMLs share a parent directory

The renderer writes frames to a directory next to the input HTML. Two parallel invocations of clips that live in the same `src/` end up writing to staging dirs whose names collide, the PNGs overwrite each other, and ffmpeg encodes whichever frames happened to be on disk when it ran. Symptoms: a clip whose first second is clip A and whose final second is clip B; identical content in two MP4s that should differ.

- **Structural fix:** every clip lives in its own subfolder inside `src/` (see "Folder and naming convention"). This is the human-facing rule.
- **Safety net:** the renderer also UUID-suffixes its staging dir on every invocation. Even with the wrong folder layout, two parallel renders won't share a directory.
- **Recovery:** if you find a corrupted MP4, the source HTML is almost certainly fine — just re-render serially.

### 2. CloudStorage paths (Google Drive, iCloud) lag screenshot writes

Filesystem virtualization on `~/Library/CloudStorage/` and `~/Library/Mobile Documents/` doesn't make new files visible to other processes immediately. ffmpeg can start before all the PNG frames have surfaced, encoding a truncated or empty MP4.

- **The renderer auto-detects CloudStorage paths and stages frames in `/tmp/`.** No action needed if you're running it from the canonical location.
- **If a render fails with "ffmpeg encountered 0 frames" or produces a 0-second MP4** on a non-CloudStorage path, you may be hitting a different filesystem quirk — try staging in `/tmp/` manually.

### 3. CSS animation shorthand silently resets longhands

This bug looks like correct CSS that doesn't work:

```css
.row.bot  { animation: slide-in-l 0.55s ease-out forwards; }
.r2 { animation-delay: 0.5s; }   /* ← does nothing! */
```

The `animation:` shorthand sets `animation-delay: 0` implicitly. `.row.bot` has higher specificity (2 classes) than `.r2` (1 class), so `.row.bot`'s reset wins. All rows that match `.row.bot` get delay 0 — every bot bubble fades in at t=0 simultaneously.

- **Diagnosis:** Compare what you wrote (sequenced delays) with what plays back (everything at once). If they disagree, this bug is the first suspect.
- **Fix:** bump the override selector's specificity to match: `.row.r2 { animation-delay: 0.5s }`. Same number of class selectors, so later rule wins.
- **Prevent:** when writing animation shorthands, set delay explicitly in the same rule (`animation: name 0.5s 0.3s ease-out forwards`), OR use longhand `animation-delay` everywhere, OR override delay only from rules with equal-or-greater specificity.

## When the animation has many states / labels building in

For sequences like "four boxes appear left-to-right" or "three labels fade in then animate into a file diagram," author one animation per element with staggered `animation-delay`, all sharing the same total duration. Don't try to script complex sequences with JavaScript timelines — CSS keyframes + delays cover the common cases and are dead simple to seek deterministically with the render pipeline.

Example pattern (four-element build-in, last element settles at ~0.8s, total 3.0s = 2.2s hold):

```css
.box-1 { animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; animation-delay: 0.0s; }
.box-2 { animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; animation-delay: 0.2s; }
.box-3 { animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; animation-delay: 0.4s; }
.box-4 { animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; animation-delay: 0.6s; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

Two important details:

- Each element's `animation-duration` is its own build-in time (0.8s here), **not** the total clip length. The clip's total length comes from the `--duration` flag passed to the renderer.
- `animation-fill-mode: forwards` (via the `forwards` keyword on the shorthand) holds the `to` state forever after the animation completes. Without it, the box snaps back to `from` and the final frame is empty.

## Output expectations

After rendering, tell the user:

- Where the MP4 lives (relative path from their cwd).
- Duration, fps, resolution.
- One short sentence on what was animated.
- (Optional) Whether the next animation in their script is the obvious next thing to build.

Keep it terse. The user will preview the MP4 themselves.

If the MP4 is overwriting a path already referenced by an FCPXML the editor opened earlier, mention that Final Cut will keep showing the cached old render. The reliable fix (tested) is to drag the updated MP4 into the timeline again, replacing the existing instance — menu-based cache flushes (Delete Generated → Render Files, close+reopen) did not refresh it in practice. The disk file is correct; FCP just won't pick it up without the re-drag.

## Reference files

- `templates/starter.html` — copy this to start a new animation.
- `templates/card.html` — copy this to start a new section/chapter card (static, no keyframes).
- `templates/chat-thread.html` — scaffold for any "Claude in a back-and-forth with the user" scene. User on right, bot on left, with sub-styles for thinking dots, tool-call chips, draft docs, and edit annotations.
- `templates/file-mock.html` — scaffold for an IDE-style file window (SKILL.md, README, settings). Title bar with traffic-light dots, cerulean-keyed frontmatter, neutral instruction skeleton.
- `templates/math-curve.html` — scaffold for any chart of an analytical relationship. Generates the SVG path procedurally from a JS function (Gaussian + tanh by default); easy to swap in any y(x).
- `scripts/render.py` — the render pipeline. Don't reinvent.
- `references/techniques.md` — patterns for common animation types (morph, build-in, draw-on, side-by-side).
- `assets/README.md` — running index of bundled logos/icons.
- `assets/icons/heroicons.md` — quick-reference Heroicon paths.
