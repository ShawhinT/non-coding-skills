# ABA — web composition

Load this when building anything that renders in a browser — a marketing landing page, a course page, the LMS app, an HTML email, a docs site, an admin surface. The universal tokens in `SKILL.md` and `colors_and_type.css` are the foundation; this file covers the website-specific composition (hero stack, header, footer, hover states, motion, Tailwind rhythm) that doesn't transfer to infographics or animations.

## Register: marketing vs. app

Every web surface is one of two registers. The tokens are shared; the emphasis differs.

- **Marketing (brand register).** Landing pages, course pages, one-pagers, slides, HTML emails. Design *is* the product — voice carries the page, hierarchy is editorial, eyebrows and underline-highlights earn their keep, body copy stays at 65–75ch, white space is generous.
- **App / LMS (product register).** Course player, dashboard, settings, account, admin surfaces. Design *serves* the task — density beats decoration, status feedback beats hero treatment, eyebrows are rare, body copy can drop below 65ch in tables, badges proliferate to communicate state. Same palette and type; faster rhythm.

If a surface is ambiguous (e.g. a logged-in "explore courses" page), pick the register that matches the user's *state*: are they here to be persuaded (marketing) or to do a task (product)?

## The hero pattern (marketing only)

Every marketing hero on the live site follows the same structure:

1. Eyebrow — uppercase Manrope 600, Cerulean, `0.2em` tracking. E.g. `TRANSFORM YOUR BUSINESS`.
2. 2-line H1 with **one phrase highlighted** by a manual underline behind the text. The underline is a `::before` pseudo-element, 0.25em tall, in primary-blue at 90% opacity. See `.highlight` in `colors_and_type.css`.
3. 1-sentence subhead.
4. Single primary CTA pill with trailing `→` arrow.

This pattern is *for landing pages*. Do not transfer it to infographics or animations — see the corresponding reference files.

## Page rhythm

- Page bg: `--aba-base-100` (`#010413`).
- Page max-width: `max-w-7xl` (80rem / 1280px).
- Horizontal padding: `px-4 md:px-8 lg:px-8`.
- Section padding: `py-5 lg:py-8 my-8`. Hero is taller (`py-7 lg:py-10`).
- Foreground text uses opacity-on-white, not separate gray tokens. See `--fg-1` through `--fg-7` in `colors_and_type.css`.

## Components

See `references/components.md` for the annotated catalog. The components covered there are all *web-only* primitives:

- **Buttons** — pill (`border-radius: 32px`), Manrope 700, no shadow. Primary / outline / neutral variants.
- **Cards** — `rounded-2xl`, 1px low-opacity border, flat (no shadow until hover).
- **Badges** — pill, JetBrains Mono 11px. Free / paid / duration / live-event dot.
- **Inputs** — underline-style on marketing; OTP boxes on auth.
- **Header / nav** — wide PNG wordmark + 3 nav links + primary CTA.
- **Footer** — 3 columns: signature + link stacks + newsletter signup.
- **FAQ accordion** — 1px-bordered rows, Manrope 600 14px questions, plus/× toggle.

## Hover and focus states

ABA web motion is small and color-only.

- `a:hover` lightens by mixing 80% Cerulean with 20% white.
- `.aba-card:hover` lifts the border to 50% Cerulean and adds a soft primary-tinted shadow (`--shadow-card-hover`).
- Inputs on focus: `border-color: var(--aba-primary)`.
- Button hover: background lightens by 12% white-mix.

All transitions are `transition-colors` or `transition-all` at 150–200ms (`--dur-fast` / `--dur-base`), default easing `--ease-standard`.

**No bounces, no scale transforms, no spring physics, no entrance animations on marketing pages.**

## Motion

- One named keyframe — `@keyframes marquee` for the partner-logo strip (90s linear infinite). That's it.
- `html { scroll-behavior: smooth }` (gated by `prefers-reduced-motion: no-preference`).
- The hero radial-blue glow is the only multi-color gradient on a marketing surface (other than the diagonal thumbnail tiles inside service/training cards — always a `from-primary to-primary/40` confined to ~16:9 tiles with one white outline icon centered).

## Shape & elevation

- **Almost flat.** No global shadow system. The only shadow used is a soft primary-tinted glow on card hover.
- **Borders are 1px and low-opacity:** `border: 1px solid rgba(255,255,255,0.08)` is the default. Card variants use `border-base-300` / `border-error/20` / `border-primary/50` (hover).
- **No thick outlined buttons or cards.**
- **No backdrop-blur on marketing pages.** Transparency/blur is absent.

## Pills as the dominant button shape

Every button on the live site is a full pill (`border-radius: 32px` / `--radius-field`), Manrope 700, no shadow, color-only hover. This is a web convention — infographics often have no CTA at all (they're not clickable), and animations don't render buttons. Don't transfer the pill primitive to those surfaces.

CTA labels read like the next thing you'd say + `→`:

- `Book intro call →`
- `Get in touch →`
- `Let's talk.`

## Surfaces

| Surface | Pattern |
|---|---|
| Marketing landing | Hero → social-proof marquee → pain cards → service ladder → testimonial → secondary CTA → FAQ → footer |
| Course landing | Hero (course title + duration badge + free/paid badge) → curriculum list → instructor card → CTA |
| Login | Centered card on `base-100`, OAuth button + email OTP. Card uses `bg-base-200`, `rounded-2xl`, 1px `border-base-content/15`. |
| Contact | Single-column form, underline-style inputs, `Send` outline button. |

Grids: 1-col mobile → 2- or 3-col `md:` / `lg:`. Pain points use a 1/4/6 progression (mobile / `md:grid-cols-4` / `lg:grid-cols-6`) to center the odd card.

## Web-only absolute bans

In addition to the universal bans in `SKILL.md`:

- **Backdrop-blur, glassmorphism.** Transparency and blur are absent from this brand.
- **Modal as first thought** (app register). Modals are usually laziness. Exhaust inline / progressive disclosure / route-based alternatives first.
- **Gradient overlays on hero images.** The brand doesn't use hero images.
