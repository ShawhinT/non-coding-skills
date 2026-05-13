# Worked examples

When in doubt, open one of these and read the HTML before authoring from scratch. Each one represents a pattern that worked in production. The full project — HTML + rendered PNG + any local assets — is bundled inside this skill under `references/examples/<slug>/`, so the references stay valid on any machine.

## Landscape (1080×820)

- **`connectors-vs-skills`** — two-panel A vs B comparison.
  Path: `references/examples/connectors-vs-skills/connectors-vs-skills.html`
  - Two bordered cards in a `1fr 1fr` grid (with `min-width: 0` so the columns stay equal).
  - Each card: display word (Manrope 800, 70px), label line (`= capability` / `= competence`, JetBrains Mono in accent), descriptor sentence, graphic.
  - Left card graphic: hub-and-spoke SVG with Claude logo center + 5 app spokes (Gmail, Google Calendar, Notion, Stripe, Jira) connected by dashed lines.
  - Right card graphic: monospace ASCII directory tree.
  - Footer `@shawhintalebi` centered, 14px JetBrains Mono.

## Portrait (1080×1350)

- **`6-ways-claude-context`** — numbered vertical list.
  Path: `references/examples/6-ways-claude-context/6-ways-claude-context.html`
  - Title-only header. No eyebrow, no subtitle, no decorative pre-roll.
  - Six rows in a flex column with `gap: 18px`; each row is a `1.5px` border card.
  - Row grid: `70px 64px 1fr` = number (JetBrains Mono 32px Cerulean) / icon tile (`64x64` with `rgba(8,124,167,0.10)` fill + Heroicons-style inline SVG) / text block (Manrope 800 32px heading + Libre Franklin 20px desc).
  - Canvas uses `justify-content: center` with symmetric 80px top/bottom padding so the content sits balanced.
  - Use when the post is a numbered list of N≤6 with parallel structure (each item is one method/tactic/option).
  - No `assets/` folder — all icons are inline SVG.

## Square (1080×1080)

_(none yet — add when one ships.)_
