# Graphics that have shipped

Both are HTML rendered with `scripts/render_png.py` (Playwright, 2×). Dark neutral page
`#1b1f23`, Inter from Google Fonts, cards with 14–16px radius. The avatar is referenced as
`../assets/avatar.png`, so copy the HTML into a sibling of `assets/` (or rewrite the path) before
rendering.

| File | What it is | Size | Shaw's revisions, in order |
|---|---|---|---|
| `dm-collage.html` | 3×2 grid of LinkedIn DM cards, recipient names redacted | 2000×1040 | keep his own name/pronouns/time; real photo, not a blank circle |
| `followers-cards.html` | YouTube / Medium / LinkedIn profile cards with counts | 2000×720 | real photo; drop the subtitle; title 3× bigger |

A repeat is a data swap: copy the file, edit the text, render. Start from the final state the table
describes — those revisions were asked for and shouldn't need asking again.

## Conventions baked into both

- Cards styled after the platform (YouTube dark with pill Subscribe; Medium white with green
  Follow; LinkedIn white with banner, overlapping avatar, blue Follow) — but the platform name is a
  small uppercase text label, never a logo.
- Recipient names → `<span class="redact">Name</span>` (gray block). Shaw's header line stays
  exactly as the platform renders it.
- Cards are ordered chronologically; a long message clips in a fixed grid, so drop the height
  constraint or add a row rather than shrinking type.
- Anything on a card that didn't come from a real screenshot (a LinkedIn headline, location,
  "500+ connections") is a guess — name it in the wrap-up.

## Fallbacks

- Playwright's Chromium missing: `python -m playwright install chromium`.
- A real Wayback capture sometimes beats a mockup because it carries the date bar. Take it with
  `computer screenshot save_to_disk`, then crop the donation banner off the top with PIL
  (`im.crop((0,176,w,520))` at a 1568-wide viewport; the bar with the capture date sits at
  y≈180–230).
