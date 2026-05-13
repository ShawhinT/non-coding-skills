---
name: aba-brand-system
description: >
  AI Builder Academy's brand and design system — colors, typography, voice/tone,
  components, icons, and copy patterns for aibuilder.academy and any ABA-branded
  surface (landing pages, decks, one-pagers, social graphics, emails). Use
  whenever Shaw is designing, mocking up, or reviewing anything that should look
  or sound like ABA. Triggers: "design a landing page for ABA", "make an ABA
  mockup", "one-pager for [ABA offer]", "what colors / font does ABA use",
  "ABA-ify this", "make this on brand", "what's the ABA voice", "design an ABA
  banner / hero / card / form", "slide template for ABA", "match the ABA
  homepage". Also fire on any AI Builder Academy reference when the deliverable
  is a visual artifact (HTML, slide, image, mockup, SVG, React component) or copy
  that sits on an ABA surface. Casual mentions like "make it look like the ABA
  site" or "give this an aibuilder.academy feel" count too.
---

# AI Builder Academy — Brand & Design System

This skill codifies the look, feel, and voice of **AI Builder Academy (ABA)** — Shaw Talebi's LMS + services platform at [aibuilder.academy](https://aibuilder.academy). Use it whenever you're producing a visual artifact (landing page, mockup, one-pager, slide, social graphic, HTML email, SVG, React component) or copy that should sit on an ABA surface.

The brand is **dark, editorial, founder-direct**. Calm and serious, not flashy. Direct founder-to-founder copy, no AI hype. A small palette, three fonts, consistent radii.

## Register: marketing vs. app

Every ABA surface is one of two registers. Identify before designing — the tokens are shared, but the emphasis differs.

- **Marketing (brand register).** Landing pages, course pages, one-pagers, slides, social graphics, emails. Design *is* the product here — voice carries the page, hierarchy is editorial, eyebrows and underline-highlights earn their keep, body copy stays at 65–75ch, white space is generous.
- **App / LMS (product register).** Course player, dashboard, settings, account, admin surfaces. Design *serves* the task — density beats decoration, status feedback beats hero treatment, eyebrows are rare, body copy can drop below 65ch in tables, badges proliferate to communicate state. The visual identity is the same palette and type; the rhythm is faster.

If a surface is ambiguous (e.g. a logged-in "explore courses" page), pick the register that matches the user's *state*: are they here to be persuaded (marketing) or to do a task (product)?

## Before you design any new surface

Run this three-step prelude before opening the template or matching an existing pattern. It catches the cases where the right answer is *not* to match what already exists.

1. **Scene sentence.** One sentence: who's looking, what state are they in, what's the single next action. Not "a page about services" — "a busy founder at 11pm, third tab open comparing AI consultants, deciding in 30 seconds whether Shaw is real and bookable." If the sentence doesn't force the CTA and the visual priority, add detail until it does.
2. **Register.** Marketing or product? (See above.)
3. **Color strategy.** ABA is **Restrained** by default — tinted near-black neutral + Cerulean as the one accent doing ~80% of the chromatic work. Cardinal red, lime, goldenrod, coral are *semantic only* (wordmark / free or success / paid / pain). Don't drift to a Committed (one color owning the surface) or Drenched (the surface IS the color) strategy without a deliberate campaign exception that the user has agreed to.

## When you fire

1. **Read this whole SKILL.md.** Don't skim. The brand is more about restraint than rules.
2. **Pull the reference files relevant to your task.** They live next to this file in `references/`:
   - `references/colors_and_type.css` — the canonical CSS variables, drop-in for any HTML deliverable
   - `references/voice-and-tone.md` — exhaustive copy guidance with do/avoid examples
   - `references/components.md` — annotated component code (buttons, cards, badges, inputs, header, footer)
   - `references/icons.md` — the inline-SVG icon system (paths + usage)
3. **Match an existing pattern before inventing a new one.** Every component below has been used on the live site. If you find yourself drawing a new shape, designing a new card variant, or coining a new microcopy phrase, stop and reach for what already exists.

