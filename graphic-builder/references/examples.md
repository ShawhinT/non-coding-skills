# Worked examples

When in doubt, open one of these and read the HTML before authoring from scratch. Each one represents a pattern that worked in production. The full project — HTML + rendered PNG + any local assets — is bundled inside this skill under `references/examples/<slug>/`, so the references stay valid on any machine.

Examples are grouped by mode. See `references/modes/` for the packaging rules each mode follows.

## Social graphic

Feed stills (LinkedIn). Wordless by default; the examples below other than `youtube-mcp` use the infographic packaging sub-mode. See `references/modes/social-graphic.md`.

### Landscape (1080×820)

- **`connectors-vs-skills`** — two-panel A vs B comparison.
  Path: `references/examples/connectors-vs-skills/connectors-vs-skills.html`
  - Two bordered cards in a `1fr 1fr` grid (with `min-width: 0` so the columns stay equal).
  - Each card: display word (Manrope 800, 70px), label line (`= capability` / `= competence`, JetBrains Mono in accent), descriptor sentence, graphic.
  - Left card graphic: hub-and-spoke SVG with Claude logo center + 5 app spokes (Gmail, Google Calendar, Notion, Stripe, Jira) connected by dashed lines.
  - Right card graphic: monospace ASCII directory tree.
  - Footer `@shawhintalebi` centered, 14px JetBrains Mono.

- **`two-types-of-skills`** — two-panel comparison with parallel-card eyebrows + bottom-anchored examples row.
  Path: `~/Documents/_stv/_content/_SFC/sfc/2026/ai-education/two-types-of-skills/two-types-of-skills.html`
  - Title at top (Manrope 800, 48px), then two cards in `1fr 1fr` grid.
  - Each card: `TYPE 1` / `TYPE 2` mono eyebrow → display word → one-line descriptor → graphic → `e.g.` footer row separated by a hairline border.
  - Equal-bottom alignment via `.card { min-height: 560px; display: flex; flex-direction: column }` + `.graphic { flex: 1 }` — works when the two graphics are different sizes (left = 3-step list, right = 3+2 logo tile grid).
  - Logo tiles use `object-fit: contain` on the `<img>` so mixed-aspect-ratio logos (Gmail 4:3, Slack 1:1) don't squish.
  - Use when comparing two named *types* or *categories* with examples — the eyebrow carries the "this is one of two" framing.

