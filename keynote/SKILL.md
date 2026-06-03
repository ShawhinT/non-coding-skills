---
name: keynote
description: Read, create, and modify Apple Keynote (.key) presentations. Use when the user asks about .key files, wants summaries, needs to understand slide content, or wants to create/edit decks.
user_invocable: true
---

# keynote

Work with Apple Keynote (.key) presentations: extract text, export images, create new decks, add slides, set text, populate entire decks from JSON, and insert images (incl. assets fetched from the web).

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
  osascript .claude/skills/keynote/scripts/export-images.applescript "<absolute-deck-path>" "<absolute-output-dir>"
  ```
  Both paths must be **absolute** — a relative output dir (e.g. `./.keynote-skill/images/<name>`) fails with "could not be interpreted as a file URL". Use `"$(pwd)/.keynote-skill/images/<name>"`.

### Write (any `.key` file — automatic backups)

All write scripts back up the deck to `<deck-dir>/.keynote-skill/backups/<deck-name>.<timestamp>.key` before modifying, then prune so only the **3 most recent** backups per deck remain. The deck itself can live anywhere — you can collaborate directly on the user's working file.

**All scripts (read-only and write) leave the deck open in Keynote by default** so the user sees results immediately and isn't disrupted if they were already working on it. Pass `--close` as the last argument to close the deck after the operation (useful for batch scripting or when you want a clean state).

**Auto-save before edit:** every script first calls `saveIfOpen` — if Keynote currently has the target deck open, the script saves it before proceeding. This commits any unsaved user edits to disk *before* the backup runs, so the backup captures their latest work and the script's own save doesn't clobber pending changes. No need to ask the user to save first.

- **create-deck** — create a new Keynote file using the talk-basic theme. Refuses to overwrite an existing file:
  ```
  osascript .claude/skills/keynote/scripts/create-deck.applescript "<absolute-path>"
  ```

- **delete-slides** — remove slides by number/range:
  ```
  osascript .claude/skills/keynote/scripts/delete-slides.applescript "<deck-path>" "<slide-spec>"
  ```
  `<slide-spec>` accepts comma-separated numbers and ranges: `"3,5,10-15,20"`

- **add-slides** — append slides with a specific master layout:
  ```
  osascript .claude/skills/keynote/scripts/add-slides.applescript "<deck-path>" "<master-name>" <count>
  ```

- **set-slide-text** — set title, subtitle, and body on a single slide:
  ```
  osascript .claude/skills/keynote/scripts/set-slide-text.applescript "<deck-path>" <slide-number> "<title>" "<subtitle>" "<body>"
  ```
  Pass `""` for unused fields. For Title layout, `<body>` sets the footer/author field. For Title Only layout, `<body>` creates a freeform text box below the subtitle.

- **populate-deck** — populate an entire deck from a JSON file. **Destructive**: refuses to run on a deck with >1 slide unless `--force` is passed (the user's edits would be clobbered):
  ```
  osascript .claude/skills/keynote/scripts/populate-deck.applescript "<deck-path>" "<slides.json>" [--force]
  ```
  Slide 1 is reused for the first JSON entry; additional slides are appended. Processes in batches of 5 to avoid timeouts. **Prefer `set-slide-text` + `add-slides` for incremental edits** — only use `populate-deck` to build a deck from scratch.

- **insert-image** — insert an image (PNG/JPEG/etc) onto a slide:
  ```
  osascript .claude/skills/keynote/scripts/insert-image.applescript "<deck-path>" <slide-number> "<image-path>" "<position>" [width]
  ```
  `<position>` accepts named keywords (`bottom-right`, `bottom-left`, `top-right`, `top-left`, `center`) or explicit `"x,y"` (canvas is 1920×1080). `[width]` defaults to 500; height auto-scales by aspect ratio.

- **add-text-box** — add a freeform text box anywhere on a slide (custom position, font, size):
  ```
  osascript .claude/skills/keynote/scripts/add-text-box.applescript "<deck-path>" <slide-number> "<text>" "<position>" [width] [font] [size]
  ```
  Use this for any standalone text box that isn't one of the layout's title/subtitle/body placeholders — e.g. labels, data cards, callouts, replacing a deleted image with text. `<position>` accepts the same named keywords as `insert-image` or explicit `"x,y"`. Use `\n` (literal backslash-n) in `<text>` to separate lines — each becomes its own line in one box. `[width]` defaults to 560, `[size]` to 32; `[font]` (PostScript name like `Menlo-Bold`) is optional — omit to keep the theme default. **Prefer this over hand-rolling AppleScript** — it bakes in the one creation pattern that actually works (see pitfalls: text items must be made inside a `tell <slide>` block with a `height` property, or you get `-10000`).

## Fetching assets from the web

When asked to add a logo, screenshot, or other image to a slide:

1. **Find a source** — good defaults:
   - Logos: Wikimedia Commons, [brandfetch.com](https://brandfetch.com)
   - Icons: simpleicons.org, icons8.com
   - Use `WebSearch` then `WebFetch` to get the direct asset URL.

2. **Download to assets dir**:
   ```bash
   mkdir -p ./.keynote-skill/assets
   curl -sL -A "Mozilla/5.0" "<asset-url>" -o "./.keynote-skill/assets/<name>.png"
   ```
   The `User-Agent` header matters — Wikimedia and others 403 default `curl` UAs.

3. **Verify** with `file ./.keynote-skill/assets/<name>.png` — should report `PNG image data` (not `HTML document` — a sign the URL returned an error page).

4. **Insert** via the `insert-image` script.

**Tips:**
- Prefer PNG over SVG. Keynote handles PNG more reliably.
- Wikimedia hosts pre-rendered PNGs for any SVG: replace `commons/X/XX/Foo.svg` with `commons/thumb/X/XX/Foo.svg/<width>px-Foo.svg.png`.
- Keep transparent backgrounds for logos so they sit cleanly on the white deck.
- **Default to the color variant.** Prefer branded logos in their natural colors — Keynote can't recolor a flat PNG, so a monochrome icon is stuck monochrome. On lobehub the convention is `<name>-color.png` (e.g. `claude-color`, `gemini-color`, `antigravity-color`). For brands whose default icon is already colored (e.g. `openai`), the base name works. Try the `-color` variant first; fall back to the monochrome only if no color variant exists.
- **Light vs. dark monochrome (when no color variant):** a black-on-transparent logo disappears on a white slide, and white-on-transparent disappears on a dark deck. The default talk-basic theme is white, so use the **light** variant (dark icon). Always preview the PNG before inserting — if it looks blank, you've grabbed the wrong variant.
- **Wikimedia requires a descriptive User-Agent.** Generic `curl` and `Mozilla/5.0` UAs get HTTP 400. Use a UA with contact info, e.g. `curl -A "LogoFetcher/1.0 (shawhintalebi@gmail.com)" ...`.
- **Wikimedia thumb widths are restricted.** Only these widths work: **20, 40, 60, 120, 250, 330, 500, 960, 1280, 1920, 3840 px**. Arbitrary widths (600, 800) return HTTP 400 with a "use thumbnail steps" message. Pick **500** or **960** for typical logo use.
- **lobehub CDN is for AI brand logos**, not programming languages or generic apps: `https://unpkg.com/@lobehub/icons-static-png@latest/light/<name>.png`. Append `-color` for the color variant. Doesn't have python/javascript/ruby/java/cpp/html/word/excel/etc — those come from Wikimedia.
- **For desktop app icons, check `/Applications/` first.** When you want the icon "as shown on the desktop app" (purple-gradient Codex, Claude, etc.), the real icon lives at `/Applications/<App>.app/Contents/Resources/icon.icns` (sometimes `AppIcon.icns`). Convert with `sips -s format png <path>.icns --out ./.keynote-skill/assets/<name>-app-icon.png`. This is faster than web search and returns the actual shipping icon — branded marketing logos on the web are often different from the app icon (e.g. Codex ships a black wordmark logo *and* a purple gradient app icon; only the latter is in `Codex.app`).