## Quick reference (the tokens you'll use most)

### Colors (raw hex / oklch)

| Token | Value | Where it shows up |
|---|---|---|
| `--aba-primary` | `#087CA7` | Cerulean. **The brand color.** CTAs, links, focus rings, hero glow, eyebrows. |
| `--aba-secondary` | `#B80C09` | Cardinal red. Used sparingly — the wordmark red, occasional accents. |
| `--aba-accent` | `#8FC93A` | Lime. "Available" / "Free" / success / live-event dot / course progress. |
| `--aba-warning` | `#D19C1D` | Goldenrod. Paid course prices, ★ ratings. |
| `--aba-error` | `#EE6352` | Coral. Pain-point cards, form errors. |
| `--aba-success` | `#519872` | Forest. Form success states. |
| `--aba-base-100` | `#010413` | **Page background.** Near-black with a hair of blue. Almost everything sits on this. |
| `--aba-base-200` | `oklch(20% 0.042 265.755)` | Slightly lifted card surface. |
| `--aba-base-300` | `oklch(27% 0.041 260.031)` | Borders, dividers, neutral chrome. |

Foreground text uses **opacity-on-white**, not separate gray tokens:

- `rgba(255,255,255,1.0)` → primary text (titles)
- `rgba(255,255,255,0.6)` → body copy default
- `rgba(255,255,255,0.5)` → muted / subdued
- `rgba(255,255,255,0.4)` → meta labels, captions
- `rgba(255,255,255,0.3)` → very subtle (microcopy)
- `rgba(255,255,255,0.08)` → dividers / hairlines

### Type

| Role | Family | Weights | Notes |
|---|---|---|---|
| Headings, eyebrows, badges, button labels | **Manrope** | 700 / 800 | Tracking-tight (`-0.01em` to `-0.02em` on h1). Almost always extrabold (800). |
| Body, links, nav | **Libre Franklin** | 400 / 500 / 600 / 400i | Leading-relaxed (~1.6). |
| Code, meta, durations, "Free. No spam." | **JetBrains Mono** | 400 / 500 / 600 | Used for any "label" feel — eyebrows are still Manrope, but durations/badges/microcopy are mono. |

Load from Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Libre+Franklin:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

**Type scale:**

- Display XL (hero h1): `clamp(2.5rem, 5vw + 1rem, 3.75rem)` Manrope 800, tracking `-0.02em`, line-height 1
- Display LG (section h2): `clamp(2rem, 3vw + 1rem, 2.5rem)` Manrope 800, tracking `-0.01em`
- H2: 30px / 800 / line-height 1.1
- H3 (card title): 18px / 800
- Body lg: 18px / 400
- Body: 16px / 400 / line-height 1.6
- Small: 14px
- XS / meta: 12px
- Eyebrow: 14px Manrope 600 uppercase, letter-spacing `0.2em`, color `--aba-primary`

### Radii

- `--radius-box`: `0.25rem` — code blocks
- `--radius-lg`: `0.5rem` — small chips
- `--radius-xl`: `0.75rem` — status badges, FAQ accordion items
- `--radius-2xl`: `1rem` — **cards** (pain, service, testimonial, login, contact). The dominant corner on the site.
- `--radius-field`: `2rem` — **fully-pilled buttons & input pills**

### Spacing

Standard Tailwind rhythm. Section padding `py-5 lg:py-8 my-8`; hero is taller (`py-7 lg:py-10`). Page max-width `max-w-7xl` (80rem / 1280px). Horizontal page padding `px-4 md:px-8 lg:px-8`.

### Shape & elevation

- **Almost flat.** No global shadow system. The only shadow used is a soft primary-tinted glow on card hover: `box-shadow: 0 10px 25px -5px color-mix(in srgb, #087CA7 8%, transparent)`.
- **Borders are 1px and low-opacity:** `border: 1px solid rgba(255,255,255,0.08)` is the default. Card variants use `border-base-300` / `border-error/20` / `border-primary/50` (hover).
- **No thick outlined buttons or cards.**
- **No backdrop-blur on marketing pages.** Transparency/blur is absent.

