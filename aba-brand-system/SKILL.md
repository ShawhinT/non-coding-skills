---
name: aba-brand-system
description: AI Builder Academy's brand and design system — colors, typography, voice/tone, components, icons, and copy patterns for aibuilder.academy and any ABA-branded surface (landing pages, decks, one-pagers, social graphics, emails, motion graphics). Use whenever Shaw is designing, mocking up, or reviewing anything that should look or sound like ABA. Triggers: "design a landing page for ABA", "make an ABA mockup", "one-pager for [ABA offer]", "what colors / font does ABA use", "ABA-ify this", "make this on brand", "what's the ABA voice", "design an ABA banner / hero / card / form", "slide template for ABA", "match the ABA homepage", "ABA infographic", "ABA animation". Also fire on any AI Builder Academy reference when the deliverable is a visual artifact (HTML, slide, image, mockup, SVG, React component, MP4, PNG) or copy that sits on an ABA surface. Casual mentions like "make it look like the ABA site" or "give this an aibuilder.academy feel" count too.
---

# AI Builder Academy — Brand & Design System

This skill codifies the look, feel, and voice of **AI Builder Academy (ABA)** — Shaw Talebi's LMS + services platform at [aibuilder.academy](https://aibuilder.academy). Use it whenever you're producing a visual artifact (landing page, mockup, one-pager, slide, social graphic, HTML email, SVG, React component, infographic, animation) or copy that should sit on an ABA surface.

The brand is **dark, editorial, founder-direct**. Calm and serious, not flashy. Direct founder-to-founder copy, no AI hype. A small palette, three fonts, consistent radii, quiet motion.

## How this skill is organized

This file is the **universal core** — colors, type, voice, icons, logos, the absolute bans, and the AI-slop check. Everything here applies to every ABA deliverable, regardless of surface.

**Surface-specific composition lives in `references/`:**

| If you're building… | Load |
|---|---|
| A website, marketing page, course page, LMS surface, HTML email | `references/web-composition.md` + `references/components.md` |
| A still infographic (LinkedIn graphic, social-feed image, PNG one-pager, cheatsheet) | `references/infographic-composition.md` |
| A motion-graphic clip (B-roll, intro card, lower-third overlay, MP4 / `.mov`) | `references/animation-motion.md` |
| Any voice/copy decision | `references/voice-and-tone.md` |

**Same brand, different rhythms.** The website's hero stack (eyebrow → 2-line H1 → subhead → CTA) does not transfer to a 2-second LinkedIn still or a 4-second B-roll clip — the surface-specific files exist to make that clear.

## When you fire

1. **Identify the surface** and load the matching reference file from the table above.
2. **Read this whole SKILL.md** for the universal tokens, bans, and voice.
3. **Match an existing pattern before inventing a new one.** Every component below has been used in production.

## Universal tokens

### Colors (raw hex / oklch)

| Token | Value | Where it shows up |
|---|---|---|
| `--aba-primary` | `#087CA7` | Cerulean. **The brand color.** CTAs, links, focus rings, hero glow, eyebrows, default accent in stills. |
| `--aba-secondary` | `#B80C09` | Cardinal red. Used sparingly — the wordmark red, occasional accents. |
| `--aba-accent` | `#8FC93A` | Lime. "Available" / "Free" / success / live-event dot / course progress. |
| `--aba-warning` | `#D19C1D` | Goldenrod. Paid course prices, ★ ratings. |
| `--aba-error` | `#EE6352` | Coral. Pain-point cards, form errors, ABA chat-bubble color for Claude / AI sender. |
| `--aba-success` | `#519872` | Forest. Form success states. |
| `--aba-base-100` | `#010413` | **Page background on dark surfaces.** Near-black with a hair of blue. |
| `--aba-base-200` | `oklch(20% 0.042 265.755)` | Slightly lifted card surface. |
| `--aba-base-300` | `oklch(27% 0.041 260.031)` | Borders, dividers, neutral chrome. |

Foreground text uses **opacity-on-white** on dark surfaces, **opacity-on-`#010413`** on light surfaces. Full scale (`--fg-1` through `--fg-7`) is in `references/colors_and_type.css`.

Behavior at scale (large fills, infographic-sized blocks) and the light-bg inverse palette are covered in `references/infographic-composition.md`.

### Type

| Role | Family | Weights | Notes |
|---|---|---|---|
| Headings, eyebrows, badges, button labels | **Manrope** | 700 / 800 | Tracking-tight (`-0.01em` to `-0.02em` at body/hero scale; relax at display scale per `infographic-composition.md`). Almost always extrabold (800). |
| Body, links, nav | **Libre Franklin** | 400 / 500 / 600 / 400i | Leading-relaxed (~1.6). |
| Code, meta, durations, badges, "Free. No spam." | **JetBrains Mono** | 400 / 500 / 600 | Used for any "label" feel — eyebrows are still Manrope, but durations/badges/microcopy are mono. |

Load from Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Libre+Franklin:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

