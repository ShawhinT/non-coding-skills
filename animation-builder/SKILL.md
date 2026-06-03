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
2. **Find the transcript and pace beats to the voice-over (mandatory when one exists).** Before settling on durations or delays, look for a word-level transcript in or near the working folder — typical names include `*_transcript.json`, `transcript.json`, `*.srt`, `*.vtt`. If one exists, use it. Don't invent pacing by gut feel when the actual timing data is sitting in the project; the clip will sit on a real spine and the editor will not adjust delays clip by clip to recover what should have been baked in. See "Pacing beats to the transcript" below for the lookup pattern.
3. **Write the scene sentence.** Before opening the template, write one sentence stating: what the voice-over is saying when this clip is on screen, what idea the clip must reinforce, and what feeling it should leave. "An icon morphs" is not a scene. "Under the line *'…and that's when the wrench becomes a screwdriver'*, a wrench rotates and resolves into a screwdriver — quick, confident, no theatrics" is. If the sentence doesn't force the timing and the motion, add detail until it does.
3. **Check for brand context.** If the animation belongs to a specific brand (e.g. AI Builder Academy), invoke the matching brand-system skill (e.g. `aba-brand-system`) and pull its colors/type/voice plus the brand's *animation-motion* reference (e.g. `aba-brand-system/references/animation-motion.md`) — never the brand's web composition. Otherwise default to a tinted-neutral dark palette (see "Color hygiene") and system-ui fonts.
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

## Pacing beats to the transcript

Talking-head B-roll lives on a spine the editor has already cut. If the project has a word-level transcript, the only correct pacing strategy is: **anchor the clip at one VO moment, then express every animation delay as `wordTime − anchorTime`**. Hand-tuned delays that "feel about right" land beats half a second early or late and force the editor to nudge the clip in FCP — they will not do that for every beat, and the asset reads as off.

### How to find and read the transcript

- Look in the working folder, its siblings (`../`, `../../`), and any nearby `edits/` or `transcripts/` folders for `*_transcript.json`, `transcript.json`, `*.srt`, or `*.vtt`. If a `BRIEF.md` or project README mentions where the transcript lives, trust it.
- JSON transcripts in this house style are `{"words": [{"word": "...", "start": 0.123, "end": 0.456}, ...]}`. The lookup pattern (read-only — never modify the transcript):
  ```bash
  python3 -c "
  import json
  words = json.load(open('PATH/TO/transcript.json'))['words']
  # Find all occurrences of target keywords with surrounding context
  targets = {'sales', 'pipeline', 'customer'}
  for i, w in enumerate(words):
      wt = (w.get('word') or '').strip().lower().strip('.,!?;:')
      if wt in targets:
          ctx = ' '.join((words[j].get('word') or '') for j in range(max(0,i-5), min(len(words),i+6)))
          print(f\"{w['start']:7.2f}s  [{wt}]  ...{ctx}...\")"
  ```
- For SRT/VTT, fall back to cue start times — coarser than word-level but still better than gut-feel pacing.

### How to convert word times into clip delays

1. Pick the **anchor word** — the first word the clip should react to (often the first noun or verb in the VO sentence).
2. For each subsequent beat, compute `delay = wordStart − anchorStart`.
3. Communicate the anchor to the user in your final report: "Place this clip on the spine at **{anchorTime}s** so beats land on the words."
4. Set the clip's `--duration` to `(last beat delay) + 0.6s settle + ≥0.9s hold` so the editor has slack.

### Before you write any delay — the visual-naming checklist

Wrong delays don't come from misreading the transcript. They come from **picking the wrong word to align to**, and that mistake is easy to skip past because "230.39s" and "230.95s" both look like reasonable answers. Run this checklist for every clip *before* you start typing `animation-delay`:

1. **List the visual beats in plain language, in order.** Not "card 1 appears" — write what's *on* card 1. ("A pill labeled PRE-CALL with a draft email preview." "A schedule chip saying 'Every morning at 7:00 AM'.")
2. **For each beat, name the word the VO uses for the thing on screen.** This is the word the beat must land on. If the chip says "every morning," the word is `morning` — not `running`, not `daily`, not the verb that introduces the phrase.
3. **The anchor word is whatever the *first* beat names.** Don't anchor at the start of Shaw's sentence by reflex. Anchor at the moment the first visual subject is named — anything earlier becomes pre-roll dead air, and 1.75s of dead air before the editor's cut-in is a noticeable hole.
4. **Look up each named word in the transcript JSON.** Convert to relative delays. Now write the CSS.

**Common slip:** aligning a beat to the *verb that introduces* the noun rather than the *noun itself*. VO says "automatically draft pre-call emails" — the visual is a PRE-CALL card; the word the beat must land on is `pre-call` (the category), not `draft` (the verb), not `automatically` (the adverb). The verb is the editor's cue; the noun is the viewer's cue. Land on the viewer's cue.

**Self-test before rendering:** read the VO line out loud while looking at your delays. If at any point you say a word that names something on screen but no beat fires, the alignment is wrong — go back to step 2.

### When there is no transcript

Ask the user for word-level timings for the key beats, or transcribe the segment yourself with a quick `whisper`/`ffmpeg` pipeline if audio is available. Don't proceed with invented pacing and hope the editor fixes it.

## Section cards (chapter slates) — minimal by default

Section cards (full-bleed chapter slates marked `[CARD]` in a script, file type `card` in the naming convention) are a different deliverable than concept animations. They're on screen for 1–2 seconds while the voice-over names the next section. Viewers don't read them — they pattern-match.

Strip to three elements max:

1. **Eyebrow** (e.g. `STEP 0`, `PART 01`, `THE MINDSET`) — small, accent-colored, generously tracked.
2. **Title** — large, the section name, Title Case.
3. **(Optional) thin progress rail** at the bottom — only if the card is part of a numbered series of three or more.

Don't add: logos, frame marks ("Chapter 01 / 05" in the corner), pagination, signatures, body copy, supporting glyphs, decorative dividers. If a brand-system skill (`aba-brand-system`, etc.) is loaded, use its color and type tokens, but **don't import its hero composition** — landing-page chrome doesn't translate to a 1-second slate.

Author cards from `templates/card.html` (static — no keyframes), not `templates/starter.html` (which has animation scaffolding).

## Transparent overlays (alpha rendering)

A third artifact type, distinct from full-frame animations and full-frame cards: **transparent overlays that composite over live talking-head footage** rather than replacing it. Lower-third captions, karaoke-style intro emphasis, name plates, callout arrows that point at the speaker — anywhere the live shot's energy should remain visible while text or a graphic is layered on top.

Reach for the overlay form when the goal is to *augment* the live frame, not to *cut away from* it. If the editor would rather cut to a full-frame card, build a card; if they'd rather keep the speaker on screen with something layered, build an overlay.

### Render with `--alpha`

`scripts/render.py --alpha` switches the pipeline to a transparency-preserving path:

- Playwright screenshots use `omit_background=True`.
- ffmpeg encodes ProRes 4444 (`yuva444p10le`) into a `.mov` instead of h264 yuv420p `.mp4`.
- The output's alpha channel is preserved end-to-end; FCP imports it directly and composites it over the spine without keying or masking.

Output extension is `.mov`, not `.mp4`, when `--alpha` is on. Final Cut, DaVinci Resolve, and Premiere all import ProRes 4444 `.mov` natively.

### Place content where it doesn't fight the subject

The talking-head shot fills the frame; overlay content must claim space the subject doesn't. For a centered head-and-shoulders shot, the safe zone is the lower third (roughly y > 800 of 1080, depending on framing). Don't center an overlay where the speaker's face lives — viewers will read the overlay as obscuring the speaker rather than annotating them. If unsure, pull one frame from the talking-head footage with ffmpeg and design against that as the reference background.

### Legibility comes from the element, not from a slab

Backgrounds defeat the point of going transparent. Use a strong text-shadow on the overlay text — typically a combined soft glow + hard offset — so the text reads against any frame content the editor might cut to:

```css
text-shadow:
  0 0 24px rgba(0, 0, 0, 0.55),
  0 4px 12px rgba(0, 0, 0, 0.45);
```

White text with this shadow reads cleanly against both bright walls and dark clothing without imposing a card-like backdrop.

### Accent color for karaoke captions

When a text-only karaoke caption emphasizes a word (an `.accent` span over the talking-head shot), **do not use the brand's primary accent at full strength**. Deep, saturated brand primaries are tuned for ink on white surfaces — they read as muddy or muted when composited against varied talking-head footage (warm lamplight, dark clothing, mid-tone walls).

The rule: overlay accents need to punch against the live frame at both extremes of brightness. Test against light *and* dark frames before committing. A lighter, brighter mid-tone version of the brand's accent generally wins — saturated cyan-blues, bright mid-tone reds, and high-luminance greens hold up; deep brand primaries (deep blues, deep reds) do not.

This rule applies only to **font-only karaoke overlays** — captions with no pill, no card, no chip backing. Where the accent text sits on its own white pill or card surface (e.g. lower-third name plates with a white background), keep the brand primary — the surface contrast does the legibility work and the brand color is what's actually appropriate against white. The test: is the talking-head footage itself the backdrop behind this word? If yes, use the overlay-tuned accent. If a white surface is between the text and the footage, use the brand primary.

If a brand-system skill is loaded, it should specify the overlay-accent value for that brand. ABA's overlay-accent (`#5DC3E8`) is defined in `aba-brand-system/references/animation-motion.md`.

### File naming

Use the `overlay` type slot in the naming convention (see "Folder and naming convention"). Example: `0-overlay-intro_captions.mov`. The numeric prefix still represents playback order; the `.mov` extension tells the editor "this one has alpha."

Author from `templates/caption-overlay.html`. See the karaoke / word-by-word pattern in `references/techniques.md` for the per-word reveal mechanism.

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
- **Generic brand logos** (Google products, Microsoft, Slack, Notion, etc.) — Wikimedia Commons via WebSearch/WebFetch. Use a descriptive User-Agent including contact info (e.g. `LogoFetcher/1.0 (you@example.com)`). The pattern: find the SVG file on Wikimedia Commons, then construct the thumb URL `https://upload.wikimedia.org/wikipedia/commons/thumb/<x>/<xy>/<File.svg>/500px-<File.svg>.png`. See the keynote skill (`~/.claude/skills/keynote/SKILL.md` § "Fetching assets from the web") for the canonical pattern and gotchas (thumb widths are restricted to specific values like 500/960/1280).
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
uv run render.py <file>.html --alpha --out overlay.mov   # transparent ProRes 4444
```

Defaults: `--duration 3.6`, `--fps 30`, output is `<file>.mp4` next to the HTML. Override `--duration` to match the clip — it should equal the time of the last build-in beat plus ≥2 seconds of hold.

Pass `--alpha` when the clip is an overlay that will composite over live footage (see "Transparent overlays" above). Output extension becomes `.mov` (ProRes 4444 with alpha channel). The HTML's `body` must be transparent — see "Rendering pitfalls" for the gotcha if it isn't.

### Verifying the output

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,duration,codec_name,pix_fmt \
  -of default=nw=1 <file>.mp4
```

Should report `width=1920 height=1080 r_frame_rate=30/1 codec_name=h264 pix_fmt=yuv420p`.

### Visual validation (when the composition is non-trivial)

`ffprobe` confirms the file is technically right; it can't tell you whether the spacing, proportions, or alignment look correct. For multi-element compositions — split-screens, flow diagrams, anything with parallel/symmetric elements — screenshot the final held frame in a browser and look at it before declaring the asset done. This catches issues the prose brief doesn't surface (optical asymmetry, off-balance gradients, mismatched-by-a-pixel components).

**Before any Playwright MCP tool call, invoke the `playwright-mcp-guidance` skill.** This applies whether the call is direct or made by a dispatched subagent — in the subagent's prompt, include "first invoke the `playwright-mcp-guidance` skill" as an explicit step.

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