### Motion

- One named keyframe — `@keyframes marquee` for the logo strip (90s linear infinite). That's it.
- `html { scroll-behavior: smooth }` (gated by `prefers-reduced-motion: no-preference`).
- All hover/press transitions are `transition-colors` or `transition-all` at 150–200ms, default easing.
- **No bounces, no scale transforms, no spring physics, no entrance animations.**

### The one gradient

The hero has a single faint radial-blue glow:
```css
background: radial-gradient(ellipse 60% 50% at 50% 40%, rgba(8,124,167,0.12) 0%, transparent 70%);
```
**Don't add more gradients.** The only other multi-color gradients are the diagonal thumbnails inside service/training cards (`from-primary to-primary/40`, `from-warning to-success`) — always confined to ~16:9 tiles with a single white icon centered.

## Components (canonical patterns)

Full annotated code lives in `references/components.md`. The quick visual:

### Buttons

Always pill-shaped (`border-radius: 32px`), Manrope 700, no shadow, color-only hover.

- **Primary CTA:** `background: #087CA7`, white text, `padding: 14px 28px` for `btn-lg`. Label is the next thing you'd say + `→` (e.g., `"Book intro call →"`).
- **Outline:** transparent background, `border: 1px solid rgba(255,255,255,0.3)`, white text. Used for secondary forms (e.g., "Send" on contact form).
- **Neutral:** `background: oklch(27% 0.041 260.031)`, used for OAuth ("Continue with Google").

### Cards

All cards: `border-radius: 1rem` (`rounded-2xl`), 1px low-opacity border, transition-all 200ms. On hover: `border-primary/50` + soft primary-tinted shadow.

- **Pain card:** `background: rgba(238,99,82,0.07)` + `border: 1px solid rgba(238,99,82,0.2)`. Title in coral (`#EE6352`) Manrope 700. Body `rgba(255,255,255,0.5)`. Hover steps to `bg-error/14 border-error/40`.
- **Service / training card:** `bg-base-200` + `border-base-300`. Has a 16:9 gradient thumbnail (diagonal `from-primary to-primary/40`) with a single white outline icon centered. Pill badge ("90 min"), title in Manrope 800, body muted, price line, then a lime `"Book intro call →"` in mono.
- **Testimonial card:** `bg-rgba(0,15,40,0.5)`, decorative Georgia serif curly-quote in primary-blue, quote in `rgba(255,255,255,0.7)`, attribution with a tiny primary-blue dash + name + role muted.

### Badges