**Web type scale** lives in `references/colors_and_type.css` (`--fs-display-xl`, `--fs-display-lg`, etc.). **Display type at infographic scale (60–120px)** has its own tracking rules — see `references/infographic-composition.md`.

### Radii

- `--radius-box`: `0.25rem` — code blocks
- `--radius-lg`: `0.5rem` — small chips
- `--radius-xl`: `0.75rem` — status badges, FAQ accordion items
- `--radius-2xl`: `1rem` — **cards**. The dominant corner on every ABA surface.
- `--radius-field`: `2rem` — **fully-pilled buttons & input pills** (web only — infographics typically have no buttons).

### Iconography

**ABA does not use an icon font.** All icons are **inline SVG** at `viewBox="0 0 24 24"`, stroke `1.5`, `currentColor`, with `stroke-linecap="round"` and `stroke-linejoin="round"`. Style is **Heroicons outline**. A small filled subset exists for ★ (rating), ♥ (favorite), • (dot), and social brand marks.

**Default sizes:**
- Inline UI icons: `20px` or `22px` (`size-5`)
- Thumbnail centerpieces (inside card gradient tiles): `48px` (`size-12`)
- Live-event dot: `10–12px`
- Infographic flow arrows: bump `stroke-width` to `2.5–3` — the default 1.5 reads as a hairline render glitch at 22–32px on-canvas. See `infographic-builder` Gotchas.

**Coloring:** icons inherit `currentColor`. Tint with `color: #087CA7` / `#8FC93A` / `#EE6352` / `#D19C1D` — never with a stroke override.

Full path constants for the icons used on the live site (`arrowRight`, `check`, `play`, `tools`, `bulb`, `rocket`, `clock`, `calendar`, `envelope`, `user`, `chart`, `chat-bubble`, `bolt`, `cog`, `light-bulb`, `academic-cap`, `sparkles`, `lock`, etc.) are in `references/icons.md`. Social brand marks (`linkedin`, `youtube`, `github`, `x`) are filled, `currentColor`, also in that file.

**Do not draw new SVGs from scratch.** If a needed icon isn't in the list, copy an equivalent **Heroicons outline** path at 1.5 stroke.

### Logos

The dark-variant logo is the default (most ABA surfaces are dark).

- **Wordmark (navbar):** wide PNG at `height: 54px`. The skill's `assets/` folder has reference PNGs (`logo-wide-dark.png`, `logo-wide-light.png`). Wordmark is a web/marketing element — not used as decoration in stills or motion graphics.
- **Square mark (footer / favicon / app icon / corner stamp on stills):** `assets/logo-square-dark-192.png` and `logo-square-dark-512.png`. Render at 40×40 rounded for footer, 32×32 for chips.
- **Partner / "taught at" logos** are always rendered with `filter: brightness(0) invert(1); opacity: 0.4` (marquee) or `opacity: 0.7` (taught-at grid). They never appear in native colors.

### Drop-in CSS

For any HTML deliverable, paste `references/colors_and_type.css` at the top. It defines every variable and the base body / heading / link styles. After that you can lay out with Tailwind, plain CSS, or inline styles — the tokens are the source of truth.

## Voice & tone (this is half the brand)

**Copy is founder-to-founder.** Shaw is the implied speaker; the reader is a busy founder-CEO who already uses AI. Plain, declarative, assumes the reader is smart and short on time.

### Always

- **Direct second person.** "You don't need to become an AI expert. You need AI doing real work."
- **Plain working-English.** "Put AI to work" / "install AI across the business" / "hand off this workflow."
- **Short, declarative sentences.** Two-clause max.
- **Concrete over abstract.** "$50K and three months of consulting that generated little ROI" beats "frustrating prior experiences."
- **Sentence case for headings.** "Is this for you?", "Frequently asked questions." Title Case only for proper nouns ("AI Builder Academy", "1:1 Workshop"). Exception: full-bleed chapter/section card titles in YouTube B-roll use Title Case (see `references/animation-motion.md`).
- **CTAs read like the next thing you'd say** + trailing `→`: "Book intro call →", "Let's talk.", "Get in touch →".

### Never

- **No AI-hype words.** Forbidden: *transformative, leverage, paradigm, supercharge, unlock, revolutionize, game-changing, next-level, cutting-edge, seamless, AI-powered.*
- **No exclamation points** outside small UI states. No "Click here", "Submit", "Learn more about our services."
- **No emoji on marketing pages or stills.** The 🥖 in the footer "Built with 🥖 by Shaw Talebi" is the one exception — a personal signature, never a pattern to repeat.
- **No stat cards with icons.** Numbers and credentials are spelled out in body copy: "Ex-Toyota Data Scientist with 8+ years in AI. Teaching over 100k builders." Not iconified.
- **Social proof is logos, not metrics.** A muted brightness-0/invert marquee. Specific names recur in About Shaw (Google, Microsoft, Meta, AWS, NCSL, CEI, Matson). Numbers only appear inline ("4.7★ from 75 reviews", "165 grads").

