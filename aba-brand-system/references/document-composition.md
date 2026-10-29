# Document Composition

Load this when building a printable document (a one-pager, reference sheet, or handout rendered to PDF) that a partner or client will read. The universal tokens in `SKILL.md` still apply. This file covers what a document needs on top of them, and above all what it should leave out.

## Default to less

A first draft of a document reliably carries too much: an intro paragraph explaining the page, a logo, a CTA, sub-sections, number ranges on section labels, a "prepared for" line, caveats. Each one feels helpful; together they bury the content the reader came for. Start from a title and the content itself, and add an element only when the reader couldn't use the page without it.

- **The reader already has the context.** A partner or client receiving the doc knows who it's from and why. An intro restating that is padding.
- **Caveats and framing go to Shaw in chat, not onto the page.** If something needs saying (e.g. "these are adapted from other industries"), tell him and let him decide whether it belongs.
- **Brand through type and color, not chrome.** No logo, no CTA, no signature. The footer is `aibuilder.academy` in small muted JetBrains Mono and nothing else.
- **Fewer, flatter sections.** The coarsest grouping the reader needs, with short labels ("For operators") and no number ranges or sub-headers.
- **When exploring design options, include the minimal one.** The quietest variant is usually the one that ships.

The 10/24/26 restaurant use-case one-pager went through four rounds of removal (intro paragraph, CTA footer, logo, sub-sections, number ranges) and gained nothing. Its final form is `examples/restaurant-use-cases.html`.

## Title case for the document title

The document's main title is Title Case ("AI Use Cases for Restaurants"), an exception to the sentence-case rule in `SKILL.md`. Section labels and item names stay sentence case.

## Layout that shipped

Editorial index: one column, each item a row of mono number, Manrope 800 name, and body description in a wide right column, with hairline rules between rows. Section labels in Cerulean uppercase JetBrains Mono. No cards, fills, or dark bands. See the example file for exact values.

## Rendering

- Light page `#FAFAF7`, ink as `rgba(1,4,19,X)` (light-bg palette in `infographic-composition.md`).
- `@page { size: Letter; margin: 0 }` with a fixed `8.5in × 11in` body; footer pinned with `margin-top: auto` in a flex column.
- Render with headless Chrome, then rasterize to check:
  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer --virtual-time-budget=5000 --print-to-pdf="out.pdf" page.html
  pdftoppm -png -r 90 out.pdf preview   # preview-2.png existing means it spilled
  ```
  Count pages from the rasterized files, not `mdls`: Spotlight's page count lags a rewritten file.
- If the wide logo is ever used, its PNG has a white background: set `mix-blend-mode: multiply`.
