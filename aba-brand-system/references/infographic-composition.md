# ABA — infographic composition

Load this when building an infographic (single PNG, social-feed still) that should sit on an ABA surface. The universal tokens in `SKILL.md` and `colors_and_type.css` still apply; this file covers the things web composition doesn't — display-scale type, color at scale, light-bg inverse usage, eyebrow rules outside marketing, and the ABA-specific patterns that used to live (incorrectly) inside `graphic-builder`.

## What does *not* transfer from the web side

The ABA website hero is **eyebrow → 2-line H1 → 1-sentence subhead → primary pill CTA + `→`**. None of that transfers to a still that has ~2 seconds in the scroll.

- No CTA buttons (the graphic isn't clickable).
- No hover/transition states.
- No header/footer/nav chrome.
- The eyebrow-above-title pattern is *marketing only*. See "Eyebrow rules" below.
- The hero radial glow can carry over as a faint backdrop, but is usually overkill for a still — skip by default.

If you find yourself stacking eyebrow + H1 + subhead + accent line + CTA on a single composition, you're rebuilding the landing page. Delete back to title + body + one graphic per card.

## Display type — Manrope at 60–120px

Manrope 800 at the web hero size (`clamp(2.5rem, 5vw + 1rem, 3.75rem)` ≈ 40–60px) uses `letter-spacing: -0.02em` and works fine. At infographic display scale (60–120px), behavior changes:

- **60–80px (typical 2-card title or hero label):** keep `-0.02em`. Reads tight and intentional.
- **80–100px (single-centerpiece title, large list heading):** relax to `-0.01em`. The negative tracking compounds at scale and starts to crash letterforms together (`Mn`, `rn`, `il`).
- **100–120px+ (one-word hero, square centerpiece):** drop to `0` or `+0.005em`. The letters need to breathe; tight tracking at this size reads as fused.

Line-height stays `1.0` for display, `1.1` for two-line titles. Never use `line-height: 1.6` (body default) on a display heading — it will look like a paragraph break.

## Color at scale — what holds, what doesn't

The ABA palette is tuned for 14–30px UI text and small accents. At infographic scale (badges 64–128px, accent fills 80–256px, full-width hero strokes) the behavior shifts.

- **Cerulean `#087CA7` — holds.** Crisp at any size on both dark and light. Default accent for anything ABA-tagged.
- **Lime `#8FC93A` — holds, but dominates.** At ≥80px the lime starts to feel highlighter-bright. Pair with the bg, don't let it become the visual subject unless that's the intent (success / "go" / available).
- **Goldenrod `#D19C1D` — holds well at large fills.** Reads as a confident yellow at 100px+, where smaller goldenrod chips can look brownish.
- **Cardinal red `#B80C09` — needs help at scale on dark.** At ≥80px the deep red on `#010413` reads muddy. Either lift to a brighter red for the still (`#D52220`), thicken the outline, or move it to a light surface. Don't paint a 120px cardinal block on the dark canvas.
- **Coral `#EE6352` — holds.** Stays vibrant at any size. The default ABA chat-bubble color for the "AI / Claude" sender (see below).
- **Forest `#519872` — fades at scale.** Reads muddy at >80px on dark. Use only at small-accent scale (success ticks, status dots) or swap to lime when a bigger green is needed.

Saturated colors as ≥80px fills look intentional only when paired with negative space. A 120px coral block butting against a 120px Cerulean block reads as a flag, not a comparison — separate with at least 60px of background.

## Light-bg inverse palette

`graphic-builder` defaults to a near-white canvas (`#FAFAF7`). On that surface, the ABA dark-mode opacity scheme inverts:

- Page bg: `#FAFAF7` (off-white). Avoid pure `#FFFFFF`.
- Primary text: `rgba(1, 4, 19, 1.0)` (the dark `#010413` at full opacity, not pure black).
- Body text: `rgba(1, 4, 19, 0.65)` (echoes the 60% white on dark).
- Muted/meta: `rgba(1, 4, 19, 0.5)`.
- Dividers/hairlines: `rgba(1, 4, 19, 0.08)`.

Color behavior on the inverse surface:

- **Cerulean — holds.** Still the default accent.
- **Cardinal red — holds.** This is where cardinal looks best at scale.
- **Lime — needs care.** Lime on off-white loses its punch and looks like a sticky note. Increase saturation (`#7DB72A`) or pair with a dark outline.
- **Coral — holds.**
- **Goldenrod — washes out on light.** Either pair with a darker outline / shadow, or substitute a deeper amber (`#B17A0E`).

Surface tints (lifted card on the off-white canvas): `#FFFFFF` for the card itself, `rgba(1, 4, 19, 0.04)` for a subtle alternate. No glassmorphism, no blur.

## Eyebrow rules outside marketing

ABA's signature eyebrow is uppercase Manrope 600, `0.2em` tracking, Cerulean. On the website it sits *above* the H1. **In an infographic, the eyebrow-above-title pattern is wrong.** A LinkedIn still gets a title and the body content; eyebrows-above-title push the payload below the fold and make the graphic read as a website screenshot.

When eyebrows ARE appropriate in stills:

1. **Parallel-panel discriminators** — two or more cards being explicitly compared (`TYPE 1` / `TYPE 2`, `BEFORE` / `AFTER`, `FREE` / `PAID`, `CHAT` / `CODE`). Mono, ~14px, uppercase, accent-colored. They carry structural meaning, not decoration.
2. **Below-title metadata** — when the title is the main hook, a small mono caption *below* the H1 in accent (`4-STEP FRAMEWORK`) can work. ~16px mono, one phrase, uppercase. Reads as a quiet caption, not a website pre-roll.
3. **Per-row labels in lists** — `STEP 1`, `STEP 2`, … inside a numbered card grid. JetBrains Mono in accent, ~14–16px.

What to *delete*:

- An eyebrow above the H1 on a single-title composition.
- An eyebrow plus a subtitle on the same level.
- Decorative pre-roll labels ("INTRODUCING…", "NEW FRAMEWORK") that add nothing the title doesn't already say.

## Logo placement

The wordmark belongs on the website. In a still:

- **Default:** small mono signature line at the bottom-center. Personal stills use `@shawhintalebi`. **ABA-tagged stills use `aibuilder.academy`** in the same treatment — JetBrains Mono ~14px, ~60% opacity, `0.04em` tracking, centered. The brand URL replaces the personal handle; same treatment, same position.
- **Title-card or hero stills only:** the square logo mark (`logo-square-dark-192.png` on dark, the matching light variant on light) at 32–40px in a bottom or top corner at ~40% opacity. Skip the wordmark unless the still IS the title card for a larger piece (deck cover, course thumbnail).
- **Never:** wordmark on the canvas as decoration, large logo lockup, multi-element brand stamp.

## ABA chat-bubble color mapping

When an infographic depicts a chat thread between Claude and a user (a common ABA visual), the two senders map to specific brand colors:

- **AI / Claude sender:** coral `#EE6352` (the ABA error/coral token).
- **User sender:** Cerulean `#087CA7`.

Same mapping should be used consistently across all ABA conversation graphics so the colors function as a sender key without needing a legend. If the conversation involves a different non-Claude AI (e.g. depicting a tool that uses GPT or Gemini for contrast), use that brand's native color for *that* speaker and keep Cerulean for the user.

`graphic-builder` describes only the *structural* rule ("two-sender threads need two semantic accent colors with sufficient contrast"). The specific hex mapping is ABA-only and lives here.

## Composition defaults for ABA stills

- **Single visual idea per graphic.** Same rule as the generic skill.
- **Sentence-case titles.** Title Case is acceptable only for a single dominant display title when the composition is heading-driven.
- **Left-align body and headings** unless the composition is explicitly symmetric (single-centerpiece square).
- **Three elements per card max:** one heading word, one supporting line, one graphic.
- **One accent doing the chromatic work.** Cerulean by default. Brand-mark colors of products being depicted (Claude coral, Stripe purple, Slack four petals) are not second accents — they're brand marks and they're allowed.

## Footer convention

ABA-tagged stills: `aibuilder.academy` in JetBrains Mono ~14px at ~60% opacity, bottom-center, `0.04em` tracking. Quiet signature, not a brand stamp. The generic `graphic-builder` default is `@shawhintalebi` — swap to `aibuilder.academy` for ABA-branded work.

## Quick checklist before shipping an ABA still

1. ☐ The hero-stack (eyebrow + H1 + subhead + CTA) is NOT on the canvas.
2. ☐ Title sits in Manrope 800 with tracking adjusted for display size (see "Display type" above).
3. ☐ Body / muted text uses the inverse opacity scale if the canvas is light, or the dark-mode scale if dark.
4. ☐ One accent doing the chromatic work (Cerulean default). Brand-mark colors of depicted products don't count.
5. ☐ Cardinal red is not painted as a ≥80px fill on the dark canvas.
6. ☐ Footer is `aibuilder.academy` (not `@shawhintalebi`).
7. ☐ Eyebrows, if present, are parallel-card discriminators or below-title metadata — not website-style pre-roll.
8. ☐ Sentence case in body. Em dashes in display sizes are out.
