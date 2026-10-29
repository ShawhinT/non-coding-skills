# Intro name title — "Hey everyone, I'm Shaw"

Every video on the channel opens with a lower-third name title over the line where Shaw introduces himself. It is a standing asset, not something to rebuild per video.

## The asset

- **Canonical render:** `~/Documents/_stv/_content/_LFC/YT_assets/shaw_talebi_title3.mov` — 1920×1080, ProRes 4444 with alpha, 60 fps, 5 s. Earlier generations (`shaw_talebi_title.mp4`, `shaw_talebi_title2.mp4`) sit beside it and carry the pre-ABA look; don't reach for them.
- **Source:** `assets/intro-title/shaw_talebi_title3.html` in this skill (same file is next to the render in `YT_assets`). It's an `animation-builder` page: two stacked `#010413` plates, "Shaw Talebi" in Manrope 800 at 62 px over "AI Builder, Bread Enthusiast" in Manrope 500 at 30 px, 10 px horizontal padding so the text sits flush to the plate edge, left edge at x = 104, slide-up in and slide-down out. Chosen on 2026-10-08 from nine candidates (design E); the alternates live in `~/Downloads/title-designs/` if he wants to revisit.

## Placing it

Treat it like any Step 8 overlay: a `placements.json` entry on lane 1, emitted by `place_overlays.py`. Find the kept take of the intro line in the word-level transcript (`transcript_lookup.py --phrase "hey everyone i'm shaw"`, last occurrence wins) and translate to timeline time through the spine. Start the title a beat after the cut lands, around 0.3 s into the kept take, so it rises while he is saying his name rather than popping on the first frame. The natural 5 s length is right; don't trim it unless the intro is shorter than that.

```json
{"placements": [{"asset": "~/Documents/_stv/_content/_LFC/YT_assets/shaw_talebi_title3.mov", "start": 0.3}]}
```

Copy the `.mov` into the video's `2-drafts/<video>/assets/` folder (numbered like the other overlays, e.g. `1-title-shaw_talebi.mov`) before placing, so the FCPXML references a path that travels with the project.

## Changing the text or look

Edit the HTML, then re-render with `animation-builder`:

```
uv run --project ~/.claude/skills/animation-builder ~/.claude/skills/animation-builder/scripts/render.py \
    shaw_talebi_title3.html --alpha --fps 60 --duration 5 --out shaw_talebi_title4.mov
```

Bump the number rather than overwriting, and copy the new pair back to `YT_assets` so the next edit finds it. Check the result by compositing a frame over a real intro frame with PIL (`Image.alpha_composite`); ffmpeg's `overlay` filter has dropped the alpha on these files and shown nothing.
