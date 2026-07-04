# Mode: social-infographic

A single PNG sized for a social feed (LinkedIn by default). It's a standalone still — nothing around it frames it, and it has ~2 seconds in a scroll to land one idea. So it carries its own title, body, optional takeaway, and a quiet footer signature.

Read this *with* the shared engine in `SKILL.md`; this file covers only what's specific to social stills.

## What this mode is for

- Single PNG, sized for the feed (landscape, portrait, or square).
- One visual idea per graphic. Two-panel comparisons, vertical lists, single-centerpiece concept stills.
- Not a website mockup, not a slide deck, not a B-roll clip.

**Recognized exception — composite cheatsheets.** A tall portrait (~1080×~2000) that bundles 3–6 standalone topics into one educational summary (e.g. `claude-skill-cheatsheet`). Each section is a labeled card group with its own self-contained visual idea — the *composite* doesn't violate "one idea per graphic," it stacks several. Use when the brief explicitly asks for a "cheatsheet," "guide," or "everything-you-need" piece that summarizes content already proven as individual graphics. Reuse the markup from those individual graphics (don't re-author from scratch).

## Workflow additions (social-specific)

- **Write the scene sentence** before opening the template: who's scrolling the feed, what they should understand in 2 seconds, what feeling it should leave. "A graphic comparing X and Y" is not a scene. "A founder scrolling at lunch realizes that 'connectors' and 'skills' aren't synonyms — one gives Claude access, the other gives it competence — and remembers it because the right side has a directory tree she's seen on her own machine" is.
- **Pick aspect ratio.** Default landscape (1080×820). Portrait (1080×1350) for vertical lists or stacks. Square (1080×1080) for single centerpieces with symmetric margin. Don't reflexively pick square — landscape and portrait read fine in-feed.

## Project folder convention

**Every infographic gets its own folder. Create it first, before writing any HTML.** No loose HTMLs or PNGs in shared directories.

- **Folder name:** kebab-case slug matching the topic — `connectors-vs-skills/`, not `infographic-2026-05/`.
- **Folder location:** `~/Documents/_stv/_content/_SFC/linkedin/<year>/<category>/<slug>/`. `<category>` is typically `AI-education`, `misc`, or a similar topical group. If the category isn't obvious from the brief, ask.
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

## Treat it as a still, not a website

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
- CTA buttons (a still isn't clickable)
- Background glows beyond one very faint one if any
- Hover/transition styles (the graphic is a still)

**Card-per-step is the canonical exception** to "no decorative card grids." When the visual idea is "N discrete steps you do in order," giving each step its own card (`rounded-2xl` or similar, low-opacity hairline border, light surface on the off-white bg) sharpens the beat structure and makes the step eyebrows + labels bottom-align cleanly. Still keep each card to graphic + step eyebrow + one-line label — the card adds structure, not extra elements. Live example: `four-step-framework`.

**When a brand-system skill is loaded, this rule gets *harder*, not softer.** ABA's canonical hero is eyebrow + 2-line H1 + 1-sentence subhead + CTA. Do not transfer that pattern to the still. A social still gets a title and the body content; on a single-title composition, eyebrows and subtitles are dead weight that push the actual payload below the fold and make the graphic read as a website screenshot instead of a still. If you find yourself writing both a subtitle and a brand-system eyebrow on the top-level title, the subtitle is the one to delete, and probably the eyebrow too.

**Exception — eyebrows as parallel-card labels.** When two or more cards are being explicitly compared (`TYPE 1` / `TYPE 2`, `BEFORE` / `AFTER`, `FREE` / `PAID`), short mono eyebrows above the card heading work as discriminators — they carry structural meaning, not decoration. Used in `two-types-of-skills`. Still keep them tight: one or two words, mono, ~14px, uppercase.

**Exception — eyebrow as below-title metadata.** When the title carries the entire hook and you still want a small structural label (e.g. `4-STEP FRAMEWORK`), it can sit *below* the h1 in mono accent. Reads as a quiet caption rather than a website pre-roll. Used in `four-step-framework`. Keep it short and tight: one phrase, mono, ~16px, uppercase.

## Footer

- **Default:** `@shawhintalebi` in JetBrains Mono, ~14px, ~60% opacity, bottom-center. Quiet signature, not a brand stamp. Brand-system skills may override the handle (e.g. `aba-brand-system/references/infographic-composition.md` specifies `aibuilder.academy` for ABA-branded stills — same treatment, brand URL in place of personal handle).
- **Footer placement on variable-height canvases.** When the canvas is taller than its content (composite cheatsheets, in-progress drafts), the footer floats up just below the last section with dead space below — reads as broken. Anchor it to the lower third: `html, body { min-height: 100vh }`, `.canvas { min-height: 100vh; display: flex; flex-direction: column }`, `.footer { margin-top: auto }`, plus a small canvas `padding-bottom` (~28px). Footer sticks to the bottom regardless of content length, so mid-iteration renders stay readable and final renders look intentional. Pair with the iterative-height workflow under Rendering in `SKILL.md`. For a final render whose height is measured, a footer in normal flow (plain `margin-top` + bottom padding) removes bottom dead space directly; reserve the `margin-top: auto` trick for drafts whose height is still in flux.

## Examples

See `references/examples.md` § "Social infographic" — `connectors-vs-skills` (canonical landscape two-panel), `two-types-of-skills`, `four-step-framework`, `6-ways-claude-context` (portrait list), `non-coding-skills` (portrait card list), `claude-skill-cheatsheet` (composite).
