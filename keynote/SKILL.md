---
name: keynote
description: Read, create, and modify Apple Keynote (.key) presentations. Use when the user asks about .key files, wants summaries, needs to understand slide content, or wants to create/edit decks.
user_invocable: true
---

# keynote

Work with Apple Keynote (.key) presentations: extract text, export images, create new decks, add slides, set text, and populate entire decks from JSON.

## Usage

`$ARGUMENTS` is a file path, glob pattern, or instruction. If empty, default to all `.key` files in the current working directory.

## Scripts

### Read-only (any `.key` file)

- **extract-text** — get slide text, titles, and presenter notes:
  ```
  osascript .claude/skills/keynote/scripts/extract-text.applescript "<absolute-path>"
  ```

- **export-images** — export slides as PNGs:
  ```
  osascript .claude/skills/keynote/scripts/export-images.applescript "<absolute-path>" "./.claude/keynote/images/<name>"
  ```

### Write (.claude/keynote directory only)

- **create-deck** — create a new Keynote file using the talk-basic theme:
  ```
  osascript .claude/skills/keynote/scripts/create-deck.applescript "<absolute-path-in-.claude/keynote>"
  ```

- **delete-slides** — remove slides by number/range:
  ```
  osascript .claude/skills/keynote/scripts/delete-slides.applescript "<absolute-path-in-.claude/keynote>" "<slide-spec>"
  ```
  `<slide-spec>` accepts comma-separated numbers and ranges: `"3,5,10-15,20"`

- **add-slides** — append slides with a specific master layout:
  ```
  osascript .claude/skills/keynote/scripts/add-slides.applescript "<deck-path>" "<master-name>" <count>
  ```
  Example: `osascript .claude/skills/keynote/scripts/add-slides.applescript "./.claude/keynote/deck.key" "Title Only" 5`

- **set-slide-text** — set title, subtitle, and body on a single slide:
  ```
  osascript .claude/skills/keynote/scripts/set-slide-text.applescript "<deck-path>" <slide-number> "<title>" "<subtitle>" "<body>"
  ```
  Pass `""` for unused fields. For Title layout, `<body>` sets the footer/author field. For Title Only layout, `<body>` creates a freeform text box below the subtitle.

- **populate-deck** — create and populate an entire deck from a JSON file:
  ```
  osascript .claude/skills/keynote/scripts/populate-deck.applescript "<deck-path>" "<slides.json>"
  ```
  Slide 1 is reused for the first JSON entry; additional slides are appended. Processes in batches of 5 to avoid timeouts.

## Populating slides

### Text item mapping (talk-basic theme)

| Layout | text item 1 | text item 2 | text item 3+ |
|--------|------------|------------|-------------|
| **Title** | footer/author (y=934) | big title (y=203) | subtitle (y=569) |
| **Section** | center text (y=357) | — | — |
| **Title Only** | title (y=85) | subtitle (y=187) | — (no body placeholder) |
| **Blank** | — | — | — |

The scripts detect which layout a slide uses by checking the y-position of text item 1:
- `> 900` → Title layout
- `> 300` → Section layout
- `< 200` → Title Only layout
- No text items → Blank layout

Each layout has duplicate/extra text items (items 4+) that are ignored. Item at y=1030 is a logo/watermark placeholder.

**Body text on Title Only slides**: Since there is no body placeholder, body content is injected via `make new text item` as a freeform text box positioned at y=300. These are starting points for manual editing.

### Body text formatting

Each newline in the body field becomes a separate bullet point. Use `\n` (literal newline) to separate bullets in JSON:
```json
{"body": "First bullet\nSecond bullet\nThird bullet"}
```

For a subtitle line without a bullet (on Title Only), use the `subtitle` field, not the `body` field.

### JSON format for populate-deck

```json
[
  {"master": "Title", "title": "Deck Title", "subtitle": "A subtitle", "body": "", "author": "Shaw Talebi"},
  {"master": "Title Only", "title": "Slide Title", "subtitle": "Lead-in line", "body": "Bullet 1\nBullet 2\nBullet 3"},
  {"master": "Section", "title": "Section Name"},
  {"master": "Blank"}
]
```

### Available master layouts (talk-basic theme)

Title, Section, Title Only, Blank

## Creating a deck from scratch

1. **Plan content** — outline slides with titles, subtitles, and bullet points
2. **Write JSON** — create a `slides.json` file following the format above
3. **Create deck** — `osascript .claude/skills/keynote/scripts/create-deck.applescript "./.claude/keynote/deck.key"`
4. **Populate** — `osascript .claude/skills/keynote/scripts/populate-deck.applescript "./.claude/keynote/deck.key" "./.claude/keynote/slides.json"`
5. **Verify** — extract text and export images to confirm content placement
6. **Iterate** — use `set-slide-text` to fix individual slides, or `delete-slides` + `add-slides` to restructure

## Safety

Scripts that modify files enforce a `.claude/keynote` directory constraint — they refuse to run if the target path does not contain ".claude/keynote". Read-only scripts (`extract-text`, `export-images`) can operate on any `.key` file.

## Output directory

Save all outputs to `./.claude/keynote/` in the current working directory. Before writing any output, run `mkdir -p ./.claude/keynote/images`.

- **Images**: `./.claude/keynote/images/<presentation-name>/`
- **New decks**: `./.claude/keynote/`
- **Text extractions or summaries**: `./.claude/keynote/`
- **JSON slide data**: `./.claude/keynote/`

## Style Guide

When creating new presentations, first read `.claude/skills/keynote/shaw-style-guide.md`. Follow the visual design, narrative structure, and content patterns described there to match Shaw's established presentation style.

## Common pitfalls

- **-1700 errors**: Avoid referencing `slide N of doc` immediately after creation in the same tell block. Use direct references from `make new slide` or operate in a separate open/save/close cycle.
- **AppleEvent timeouts (-1712)**: Never populate more than ~5 slides per open/save/close cycle. The `populate-deck` script handles this automatically.
- **Wrong text field**: Always check which layout a slide uses before setting text. Title layout has the title at item 2; Title Only has it at item 1.

## Notes

- Keynote must be installed on the system
- The AppleScripts open and close documents in Keynote automatically
- For large presentations, text extraction is usually sufficient; only export images when visuals matter
- The `populate-deck` script requires Python 3 (for JSON parsing)
