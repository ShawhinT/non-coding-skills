# ABA — motion & animation

Load this when building a motion-graphic clip (B-roll, intro card, lower-third overlay) that should sit on an ABA surface. The universal tokens and voice rules in `SKILL.md` still apply; this file covers brand motion principles and the ABA-specific overlay-accent that used to live (incorrectly) inside `animation-builder`.

## The brand motion principle: quiet

ABA's website motion budget is tiny — color-tint hover transitions at 150–200ms, the hero radial-blue glow as a static backdrop, one marquee for partner logos. That restraint carries into animation: ABA motion is **quiet**, not theatrical.

- **Color transitions, opacity fades, short translates.** That's the motion vocabulary.
- **No bounces, no spring physics, no elastic / back easings, no overshoot.** Even on display-sized type morphs.
- **No theatrical rotates.** A subtle 4–8° tilt during a morph is the ceiling. No 360° spins, no flip-cards.
- **No scale-overshoot.** Elements arrive at scale 1.0 from 0.95 or 1.05, not from 1.2.
- **No counting-up number animations.** Numbers appear in their final state or cross-fade.

If the clip needs energy, it comes from the *idea* (a wrench resolving into a screwdriver, two cards bottom-aligning) — not from the easing curve.

## Easings — what to use, what to avoid

- **Standard / both-ways morphs:** `cubic-bezier(0.4, 0, 0.2, 1)` (Material standard in-out). Symmetric, restrained, the right default for A→B cross-fades.
- **Elements entering / settling:** `cubic-bezier(0.16, 1, 0.3, 1)` (exponential out). The deceleration reads as confident arrival.
- **Decelerate-only:** `cubic-bezier(0.0, 0, 0.2, 1)`. Use when an element slides in from off-screen and lands.
- **Avoid entirely:** anything in the `back` or `elastic` family. Any `cubic-bezier` with `y > 1` or `y < 0` (overshoot). The default browser `ease-in-out` is acceptable for short pulses but `cubic-bezier(0.4, 0, 0.2, 1)` is preferred for consistency.

## Durations

- **Element entry / settle:** 400–800ms.
- **A→B morph:** 400–600ms transition + 200–400ms pre-roll on state A + ≥2s hold on state B.
- **Stagger between elements:** 100–200ms. Anything tighter and they fire together; anything wider and the eye loses the thread.
- **Sequence beat:** 800–1500ms per element if pacing to voice-over.
- **Total clip:** 1–6s per `animation-builder`'s contract. Hold the composed final frame for ≥2s.

## One moving accent at a time

The website allows one moving accent (a marquee, a hover tint). Carry the rule into animations:

- **Stagger, don't choreograph a swarm.** If the composition has five elements, they fade in one by one with a 150ms stagger — they don't all wiggle simultaneously.
- **Glow-as-entry-signal, not pulse.** A faint Cerulean glow (matching the hero radial) on an element's arrival is allowed. Pulsing the glow on/off as decoration is not.
- **Stillness is the default state.** Held frames are not empty — they're the asset. Don't add idle motion to "keep the clip alive."

## Overlay accent for karaoke captions (ABA-specific)

For text-only karaoke captions that composite over talking-head footage (an `.accent` span emphasizing a word, no pill/card backing), **do not use ABA Cerulean `#087CA7` at full strength**. Cerulean is tuned for ink on white surfaces — it reads as muddy or muted against varied talking-head footage (warm lamplight, dark clothing, mid-tone walls).

The ABA house overlay-accent is **`#5DC3E8`** — a lighter, brighter cyan-blue. It punches against both bright and dark backgrounds, and the standard legibility shadow (see below) still gives it definition.

This applies only to **font-only karaoke overlays** — captions with no pill, no card, no chip backing. Where accent text sits on its own white pill or card surface (e.g. lower-third name plate with a white background), keep the brand primary Cerulean — the surface contrast does the legibility work and Cerulean is the right color against white. The test: is the talking-head footage itself the backdrop behind this word? If yes, use `#5DC3E8`. If a white surface is between the text and the footage, use Cerulean.

### Legibility shadow (paired with the overlay accent)

```css
text-shadow:
  0 0 24px rgba(0, 0, 0, 0.55),
  0 4px 12px rgba(0, 0, 0, 0.45);
```

White body text + `#5DC3E8` accent on a span both use this shadow. No card-like backdrop behind the text.

## Section-card defaults for ABA

When building a chapter slate for an ABA-tagged video:

- **Eyebrow** (`STEP 0`, `PART 01`) — Cerulean, Manrope 600 uppercase, `0.2em` tracking. Single-digit numbering on screen (zero-padding is for filenames).
- **Title** — Manrope 800 in white. Title Case is the exception to the brand's sentence-case rule (see `animation-builder` SKILL.md — chapter slates are titles, not body labels).
- **No logos, no signatures, no body copy, no decorative glyphs.** Three elements max.
- **Title-internal visual marks (arrows, separators) stay title-colored** (white/bone), not Cerulean. The accent belongs to eyebrows and progress rails — not inside the title.

## Color hygiene for ABA animations

- **Never `#000` or `#fff`** on encoded output. Pure black crushes under H.264 and produces banding around Cerulean glows. Use `oklch(0.16 0.01 250)` for dark backgrounds (already in `colors_and_type.css` as the conceptual equivalent of `--aba-base-100`).
- **Hairline strokes shimmer.** A 1px Cerulean stroke on near-black flickers after compression. Use ≥1.5px, or pair the stroke with a faint same-color glow.
- **One accent per clip.** Cerulean by default. Brand-mark colors of depicted products (Claude coral, Stripe purple) are fine; they don't count as a second accent.

## Quick checklist before rendering an ABA clip

1. ☐ Motion vocabulary is fades / opacity / short translates / color transitions. No bounces, no overshoot, no theatrical rotates.
2. ☐ Easings are `cubic-bezier(0.4, 0, 0.2, 1)` or `cubic-bezier(0.16, 1, 0.3, 1)`. No `back` / `elastic`.
3. ☐ Karaoke caption accents (no pill backing) use `#5DC3E8`, not Cerulean.
4. ☐ Karaoke caption text has the soft+hard legibility shadow.
5. ☐ Section-card titles are Title Case; eyebrows and body labels are sentence case.
6. ☐ Composed final frame holds for ≥2 seconds.
7. ☐ Background is tinted dark (`oklch(0.16 0.01 250)`), not pure `#000`. Body text isn't pure `#fff`.
8. ☐ One accent doing the work. No secondary decorative hue.
