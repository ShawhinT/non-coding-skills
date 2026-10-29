# Mode: carousel

A multi-page PDF sized for a LinkedIn document post: a cover, a run of cards the reader swipes, and a close. Each page is its own composition, but they're read as a sequence — which is the whole difference from a still. A misalignment invisible on one card becomes a twitch on every swipe.

Read this *with* the shared engine in `SKILL.md`; this file covers only what's specific to carousels.

## What this mode is for

- One PDF, many pages, uploaded as a LinkedIn document post.
- 1080×1350 (4:5) by default — the tallest ratio the feed gives a document.
- A list, a glossary, a sequence of steps: content with a natural unit that repeats.
- Not a deck (that's `keynote`), not a single still (that's `social-graphic`).

## Author it as one HTML, not N files

Every page is a `<section>` at the page size inside a single HTML file. One stylesheet, one set of tokens, one place to change a shared element. Rendering the whole file to PDF is then one command.

```css
.page { position: relative; width: 1080px; height: 1350px; overflow: hidden; }
@media screen { .page { margin: 0 auto 26px; } }   /* stack for eyeballing in a browser */
@media print {
  @page { size: 11.25in 14.0625in; margin: 0; }    /* 1080×1350 at 96dpi — inches, not px */
  .page { margin: 0; page-break-after: always; break-after: page; }
  .page:last-child { page-break-after: auto; break-after: auto; }
}
```

**Separate the content from the renderer.** A carousel is the same card N times with different words, so put the copy in a list at the top of a small `build.py` and let one function per page-type emit the HTML. Changing a definition then means editing one line, not hunting through 17 near-identical blocks. This also makes design exploration nearly free: a second renderer over the same content data gives a full alternate deck to compare.

## Rendering

`scripts/render.sh` screenshots a single page to PNG and does not cover this. Print instead:

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
  --virtual-time-budget=15000 \
  --print-to-pdf="$PWD/<slug>.pdf" "file://$PWD/<slug>.html"
```

- **`--virtual-time-budget` is not optional.** Without it Chrome prints before webfonts arrive and silently falls back to Helvetica — the output looks plausible, just not in the brand's typefaces. Load fonts with `<link …&display=block>` rather than an `@import` inside `<style>`, which loses the race more often.
- **Verify the page count** (`mdls -name kMDItemNumberOfPages -raw <file>.pdf`). A stray text node between sections can print a blank page.
- **Inline any logo as SVG** (read the path out of `assets/logos/` at build time) so the PDF carries no external file reference.

## Comparing designs

When the direction isn't settled, render each candidate as a **sample deck** — cover, four or five cards chosen to break the layout, close — rather than a full deck. Pick the samples for stress, not for order: the shortest term, the longest name, the longest body copy, the one with an extra line. Then build one contact sheet that scales every candidate's pages down in columns (`transform: scale(0.3)` with a compensating negative margin) so they can be judged side by side in a single image.

## Project folder convention

Same as `social-graphic` — `…/linkedin/<year>/<category>/<slug>/` — with the deck at the top level and exploration kept out of the way:

```
<slug>/
  build.py                ← content data + one renderer per design
  render.sh               ← rebuild + print
  <slug>.html
  <slug>.pdf              ← the deliverable
  assets/                 ← project-local copies of any logos inlined
  explorations/           ← sample decks + the contact sheet, once a direction is picked
```