Pill-shaped (`border-radius: 32px`), `padding: 4px 10px`, **JetBrains Mono 11px** font (this is what tells you it's a badge — duration/price/status reads as data, not prose).

- Free → `background: #8FC93A` + black text
- Paid price → `background: #D19C1D` + white text
- Duration → `background: #087CA7` + white text
- Live-event dot → a `10x10px` `#8FC93A` circle followed by `LIVE TUE, MAY 5` in mono accent

### Inputs

- **Underline / soft style:** transparent background, `border: 1px solid rgba(255,255,255,0.2)`, `border-radius: 8px`, `padding: 10px 14px`, Libre Franklin 14px. On focus: `border-color: #087CA7`.
- **OTP boxes:** `48x56px`, `background: oklch(20% 0.042 265.755)`, `border: 1px solid oklch(27% 0.041 260.031)`, primary-blue mono text at 22px, centered.

### Header / nav

- `max-w-7xl` centered, horizontal padding `px-8`, vertical `py-3`.
- Left: wide PNG wordmark at `height: 54px` (`h-17`).
- Center/right: 3 nav links in Libre Franklin 14px 500 (Events / Courses / Services), then a primary pill CTA (`"Get in touch"`).
- No shadow under the navbar — only a low-opacity `border-bottom` on the auth pages.

### Footer

3-column grid on desktop, single column on mobile.

- Col 1: small square logo (40px, rounded) + wordmark in Manrope 600 + `"Built with 🥖 by Shaw Talebi"` in JetBrains Mono at 12px + social icons row (LinkedIn / YouTube / GitHub).
- Col 2: two stacks of uppercase tracked links (`Events / Courses / Services / Contact` and `Privacy / Terms / Support`) in Libre Franklin 500 12px, all at 50% opacity.
- Col 3: `STAY IN THE LOOP` eyebrow (Manrope 700 uppercase tracked) + email input + small pill `Subscribe` button + `"Free. No spam. Unsubscribe anytime."` in JetBrains Mono 11px at 30% opacity.
- Centered copyright row at the bottom with a `border-t border-base-content/5`.

### FAQ accordion

Each row: `border: 1px solid rgba(255,255,255,0.08)`, `border-radius: 12px`, `padding: 16px 18px`. Question is **Manrope 600 14px**. Question phrasing matches how a real prospect would type ("Do I need to be technical?", "We already use AI day-to-day. Is this still useful?"). Plus/× toggle in muted white on the right. Open state shows answer below in body color at 50% opacity.

## Absolute bans (match-and-refuse)

If you're about to write any of these, rewrite the element with different structure. These are the things that make an ABA surface stop looking like ABA. They consolidate the no-list scattered through this doc — scan this section before designing, not after.

**Visual / structural:**
- **Skeuomorphism, glassmorphism, backdrop-blur.** Transparency and blur are absent from this brand.
- **Gradient-heavy "AI" look.** Glowing orbs, sparkle particles, neon edges, gradient-on-everything. The whole brand is positioned against this lane.
- **Gradient text.** `background-clip: text` with a gradient. Emphasis through weight, size, or the manual underline highlight — never gradient fills.
- **Hero-metric template.** Big number + tiny label + supporting stats row + accent — the SaaS dashboard cliché. ABA spells credentials inline in body copy ("8+ years, 100k+ builders"), never as iconified stat cards.
- **Big hero images, decorative illustrations, stock photography.** None of these.
- **Side-stripe borders.** Colored `border-left`/`border-right` greater than 1px as accents on cards or callouts. Use full borders, background tints, or nothing.
- **Identical card grids beyond the canonical patterns.** If you find yourself drawing a fifth card variant, the content needs a different structure, not another card.
- **Modal as first thought** (app register). Modals are usually laziness. Exhaust inline / progressive disclosure / route-based alternatives first.

**Motion:**
- **Bounce, spring, elastic, scale-overshoot entrances.** Hover/press at 150–200ms color transitions is the whole motion budget on marketing pages.

**Color:**
- **Pure `#000` or `#fff`.** Page background is `#010413`, foreground is `rgba(255,255,255,0.X)` — never raw black/white.
- **Adding a sixth chromatic color.** The palette is closed. New campaigns extend through value/opacity of existing tokens, not new hues.

**Copy:**
- **AI-hype words:** *transformative, leverage, paradigm, supercharge, unlock, revolutionize, game-changing, next-level, cutting-edge, seamless, AI-powered.*
- **Exclamation points** outside small UI states. **Generic CTAs:** "Click here", "Submit", "Learn more".
- **Emoji on marketing surfaces.** The 🥖 in Shaw's footer signature is the one exception — a personal mark, not a pattern to repeat.
- **Em dashes** in display type. Use commas, colons, parentheses, or two short lines. Em dashes at 60–80px size read as rendering glitches.
- **Title Case headings.** Sentence case for everything except proper nouns.

## The AI-slop check

Before shipping, run two altitudes. The brand is genuinely positioned in a saturated category — the protection is reflex-based, not just rule-based.

- **First-order:** would a generic AI-consulting homepage already look like this? (glowing orb, gradient hero, "Unlock the power of AI", iconified stat cards). If yes, the design has collapsed to the category default. Rework.
- **Second-order:** would a *"not-generic"* AI-consulting homepage already look like this? (dark editorial + Cerulean accent + Manrope big-and-bold + underline-highlighted hero phrase). This is the lane ABA is in, and the lane is filling up. If the page is indistinguishable from three other "anti-SaaS" AI founders' sites, something needs to break the pattern — a structural choice (no hero, single-column long-form, terminal-style typesetting) or a copy choice (a specific number/anecdote in the H1 instead of a slogan). Match the system, don't be the system.

## Voice & tone (this is half the brand)

**Copy is founder-to-founder.** Shaw is the implied speaker; the reader is a busy founder-CEO who already uses AI. Plain, declarative, assumes the reader is smart and short on time.

### Always

- **Direct second person.** "You don't need to become an AI expert. You need AI doing real work."
- **Plain working-English.** "Put AI to work" / "install AI across the business" / "hand off this workflow."
- **Short, declarative sentences.** Two-clause max.
- **Concrete over abstract.** "$50K and three months of consulting that generated little ROI" beats "frustrating prior experiences."
- **Sentence case for headings.** "Is this for you?", "Frequently asked questions." Title Case only for proper nouns ("AI Builder Academy", "1:1 Workshop").
- **CTAs read like the next thing you'd say** + trailing `→`: "Book intro call →", "Let's talk.", "Get in touch →".

### Never

- **No AI-hype words.** Forbidden: *transformative, leverage, paradigm, supercharge, unlock, revolutionize, game-changing, next-level, cutting-edge, seamless, AI-powered.*
- **No exclamation points** outside small UI states. No "Click here", "Submit", "Learn more about our services."
- **No emoji on marketing pages.** The 🥖 in the footer "Built with 🥖 by Shaw Talebi" is the one exception — a personal signature, never a pattern to repeat.
- **No stat cards with icons.** Numbers and credentials are spelled out in body copy: "Ex-Toyota Data Scientist with 8+ years in AI. Teaching over 100k builders." Not iconified.
- **Social proof is logos, not metrics.** A muted brightness-0/invert marquee. Specific names recur in About Shaw (Google, Microsoft, Meta, AWS, NCSL, CEI, Matson). Numbers only appear inline ("4.7★ from 75 reviews", "165 grads").

### The hero pattern

Every marketing hero on the site follows the same structure:

1. Eyebrow (uppercase Manrope, primary-blue, `0.2em` tracking) — e.g., `TRANSFORM YOUR BUSINESS`
2. 2-line H1 with **one phrase highlighted** by a manual underline behind the text — e.g., `"AI Lets Small Teams Do Big Things."` with `"Big Things"` highlighted.
3. 1-sentence subhead.
4. Single primary CTA with trailing `→` arrow.

The underline highlight is rendered as a `::before` pseudo-element behind the text, 0.25em tall, in primary-blue at 90% opacity. See `.highlight` in `references/colors_and_type.css`.

### Pain-point cards

Titled like complaints, not features:

- ✅ "You're only scratching the surface."
- ✅ "You've been burned before."
- ✅ "You don't know what to focus on."
- ❌ "Underutilized AI capabilities"
- ❌ "Past consulting disappointments"

Then a one-sentence amplification in muted body color.

### CTA microcopy library

- Primary: `"Book intro call →"` / `"Get in touch →"` / `"Let's talk."`
- Footer: `"Free. No spam. Unsubscribe anytime."`
- Mid-funnel: `"Book a 25-minute call. We'll find one workflow worth handing off this week."`
- Newsletter heading (footer column): `STAY IN THE LOOP` (uppercase Manrope, tracked)

Full voice guide with do/avoid examples lives in `references/voice-and-tone.md`.

## Iconography

**ABA does not use an icon font.** All icons are **inline SVG** at `viewBox="0 0 24 24"`, stroke `1.5`, `currentColor`, with `stroke-linecap="round"` and `stroke-linejoin="round"`. Style is **Heroicons outline**. A small filled subset exists for ★ (rating), ♥ (favorite), • (dot), and social brand marks.

**Default sizes:**
- Inline UI icons: `20px` or `22px` (`size-5`)
- Thumbnail centerpieces (inside card gradient tiles): `48px` (`size-12`)
- Live-event dot: `10–12px`

**Coloring:** icons inherit `currentColor`. Tint with `color: #087CA7` / `#8FC93A` / `#EE6352` / `#D19C1D` — never with a stroke override.

Full path constants for the icons used on the live site (`arrowRight`, `check`, `play`, `tools`, `bulb`, `rocket`, `clock`, `calendar`, `envelope`, `user`, `chart`, `chat-bubble`, `bolt`, `cog`, `light-bulb`, `academic-cap`, `sparkles`, `lock`, etc.) are in `references/icons.md`. Social brand marks (`linkedin`, `youtube`, `github`, `x`) are filled, `currentColor`, also in that file.

**Do not draw new SVGs from scratch.** If a needed icon isn't in the list, copy an equivalent **Heroicons outline** path at 1.5 stroke.

## Logos

The dark-variant logo is the default (the site is dark).

- Wordmark (navbar): use a wide PNG at `height: 54px`. The skill's `assets/` folder has reference PNGs (`logo-wide-dark.png`, `logo-wide-light.png`).
- Square mark (footer / favicon / app icon): `assets/logo-square-dark-192.png` and `logo-square-dark-512.png`. Render at 40×40 rounded for footer, 32×32 for chips.
- **Partner / "taught at" logos** are always rendered with `filter: brightness(0) invert(1); opacity: 0.4` (marquee) or `opacity: 0.7` (taught-at grid). They never appear in native colors.

## Surfaces & layout

| Surface | Pattern |
|---|---|
| Marketing landing | Hero → social-proof marquee → pain cards → service ladder → testimonial → secondary CTA → FAQ → footer |
| Course landing | Hero (course title + duration badge + free/paid badge) → curriculum list → instructor card → CTA |
| Login | Centered card on `base-100`, OAuth button + email OTP. Card uses `bg-base-200`, `rounded-2xl`, 1px `border-base-content/15`. |
| Contact | Single-column form, underline-style inputs, `Send` outline button. |

Grids: 1-col mobile → 2- or 3-col `md:` / `lg:`. Pain points use a 1/4/6 progression (mobile / `md:grid-cols-4` / `lg:grid-cols-6`) to center the odd card.

## Drop-in CSS

For any HTML deliverable, paste `references/colors_and_type.css` at the top. It defines every variable and the base body / heading / link styles. After that you can lay out with Tailwind, plain CSS, or inline styles — the tokens are the source of truth.

## Process checklist before you ship a deliverable

1. ☐ Page background is `#010413`. Body text is white at 60% opacity. Headings are Manrope 800.
2. ☐ Every button is a full pill (`border-radius: 32px`), Manrope 700, no shadow.
3. ☐ Every card is `rounded-2xl` (`1rem`), 1px border at low opacity, flat (no shadow unless hover).
4. ☐ Eyebrows are uppercase Manrope 600, `0.2em` tracking, `#087CA7`.
5. ☐ Badges (duration / price / status) are JetBrains Mono 11px in a pill.
6. ☐ Copy is direct second-person, sentence-case, no AI-hype words, no exclamation points, no emoji (except 🥖 in the Shaw signature line).
7. ☐ CTAs read like the next thing you'd say, with a trailing `→`.
8. ☐ Icons are inline SVG, Heroicons outline, stroke 1.5, `currentColor`.
9. ☐ No gradient anywhere except the hero radial glow and the diagonal thumbnail tiles inside service cards.
10. ☐ No backdrop-blur, no decorative illustrations, no big hero images, no bounce/scale animations.

## Reference files (bundled with this skill — no external dependencies)

```
SKILL.md                       ← this file
references/
  colors_and_type.css          ← drop-in CSS variables + base element styles
  voice-and-tone.md            ← copy patterns, do/avoid, hero/pain/CTA examples
  components.md                ← annotated HTML for every canonical component
  icons.md                     ← inline-SVG icon paths + usage snippets
assets/
  README.md                    ← logo file index (logos themselves are the user's site assets)
```