- **`four-step-framework`** — N-step horizontal progression (4 cards in a row).
  Path: `~/Documents/_stv/_content/_SFC/sfc/2026/ai-education/four-step-framework/four-step-framework.html`
  - Header is title-first, eyebrow-below (h1 then `4-STEP FRAMEWORK` mono in accent). Inverts the default eyebrow-above order when the title is the main hook and the eyebrow is metadata.
  - Cards in a `1fr 1fr 1fr 1fr` grid with **explicit `height` on the grid** (470px) instead of letting `flex: 1` distribute remaining space — without this the cards float up and leave dead space at the bottom of the canvas.
  - Each card: white bg, 18px radius, 1px hairline border, mono step eyebrow (`STEP 1`) in accent, bold Manrope step label below.
  - Connector arrows (Heroicons `arrow-long-down`) use **stroke-width 2.75**, not the default 1.5 — at ~22–32px on-canvas the thin default reads as a render glitch.
  - Step 2 uses the **chat-thread bubble cluster** pattern:
    - Vertical `.thread` of alternating `.row.left` / `.row.right` flex rows, each with a fixed-width pill (`width: 72px; height: 22px; border-radius: 14px`).
    - Two colors map to two senders — pick one mapping and keep it consistent across all conversation graphics in the same brand context. (If a brand-system skill is loaded, see its composition reference for the specific sender→color mapping; e.g. `aba-brand-system/references/infographic-composition.md` defines ABA's coral=AI / Cerulean=user pairing.)
    - Pills contain three small white dots (5px circles, 4px gap) to read as "a message" without committing to text content.
    - One bubble per row to keep the thread reading top-to-bottom; never stack bubbles diagonally — that scatters the eye.
    - Use whenever a graphic needs to *imply* a conversation without rendering legible text (e.g. "many messages distill into one document").
  - Use when the post is an ordered framework with N≤4 parallel steps and each step needs its own visual.

### Portrait (1080×1350)

- **`6-ways-claude-context`** — numbered vertical list.
  Path: `references/examples/6-ways-claude-context/6-ways-claude-context.html`
  - Title-only header. No eyebrow, no subtitle, no decorative pre-roll.
  - Six rows in a flex column with `gap: 18px`; each row is a `1.5px` border card.
  - Row grid: `70px 64px 1fr` = number (JetBrains Mono 32px Cerulean) / icon tile (`64x64` with `rgba(8,124,167,0.10)` fill + Heroicons-style inline SVG) / text block (Manrope 800 32px heading + Libre Franklin 20px desc).
  - Canvas uses `justify-content: center` with symmetric 80px top/bottom padding so the content sits balanced.
  - Use when the post is a numbered list of N≤6 with parallel structure (each item is one method/tactic/option).
  - No `assets/` folder — all icons are inline SVG.

- **`non-coding-skills`** — icon-led vertical card list (7 items), sized to fill the frame.
  Path: `references/examples/non-coding-skills/non-coding-skills.html`
  - Title-only header (Manrope 800, 72px), then 7 cards in a flex column, `gap: 16px`, each a 20px-radius hairline-border card. No number column (unlike `6-ways-claude-context`) — the icon leads.
  - Card row: `92px` icon tile (`rgba(1,4,19,0.04)` fill + hairline) + text block (Manrope 700 42px name, JetBrains Mono 23px accent handle inline, Libre Franklin 28px desc).
  - Icon tiles mix inline Heroicons (in the accent) with brand-logo `<img>`s using `object-fit: contain` — so a Heroicon and a Keynote/YouTube logo sit at consistent size in the same tile.
  - **Frame-fill sizing:** scaled type/tiles up and sized the canvas to *measured* content (~1080×1555) instead of a fixed 1350; footer sits in normal flow (no `margin-top: auto`). See SKILL.md § "Composition principles — Fill the frame" and § "Iterative height tuning for tall composites."
  - Use for a flat catalog/list of N items (tools, skills, features) where each item is one icon + name + one-line description and order doesn't imply sequence.

### Square (1080×1080)

- **`youtube-mcp`** — wordless two-mark connection graphic (the canonical bare social graphic).
  Path: `references/examples/youtube-mcp/youtube-mcp.html`
  - Claude mark and YouTube mark, a dotted Cerulean line, a solid Cerulean disc with a Heroicons link icon at the midpoint. No title, caption, or footer: the LinkedIn post copy carries the hook.
  - **White panel behind the composition.** A 960×520 `#FFFFFF` card (hairline border, 40px radius) centered on the cream canvas. Without it the composition floated in undifferentiated cream; with it the margin reads as deliberate. Same principle as SKILL.md § "Cream reads as warm only against white."
  - **Optical weight, not equal pixels.** The Claude starburst is set at 300px and the YouTube slab at 252px; the starburst is visually lighter, so equal boxes made it read smaller.
  - **Exact-spacing dotted connector.** An SVG `<line>` with `pathLength="5"`, `stroke-dasharray="0 1"`, `stroke-linecap="round"`, `stroke-width="7"` gives six evenly spaced round dots whose endpoints land exactly on the line ends, independent of the line's pixel length. CSS `border: dotted` can't do that.
  - Flex row (`mark · dots · badge · dots · mark`) centered in the panel, so nothing is absolutely positioned and the composition recenters if a mark is resized.
  - Chosen out of ~17 explored mockups via the fan-out workflow (SKILL.md § Ideating from scratch).

### Composite cheatsheet (tall portrait, 1080×~2000)

- **`claude-skill-cheatsheet`** — multi-section educational summary bundling several standalone topics into one shareable artifact.
  Path: `references/examples/claude-skill-cheatsheet/claude-skill-cheatsheet.html`
  - Title-only header (Manrope 800, large) + one-line subtitle + 3px cerulean rule. No eyebrow.
  - Multiple labeled sections stacked vertically with `gap: 36px`; each section is a `.section` flex column with its own `.section-title` (Manrope 800, 28px) and a card group below.
  - Each section reuses the markup from an existing standalone graphic (Chat/Cowork/Code triplet, Connectors vs Skills two-card, 3 types of skills, 4-step loop, 6 ways grid). Copy from the source HTMLs rather than re-authoring, and namespace classes by section (`.s1-card`, `.s2-card`, etc.) to avoid collisions.
  - **Footer auto-positioning:** `html, body { min-height: 100vh }` + `.canvas { min-height: 100vh; display: flex; flex-direction: column }` + `.footer { margin-top: auto }` + canvas `padding-bottom: 28px` anchors the footer to the lower third regardless of canvas height. Footer text defaults to `@shawhintalebi`; brand-system skills may override (e.g. `aba-brand-system` uses `aibuilder.academy`).
  - **Surface-state pill pattern** (used in the 6-ways grid) — small per-row mono pills showing which of N surfaces a method works on. Three states with semantic styling:
    - **On:** filled pill in the surface's accent color (chat=cerulean, cowork=coral, code=slate). One color per surface — pills read as a legend without needing one.
    - **Partial:** transparent bg with 1px outline in the same color (when a feature exists but is limited on that surface).
    - **Off:** muted gray fill, no strikethrough. Strikethrough reads as "removed" and feels aggressive; muted reads as "not applicable."
    Reusable for any "X works on Y" availability matrix without resorting to a full grid.
  - **Section-flow notes:** every card uses `1.5px solid var(--border)` with `border-radius` 14–22px depending on density. Card edges *are* the section breaks — no decorative dividers between sections.
  - Use when the brief is a "cheatsheet," "guide," or "everything-you-need" piece summarizing 3–6 topics already proven as individual graphics. See SKILL.md § "What this skill is for — Recognized exception" for when composite cheatsheets justify the multi-idea format.

## Embedded graphic

Figures that live inside a blog post, slide, or doc. Bare diagram, no social packaging (no title/subtitle/takeaway/footer by default), canvas sized tight to content. See `references/modes/embedded-graphic.md`.

### Horizontal flow / pipeline

- **`prompt-injection-pipeline`** — left-to-right cause-and-effect flow (the canonical embedded-mode example).
  Path: `references/examples/prompt-injection-pipeline/prompt-injection-pipeline.html`
  - Three columns connected by labeled arrows: a "what X can see" source card → a centered subject node (Claude logo in a `118px` disc) → a "what X can do" action list. Layout is `.flow { display: flex; align-items: center; justify-content: space-between }` with fixed-width `.col-source` / `.col-claude` / `.col-actions` and slim `.col-arrow` columns between them.
  - **Connector arrows** are Heroicons `arrow-right` at `stroke-width: 2.75` with a mono caption beneath each (`reads` / `acts`) — the two arrows carry the two-condition logic.
  - **`.action` rows** = icon chip (`42px` rounded, hairline) + verb. Built-in capabilities use inline Heroicons (folder, globe); a real connector uses its brand logo (`gmail.png`). The mix reads as "built-in vs connector" without a legend.
  - **`.action.contained`** is the highlighted/focal row: accent border + faint accent tint + a two-line text block (verb + a mono sub-note with a lock icon, e.g. "Drafts it, cannot send"). Use to single out one row as the resolved outcome.
  - **Malicious-instruction callout** (`.mal`): a tinted, bordered block in a semantic danger color (cardinal red `#B80C09`) embedded among grey skeleton-text bars in a browser-card, so the injected line reads as hidden-in-content.
  - **Two semantic colors** coexist (danger red for the malicious line, cerulean for the contained-safe outcome) plus a brand logo's native color — allowed because each carries meaning, not decoration.
  - Title was added at the user's explicit request (centered Manrope 800); it is NOT a default for embedded figures.
  - Content-fit canvas: `width: 1080px`, no fixed height, `~56px 60px 34px` padding; rendered tall then trimmed (final ~1080×512).
  - Use for any "input → actor → output" or "A causes B causes C" idea where the arrows themselves carry meaning.

### Two-zone comparison

- **`roles-and-groups`** — two labeled zones side by side.
  Path: `references/examples/roles-and-groups/roles-and-groups.html`
  - `.columns { display: flex }` with a fixed-width left zone (`flex: 0 0 452px`) and a flexible right zone (`flex: 1; min-width: 0`), each under a Manrope 800 zone heading.
  - Left zone stacks labeled chip groups (mono `DEFAULTS` / `CUSTOM ROLES` captions + permission cards with check/x rows); right zone holds two parallel `rounded-2xl` group cards with assigned-role chips and a status line.
  - **One accent (cerulean) used semantically** as a single thread — the same accent marks the granting role chip, the granted-permission checks, and the "on" status — so it functions as a key without a legend.
  - **Centered summary note** (`.note`, mono, muted) under the right zone states the rule the diagram teaches.
  - Content-fit canvas: `width: 1080px`, no fixed height, rendered tall then trimmed (final ~1080×560).
  - Use to contrast two related structures (categories, before/after, two configurations) where each side is a labeled container of items.

### Before / after workflow contrast

- **`demo-discovery-call`** — the same job done by hand vs. by the agent, as a 50/50 split. Built for a Keynote slide (1920×1080, white, no title of its own beyond the slide's).
  Path: `references/examples/demo-discovery-call/demo-discovery-call.html`
  - **The silhouette is the argument.** Left is 17 uniform grey checkbox rows (`height: 44px`, `#F4F6F7` on a hairline border, muted `#69787F`); right is five calm colored blocks. It lands before a word is read. This is the case where text volume is doing *visual* work — see SKILL.md § "Separate text doing visual work from text apologizing for the visual" — so the row count survives compression, and vertical room comes out of padding and type, never out of dropping rows.
  - **Right column = an ink spine with cards branching off it** at the moment each is produced. `.drops` holds an absolutely-positioned `.rail` (3px) plus a `.railtip` triangle; each `.drop` draws its own connector via `:before` (a 3px bar) and `:after` (a CSS triangle arrowhead), so branches need no SVG and reflow automatically.
  - **A rotated bracket labels a group without spending a row.** `.bracket .lab { writing-mode: vertical-rl; transform: rotate(180deg) }` beside a 3px bar, sized by a small `getBoundingClientRect` pass to span exactly the cards it names. Because the bracket names the group, the individual cards carry no repeating tag — that pairing is the text-economy principle in practice.
  - **Component color is consistent with the deck it lives in:** coral = automation/trigger, goldenrod = instructions (SOP + skill chips), cerulean = connectors, forest = records, ink = outputs and the human. Right-edge tags (`UPDATED` / `CREATED` / `DRAFT ONLY`) carry state the color can't.
  - **The human block closes it.** A dark full-width card ending on what the person still does keeps the claim honest — nothing in the graphic implies the agent acts unsupervised.
  - Siblings `demo2` / `demo3` swap the coral bolt for a clock plus a mono time chip (scheduled rather than event-triggered) and re-label the bracket for records *read* rather than written; all three are emitted from one generator so they can't drift.
  - Use for "manual vs. automated", "before vs. after", or any contrast where one side's tedium is the point.

### Comparison matrix / table

- **`cowork-control-matrix`** — N capabilities × several labeled dimensions, as a table on a white card.
  Path: `references/examples/cowork-control-matrix/cowork-control-matrix.html`
  - **White `--surface` card on the cream canvas** (`.card { background: var(--surface); border: 1.5px solid var(--hair); border-radius: 24px; overflow: hidden }`). The `overflow: hidden` clips the row tints to the rounded corners; the cream canvas shows as a margin so the background reads as warm, not white. See SKILL.md § "Type & color — Cream reads as warm only against white."
  - `table-layout: fixed` + a `<colgroup>` of fixed column widths. Header row = column *roles* (JetBrains Mono, uppercase, `--ink-muted`), color-coded per column: risk = coral `--risk #EE6352`, direct control = cerulean `--accent #087CA7`.
  - Each row's first cell = `50px` icon tile (accent-tinted) + Manrope name; body cells get alternating `--surface-alt` row tint + a hairline bottom border. The risk column's text is coral, the direct-control column's is cerulean — the column color *is* the legend.
  - **Stacked column sub-labels** (`DIRECT CONTROL` over `(admin sets)`, `INDIRECT CONTROL` over `(policy)`) use `text-indent: -0.2em` so the mono `(` aligns under the heading rather than looking inset. See SKILL.md § "Gotchas" #12.
  - **Brand logo in a monochrome set:** the Chrome row uses the single-path simpleicons `chrome.svg` with `fill="currentColor"`, tinted to the accent, sitting in an icon tile beside Heroicons — not a full-color PNG. See SKILL.md § "Icons."
  - **Two semantic colors** (risk coral vs. control cerulean) coexist — the allowed semantic-role exception, a danger/safe key, not decoration.
  - Content-fit canvas: `width: 1640px` (wide table figure), no fixed height, measured then rendered (final ~1640×1112 logical).
  - Use when comparing N items across several labeled dimensions — a capability / decision / responsibility matrix.