## Speeding up videos before insertion

Keynote's Movie inspector exposes only volume, trim, poster frame, and repeat — there's no playback-speed slider. To present a screen recording faster, pre-process it:

```
.claude/skills/keynote/scripts/speed-up-video.sh <input> <speed> [output]
```
Wraps `ffmpeg` with `setpts` for video and chained `atempo` filters for audio (preserves pitch at any speed). Default output is `<input-stem>.<speed>x.<ext>` next to the input. Replace the original movie in the slide via the Movie inspector's **Replace** button.

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
  {"master": "Title", "title": "Deck Title", "subtitle": "A subtitle", "body": "", "author": "Your Name"},
  {"master": "Title Only", "title": "Slide Title", "subtitle": "Lead-in line", "body": "Bullet 1\nBullet 2\nBullet 3"},
  {"master": "Blank"}
]
```

### Available master layouts (talk-basic theme)

Title, Section, Title Only, Blank

## Creating a deck from scratch

1. **Plan content** — one slide per major outline bullet. Sub-bullets become on-slide content (subtitle, body), not separate slides. Default to Title Only layout.
2. **Write JSON** — create a `slides.json` file following the format above
3. **Create deck** — `osascript .../create-deck.applescript "<deck-path>"`
4. **Populate** — `osascript .../populate-deck.applescript "<deck-path>" "<slides.json>"`
5. **Verify** — extract text and export images to confirm content placement
6. **Iterate** — use `set-slide-text` / `add-slides` / `delete-slides` / `insert-image` to make targeted edits. **Do not re-run `populate-deck`** on an in-progress deck — it refuses by default and even `--force` discards user edits.

## Safety

- Write scripts automatically back up the deck to `<deck-dir>/.keynote-skill/backups/` before modifying. Read-only scripts (`extract-text`, `export-images`) make no backup.
- `create-deck` refuses to overwrite an existing file.
- `populate-deck` refuses to run on a deck with >1 slide without `--force`. This is the only destructive script — when in doubt, use the additive scripts instead.
- If the user has the deck open in Keynote, the AppleScripts will close and reopen it; warn before running if they may have unsaved changes.

## Output directory

- **Backups**: `<deck-dir>/.keynote-skill/backups/` (auto-created by write scripts)
- **Fetched assets**: `./.keynote-skill/assets/`
- **Image exports**: `./.keynote-skill/images/<presentation-name>/`
- **JSON slide data, scratch decks**: `./.keynote-skill/`

Run `mkdir -p ./.keynote-skill/images ./.keynote-skill/assets` before writing outputs.

## Style Guide

When creating new presentations, first read `.claude/skills/keynote/style-guide.md`. Follow the visual design, narrative structure, and content patterns described there to match your established presentation style.

## Shared helpers

Common boilerplate (path resolution, `--close` parsing, save-if-open, backup) lives in `scripts/_helpers.applescript`. Each script loads the **compiled** version (`_helpers.scpt`) at runtime via `load script`, since AppleScript's `load script` only accepts compiled `.scpt`, not raw source.

**If you edit `_helpers.applescript`, recompile it:**
```
osacompile -o scripts/_helpers.scpt scripts/_helpers.applescript
```
Both files should be checked in. The `.applescript` is the source of truth for reading/editing; the `.scpt` is what the scripts actually load.

Exported handlers:
- `resolvePath(p)` — relative or absolute path → fully resolved absolute path
- `parseCloseFlag(argv)` — true if argv contains `--close`
- `saveIfOpen(filePath)` — saves the deck if Keynote currently has it open (commits user's unsaved edits before backup/edit)
- `backupDeck(filePath)` — copies the deck to `<deck-dir>/.keynote-skill/backups/<name>.<timestamp>.key`, then prunes so only the 3 most recent backups for that deck remain

## Common pitfalls

- **-1700 errors**: Avoid referencing `slide N of doc` immediately after creation in the same tell block. Use direct references from `make new slide` or operate in a separate open/save/close cycle.
- **AppleEvent timeouts (-1712)**: Never populate more than ~5 slides per open/save/close cycle. The `populate-deck` script handles this automatically.
- **Wrong text field**: Always check which layout a slide uses before setting text. Title layout has the title at item 2; Title Only has it at item 1.
- **Image corruption**: When inserting images via raw AppleScript, always pass `width` (and `position`/`file`) as **creation properties** to `make new image`. Setting `width` or `height` *after* the image is created has been observed to corrupt the .key file. The `insert-image` script handles this correctly.
- **`-10000` creating a text box**: A new text item must be created **inside a `tell <slide>` block** with `make new text item with properties {object text:…, position:…, width:…, height:…}` — the `height` property is required. Using `make new text item at end of slide`, or omitting `height`, throws `AppleEvent handler failed (-10000)`. This is a creation-structure problem, **not** a special-character/Unicode issue — don't waste time stripping `°`/arrows/etc. Set `font`/`size` on `object text` *after* creation. The `add-text-box` script encapsulates the working pattern, so reach for it instead of hand-rolling.
- **`text items` shadowing inside Keynote `tell` blocks**: Inside `tell application "Keynote"`, the term `text items` refers to slide text-item objects, not string parts. If you parse comma-separated args (e.g. `"180,550"`) by setting `AppleScript's text item delimiters` and reading `text items of <string>`, do it **outside** the Keynote tell block — otherwise you'll get error -1728 ("Can't get every text item of '180,550'"). Same applies to any keyword that overlaps Keynote's vocabulary.
- **Don't rebuild from JSON to fix one slide**: If the user has edited the deck, `populate-deck` will wipe their changes. Use `set-slide-text` for text fixes and `insert-image` for adding visuals.

## Notes

- Keynote must be installed on the system
- The AppleScripts open and close documents in Keynote automatically
- For large presentations, text extraction is usually sufficient; only export images when visuals matter
- The `populate-deck` script requires Python 3 (for JSON parsing)