Full voice guide with do/avoid examples lives in `references/voice-and-tone.md`. The hero pattern, pain-point card phrasing, and CTA microcopy library are also there.

## Absolute bans (match-and-refuse)

If you're about to write any of these, rewrite the element with different structure. These are the things that make an ABA surface stop looking like ABA. Scan this section before designing, not after.

**Visual / structural:**
- **Skeuomorphism, glassmorphism, backdrop-blur.** Transparency and blur are absent from this brand.
- **Gradient-heavy "AI" look.** Glowing orbs, sparkle particles, neon edges, gradient-on-everything. The whole brand is positioned against this lane.
- **Gradient text.** `background-clip: text` with a gradient. Emphasis through weight, size, or the manual underline highlight — never gradient fills.
- **Hero-metric template.** Big number + tiny label + supporting stats row + accent — the SaaS dashboard cliché. ABA spells credentials inline in body copy, never as iconified stat cards.
- **Big hero images, decorative illustrations, stock photography.** None of these.
- **Side-stripe borders.** Colored `border-left`/`border-right` greater than 1px as accents on cards or callouts. Use full borders, background tints, or nothing.

**Motion:**
- **Bounce, spring, elastic, scale-overshoot entrances.** Hover/press at 150–200ms color transitions is the whole web motion budget. Animation surfaces extend this slightly (see `references/animation-motion.md`) but the principle — *quiet* — is the same.

**Color:**
- **Pure `#000` or `#fff`.** Page background is `#010413`, foreground is `rgba(255,255,255,0.X)` — never raw black/white. On light surfaces, use `#FAFAF7` and `rgba(1,4,19,0.X)`.
- **Adding a sixth chromatic color.** The palette is closed. New campaigns extend through value/opacity of existing tokens, not new hues.

**Copy:**
- **AI-hype words** (see Voice & tone above).
- **Exclamation points** outside small UI states. **Generic CTAs:** "Click here", "Submit", "Learn more".
- **Emoji on marketing surfaces.** The 🥖 in Shaw's footer signature is the one exception.
- **Em dashes** anywhere on a designed surface. Use commas, colons, parentheses, or two short lines. Shaw reads em dashes as a tell of AI-generated copy and will flag them on sight. At 60–80px display size they also read as rendering glitches.
- **Title Case headings.** Sentence case for everything except proper nouns. Exception: YouTube chapter-card titles (see `references/animation-motion.md`).

## The AI-slop check

Before shipping, run two altitudes. The brand is genuinely positioned in a saturated category — the protection is reflex-based, not just rule-based.

- **First-order:** would a generic AI-consulting homepage already look like this? (glowing orb, gradient hero, "Unlock the power of AI", iconified stat cards). If yes, the design has collapsed to the category default. Rework.
- **Second-order:** would a *"not-generic"* AI-consulting homepage already look like this? (dark editorial + Cerulean accent + Manrope big-and-bold + underline-highlighted hero phrase). This is the lane ABA is in, and the lane is filling up. If the page is indistinguishable from three other "anti-SaaS" AI founders' sites, something needs to break the pattern — a structural choice (no hero, single-column long-form, terminal-style typesetting) or a copy choice (a specific number/anecdote in the H1 instead of a slogan). Match the system, don't be the system.

## Universal process checklist

1. ☐ Surface identified — universal core + the right surface-specific reference file loaded.
2. ☐ Background is `#010413` (dark) or `#FAFAF7` (light) — not pure `#000` / `#fff`.
3. ☐ Body text uses the opacity scale on the appropriate base color.
4. ☐ Headings are Manrope 800 with tracking adjusted for size.
5. ☐ One accent doing the chromatic work (Cerulean by default).
6. ☐ Icons are inline SVG, Heroicons outline, stroke 1.5 (or 2.5–3 for emphasis arrows on stills).
7. ☐ Copy is direct second-person, sentence-case, no AI-hype words, no exclamation points, no emoji (except 🥖 in Shaw's signature line).
8. ☐ No gradient anywhere except the hero radial glow (web) and the diagonal thumbnail tiles inside service cards (web).
9. ☐ No backdrop-blur, no decorative illustrations, no big hero images, no bounce/scale animations.
10. ☐ Em dashes removed; sentence case for body.

## Reference files (bundled with this skill — no external dependencies)

```
SKILL.md                              ← this file: universal core
references/
  colors_and_type.css                 ← drop-in CSS variables + base element styles
  voice-and-tone.md                   ← copy patterns, do/avoid, hero/pain/CTA examples
  components.md                       ← annotated HTML for every canonical web component
  icons.md                            ← inline-SVG icon paths + usage snippets
  web-composition.md                  ← hero pattern, header/footer, hover/focus, marketing/app registers
  infographic-composition.md          ← display type, color at scale, light-bg palette, eyebrow rules for stills, ABA chat colors, ABA footer
  animation-motion.md                 ← brand motion principles, easings, durations, ABA karaoke overlay accent
assets/
  README.md                           ← logo file index
```