### 4. Animating `background: color-mix(..., transparent)` leaks thin colored stripes at row edges

A row whose `background` is animated via keyframes that interpolate between `transparent` and a semi-transparent `color-mix()` value (e.g. `color-mix(in srgb, var(--accent) 12%, transparent)`) renders **thin colored horizontal lines at the row's top/bottom edges before the highlight is supposed to appear**. The bug shows up even with explicit `0%, 40% { background: transparent }` holds — the interpolated value at the edge pixels resolves to a faint tint of the destination color.

- **Cause:** Chromium's compositor pre-rasterizes the animation's final paint into a layer to enable cheap interpolation. `transparent` and `color-mix(..., transparent)` are both `rgba(?,?,?,0)`, but Chromium picks the destination's non-zero RGB channels to interpolate from. At sub-pixel boundaries (top/bottom row edges), antialiasing samples the partially-blended layer and you see a 1–2px stripe of the destination color even at frames where the animation's effective alpha should be zero.
- **Fix:** Don't animate the `background` property when the endpoint uses `color-mix(..., transparent)`. Instead, paint the highlight on a `::before` pseudo-element with the final color pre-set and animate `opacity` from 0 to 1:
  ```css
  .row.highlight { position: relative; }
  .row.highlight::before {
    content: ''; position: absolute; inset: 0;
    border-radius: 8px;
    background: color-mix(in srgb, var(--accent) 12%, transparent);
    opacity: 0; pointer-events: none;
  }
  .row.highlight::before { animation: fade-hl 0.6s ease-out 2.4s forwards; }
  .row.highlight > * { position: relative; z-index: 1; }
  @keyframes fade-hl { from { opacity: 0 } to { opacity: 1 } }
  ```
  Opacity interpolation is a single scalar — no per-channel sub-pixel artifacts. The trick generalizes to any "tinted highlight fades in" pattern.
- **Prevent:** anytime you reach for `background: ... color-mix(..., transparent)` in a keyframe, stop and reach for the pseudo-element + opacity pattern instead.

### 5. Imported stylesheets bleed an opaque background into alpha renders

`--alpha` produces a `.mov` whose viewport area still composites as a solid color (often near-white or near-black) over any non-white background in the editor — even though Playwright's `omit_background=True` is set and ffmpeg's `yuva444p10le` pixel format is correct.

- **Cause:** a parent stylesheet (a brand palette, a CSS reset, a design-system import) sets `html, body { background: <color>; }`. `omit_background: true` only suppresses Chromium's default white backdrop; it cannot un-paint pixels the page itself painted. The "transparent" `.mov` is actually opaque off-white because the body was painted off-white before the screenshot.
- **Diagnosis:** open one frame of the `.mov` over a saturated solid color (red or green) — `ffmpeg -y -f lavfi -i "color=c=0xff0000:s=1920x1080" -i out.mov -filter_complex "[1:v]overlay=shortest=1" -frames:v 1 check.png`. If the red doesn't show through anywhere the overlay isn't painting, the bg is opaque.
- **Fix:** in the overlay HTML's own `<style>` block (after any `<link>` to an external stylesheet), set:
  ```css
  html, body { background: transparent !important; }
  ```
  `!important` so it beats the imported rule regardless of source order or specificity. Re-render and re-verify against red.
- **Prevent:** when authoring overlays from a template that imports a brand palette, always include the transparent-bg override even if the template's own styles look harmless — palettes change, and the next palette edit may silently re-introduce the bug.

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
- `templates/caption-overlay.html` — scaffold for transparent lower-third caption overlays (karaoke / word-by-word reveal). Render with `--alpha`; output is ProRes 4444 `.mov` with alpha.
- `scripts/render.py` — the render pipeline. Don't reinvent.
- `references/techniques.md` — patterns for common animation types (morph, build-in, draw-on, side-by-side).
- `assets/README.md` — running index of bundled logos/icons.
- `assets/icons/heroicons.md` — quick-reference Heroicon paths.
