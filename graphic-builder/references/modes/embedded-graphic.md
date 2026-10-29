# Mode: embedded-graphic

A figure that lives *inside* surrounding context — a blog post, a slide, a doc. The prose, slide, or caption around it already supplies the title and the explanation, so the graphic is **just the diagram**. This is the opposite of a social still, which has to frame itself.

Read this *with* the shared engine in `SKILL.md`; this file covers only what's specific to embedded figures.

## Packaging — strip the social chrome

By default an embedded figure has **none** of the social-still packaging:

- **No editorial title + subtitle hero stack.** The blog heading or slide title already says what this is.
- **No bottom takeaway line.** The surrounding paragraph makes the point in prose.
- **No footer signature** (`@shawhintalebi` / `aibuilder.academy`). It's a figure in someone's content, not a standalone post.

What stays is the diagram itself plus the small in-diagram labels that make it readable (section captions like `WHAT CLAUDE CAN SEE`, per-row labels, mono discriminators). Those are part of the figure, not chrome — keep them.

**Re-adding a title is the author's explicit call, not a default.** If the user asks for a title (Shaw did on the prompt-injection pipeline), add one — and a single dominant display title may be Title Case and centered if the composition is symmetric. But don't reach for the title/subtitle/takeaway stack reflexively; that's the social-still reflex and it makes an embedded figure read like a screenshot of a landing page.

**Optional footer.** None by default. If the figure is brand-anchored and may also be shared standalone, a single quiet brand footer (`aibuilder.academy`, same treatment as the social mode) is allowed — but it's opt-in, confirm rather than assume.

## Canvas sizing — content-fit, not a fixed aspect

Social stills use fixed feed presets. Embedded figures are sized tight to their content so they drop cleanly into a column or slide with no dead bands.

- **Width:** `1080px` (a comfortable inline width; renders crisp at 2x). Wider only if the host layout calls for it.
- **Height:** **not fixed.** Do NOT put `min-height: 100vh` on `html/body` or the canvas — that reintroduces the dead-space-and-floating-footer problem. Let content drive the height.
- **Padding:** tight vertical padding so the figure doesn't carry a social still's generous margins. The session figures used roughly `56–60px` top, `60–64px` sides, `30–36px` bottom.
- **Render then trim.** Render at a generous height (`--size 1080x4000` or similar), PIL-measure the content end, then re-render at `content-end + ~36px`. This is the shared iterative-height workflow in `SKILL.md` § Rendering — use it; embedded figures depend on it because there's no preset to fall back to. Observed final heights this session were short: ~430–560px tall.

## Project folder convention

Same `<slug>/<slug>.html` + `<slug>.png` + optional `assets/` layout as the social mode, but the folder **lives with its project (the blog post's or deck's folder), not in the SFC content tree.**

- Put it alongside the content it illustrates — e.g. a blog post's working directory: `~/Documents/_stv/_content/_LFC/medium/<post-slug>/<figure-slug>/`.
- Relative `assets/` paths keep the folder portable so it can be zipped and handed off with the post.
- If the destination directory isn't obvious from the brief, ask where the figure should live.

## Slide figures (knobs, not yet a separate mode)

Slides are embedded figures with a few projection-specific dials. Until enough slide work accrues to justify its own mode, handle them here:

- **Aspect:** 16:9 region, e.g. `--size 1920x1080`, or a content-fit width that matches the slide's content box.
- **Background:** transparent or the slide's bg so the figure sits seamlessly on the slide (set the canvas bg to `transparent` and render; or match the deck's surface color). Avoid the off-white `#FAFAF7` if the slide isn't off-white.
- **Type scale:** larger than blog scale — projected figures are viewed from across a room.

When real slide figures pile up, promote this into `references/modes/slide-figure.md`.

## Examples

See `references/examples.md` § "Embedded graphic":
- **`prompt-injection-pipeline`** — left-to-right flow diagram (data source → Claude → actions) with labeled connector arrows and a highlighted contained-action card. The canonical embedded-mode example.
- **`roles-and-groups`** — two-zone comparison (Roles | Groups) with permission cards and chip rows.
