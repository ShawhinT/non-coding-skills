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
  osascript .claude/skills/keynote/scripts/extract-text.applescript "<absolute-path>" [--positions]
  ```
  `--positions` prefixes each line with the text item's `{x, y}` and width. Reach for it whenever you're **editing an existing deck rather than reading one** — matching an established layout requires knowing where things already sit, and the alternative is hand-rolling AppleScript that trips the `text items` shadowing pitfall below. It's how you find the y-coordinate of a repeating row (e.g. a before/after band), confirm a citation marker landed at `{95, 1027}`, or spot a duplicated box that still holds placeholder text.

- **export-images** — export slides as PNGs:
  ```
  osascript .claude/skills/keynote/scripts/export-images.applescript "<absolute-deck-path>" "<absolute-output-dir>" [--all-stages]
  ```
  `--all-stages` emits one PNG per build stage (every animation step) instead of one per slide — what you need to rebuild a talk's slide track synced to a recording (video-editor's `references/recreated-slides.md`). Stage files are numbered sequentially across the deck, so map them back to slides from a contact sheet. Embedded movies aren't in the export; pull them from the `.key` zip's `Data/` folder (`unzip -l deck.key | grep -E 'mp4|mov'`).
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

- **set-notes** — set the presenter notes on a single slide:
  ```
  osascript .claude/skills/keynote/scripts/set-notes.applescript "<deck-path>" <slide-number> "<note-text>"
  ```
  Pass the note from the shell as an ANSI-C string (`$'line 1\nline 2'`) to get real line breaks — each line becomes its own line in the presenter notes, so a leading `• ` per line renders as a bullet list. `extract-text` reads notes back (it prints a `Notes:` line whenever a slide has one), so use it to verify. **Prefer this over hand-rolling `set presenter notes of slide N`** — it bakes in the same save-if-open + backup safety as the other write scripts.

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
- **Rendering a Wikimedia SVG to PNG — prefer `Special:FilePath`.** `https://commons.wikimedia.org/wiki/Special:FilePath/<Filename>?width=500` renders any Commons SVG to a PNG at an arbitrary width — no need to know the file's hash directory, and it sidesteps the restricted-width gotcha below. URL-encode the filename (spaces → `%20`, parens → `%28`/`%29`), e.g. `Special:FilePath/Google_Calendar_icon_%282020%29.svg?width=500`. Constructing the thumb URL by hand (`commons/thumb/X/XX/Foo.svg/<width>px-Foo.svg.png`) still works but is the fallback — you have to look up the hash path and honor the fixed width steps.
- Keep transparent backgrounds for logos so they sit cleanly on the white deck.
- **Default to the color variant.** Branded logos read best in their natural colors — Keynote can't recolor a flat PNG, so a monochrome icon is stuck monochrome. On lobehub the convention is `<name>-color.png` (e.g. `claude-color`, `gemini-color`, `antigravity-color`). For brands whose default icon is already colored (e.g. `openai`), the base name works. Try the `-color` variant first; fall back to the monochrome only if no color variant exists.
- **Light vs. dark monochrome (when no color variant):** a black-on-transparent logo disappears on a white slide, and white-on-transparent disappears on a dark deck. The default talk-basic theme is white, so use the **light** variant (dark icon). Always preview the PNG before inserting — if it looks blank, you've grabbed the wrong variant.
- **Wikimedia requires a descriptive User-Agent.** Generic `curl` and `Mozilla/5.0` UAs get HTTP 400. Use a UA with contact info, e.g. `curl -A "LogoFetcher/1.0 (shawhintalebi@gmail.com)" ...`.
- **Wikimedia thumb widths are restricted.** Only these widths work: **20, 40, 60, 120, 250, 330, 500, 960, 1280, 1920, 3840 px**. Arbitrary widths (600, 800) return HTTP 400 with a "use thumbnail steps" message. Pick **500** or **960** for typical logo use.
- **lobehub CDN is for AI brand logos**, not programming languages or generic apps: `https://unpkg.com/@lobehub/icons-static-png@latest/light/<name>.png`. Variants live **only** under `light/` and `dark/` — there is no top-level `color/` directory (requesting `.../color/<name>.png` returns a "Not found" text file, not a PNG). The color variant is `light/<name>-color.png` (e.g. `light/gemini-color.png`, `light/claude-color.png`); for brands with no color variant (e.g. `openai`) use `light/<name>.png` (monochrome dark icon, which reads fine on the white talk-basic theme). Doesn't have python/javascript/ruby/java/cpp/html/word/excel/etc — those come from Wikimedia.
- **For desktop app icons, check `/Applications/` first.** When you want the icon "as shown on the desktop app" (purple-gradient Codex, Claude, etc.), the real icon lives at `/Applications/<App>.app/Contents/Resources/icon.icns` (sometimes `AppIcon.icns`). Convert with `sips -s format png <path>.icns --out ./.keynote-skill/assets/<name>-app-icon.png`. This is faster than web search and returns the actual shipping icon — branded marketing logos on the web are often different from the app icon (e.g. Codex ships a black wordmark logo *and* a purple gradient app icon; only the latter is in `Codex.app`). This also covers Apple's own apps — Keynote, Final Cut Pro, etc. **Caveat:** many app icons (especially non-Apple apps like Chrome) are macOS **rounded-square tiles with an opaque white/gradient background**, not the bare icon-only mark. For a logo row on a white slide you usually want the transparent icon-only version — check the converted PNG, and if it's a tile, prefer Wikimedia/lobehub instead (e.g. Chrome's color wheel lives on Wikimedia; `/Applications/Google Chrome.app` is a white tile). The app-icon route is ideal for Apple apps and for brands whose desktop icon genuinely *is* the transparent mark (Codex, Claude).
- **When a brand is on neither lobehub nor icons8, use the favicon service.** `https://www.google.com/s2/favicons?domain=<domain>&sz=256` returns the brand's *own* site icon (colored, ~180–256 px, transparent) — authentic, not a third-party redraw. This is how Mux (`mux.com`), Kit (`kit.com`), and HubSpot (`hubspot.com`) were sourced. Preview it: some brands serve a square brand-colored tile (Mux's pink `M.`, Kit's blue `K`) rather than a bare glyph — that's their real app icon, so it's good.
- **Only good logos belong — a wordmark is a bad logo, not a fallback.** On a slide of tiles/columns you want the **icon-only** mark (the square symbol), colored, transparent. If the first file you find is a horizontal wordmark (name-as-text), that's the wrong asset — don't insert it and don't record its URL anywhere; find the icon instead. Wikimedia often only carries the wordmark for a brand (Jira, Confluence's base file); when it does, grab the icon from **icons8** (`https://img.icons8.com/color/480/<name>.png` — colored icon-only PNG, no UA tricks needed) or use the icon-only Commons file if one exists (e.g. Confluence's `...(cropped).svg`). Always preview before inserting.
- **Verified-good sources — check this table FIRST, before searching.** Each row below is a brand whose icon-only, colored, transparent asset has already been tracked down once, with the exact source that produced it. Fetch straight from the listed source into `./.keynote-skill/assets/` rather than re-searching. Use it as a sourcing template for similar brands too — the pattern that worked for one Wikimedia/icons8/favicon brand usually works for its neighbors. If you want the fetches to stop repeating across decks, keep your own local cache dir and `cp` from it.
  | Brand | File | Source |
  |---|---|---|
  | Claude | `claude.png` | lobehub `light/claude-color.png` |
  | Claude Code | `claude-code.png` | lobehub `light/claudecode-color.png` — note the name has **no hyphen** (`claudecode`); `claude-code` 404s |
  | Codex | `codex.png` | lobehub `light/codex-color.png` (purple-gradient app mark) — `Codex.app` is not in `/Applications` on this machine |
  | ChatGPT | `chatgpt.png` | lobehub `light/openai.png` (black knot, transparent) — `/Applications/ChatGPT.app` is a **white tile**, avoid it |
  | Cursor | `cursor.png` | lobehub `light/cursor.png` (black cube, transparent) — `/Applications/Cursor.app` is a **dark tile**, avoid it |
  | Google Meet | `google-meet.png` | Wikimedia `Google_Meet_icon_(2020).svg` |
  | Stripe | `stripe.png` | favicon service `stripe.com` (indigo #635BFF tile) |
  | Python | `python.png` | Wikimedia `Python-logo-notext.svg` — the `-notext` file is the icon-only two-snake mark; plain `Python-logo.svg` is the **wordmark** |
  | Resend | `resend.png` | simpleicons `cdn.simpleicons.org/resend/000000` → `qlmanage -t -s 480`; the favicon is only 114px and has a visible border |
  | Google Analytics (GA4) | `ga4.png` | simpleicons `cdn.simpleicons.org/googleanalytics` (brand orange #E37400 bar chart) → `qlmanage -t -s 480`. icons8 `google-analytics` is a **flat orange circle** redraw and Wikimedia's `Logo_Google_Analytics.svg` is a **wordmark** — both wrong |
  | MCP | `mcp.png` | lobehub `light/mcp.png` |
  | Gmail | `gmail.png` | Wikimedia `Gmail_icon_(2020).svg` |
  | Google Calendar | `google-calendar.png` | Wikimedia `Google_Calendar_icon_(2020).svg` |
  | Google Drive | `google-drive.png` | icons8 `google-drive` |
  | Slack | `slack.png` | Wikimedia `Slack_icon_2019.svg` |
  | Notion | `notion.png` | Wikimedia `Notion-logo.svg` (black by design) |
  | Obsidian | `obsidian.png` | Wikimedia `2023 Obsidian logo.svg` |
  | Confluence | `confluence.png` | Wikimedia `Atlassian Confluence 2017 logo (cropped).svg` — the **non**-cropped file is a wordmark |
  | Jira | `jira.png` | icons8 `jira` — Wikimedia only has wordmarks |
  | HubSpot | `hubspot.png` | favicon service `hubspot.com` |
  | YouTube | `youtube.png` | icons8 `youtube-play` |
  | Canva | `canva.png` | official teal→purple gradient badge (supplied directly) — icons8 `canva` and the favicon are an older **flat** teal, inferior |
  | Kit (formerly ConvertKit) | `kit.png` | favicon service `kit.com` (blue tile) |
  | Mux | `mux.png` | favicon service `mux.com` (pink tile) |
  | Railway | `railway.png` | lobehub `light/railway.png` — a train-in-circle mark (matches railway.app's own favicon; it is **not** an abstract geometric logo) |
  | Keynote | `keynote.png` | app icon, `/Applications/Keynote.app` |
  | Final Cut Pro | `finalcutpro.png` | app icon, `/Applications/Final Cut Pro.app` |
  | Chrome | `chrome.png` | Wikimedia `Google_Chrome_icon_(February_2022).svg` (icon-only color wheel) — the `/Applications` app icon is a **white tile**, avoid it |
  | git | `git.png` | Wikimedia `Git_icon.svg` (icon-only orange diamond) — `Git-logo.svg` is the **wordmark** version, avoid it |
  | Calendly | `calendly.png` | simpleicons `cdn.simpleicons.org/calendly` (brand-blue #006BFF icon-only "C"), rendered to 800px PNG via `qlmanage -t -s 800 -o . <file>.svg` — Wikimedia/icons8/lobehub/clearbit all had nothing usable, and the favicon service only served 48px |
  | Loopio | `loopio.png` | favicon service `loopio.com` (brand-teal icon-only "lo" mark, 256px transparent) — simpleicons has no `loopio` entry and returns an **empty file**, not a 404, so check `file` on the result |
  | PowerPoint | `powerpoint.png` | Wikimedia `Special:FilePath/Microsoft_Office_PowerPoint_%282019%E2%80%93present%29.svg?width=500` — note the filename's **en-dash** (`%E2%80%93`) in "2019–present"; a plain hyphen 404s |
  | Airspeed (formerly Glyphic) | `airspeed.png` | favicon of **glyphic.ai** (256px gradient "a" tile). `airspeed.ai`'s favicon is a GoDaddy parking placeholder, so after a rebrand try the old domain |
  | Word | `word.png` | Wikimedia `Special:FilePath/Microsoft_Office_Word_%282019%E2%80%93present%29.svg?width=500` — same en-dash filename pattern as PowerPoint (500×466, icon-only blue "W" tile) |
| Apollo.io | `apollo.png` | favicon service `apollo.io` (yellow tile, black sunburst mark, 256px) — lobehub has no `apollo` entry |

  Other brands sourced the same way and worth checking against the patterns above: `github`, `linkedin`, `playwright`, `assemblyai`. When you track down a new good logo, add a table row here so the next deck doesn't repeat the search.

  **Logos added to a slide go wherever the slide's structure says they belong.** A slide that contrasts two states with the same set of tools (e.g. "How do I do this?" vs. "How do I get Claude to do this?" icon clusters) implies each tool appears in both, so a new logo goes into every matching cluster, sized and spaced like its neighbours. Check the exported slide afterwards for crowding.
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

## What Keynote's AppleScript genuinely cannot do

Verified against `/Applications/Keynote.app/Contents/Resources/Keynote.sdef`. These are hard limits, not gaps in this skill. **When you hit one, say so plainly and hand the step back to the user — do not invent a workaround that mutates his deck.** He would rather do ten seconds of clicking than discover you rebuilt his title placeholders.

### No z-order control

There is no bring-to-front, send-to-back, arrange, or index property on any iWork item. **Newly created objects always land on top of everything already on the slide.**

The consequence that bites: `insert-image` with a full-bleed 1920×1080 image **will cover the slide's title and every other existing element.** The content is not lost, just buried.

Tell the user: *"the image is in, but Keynote's AppleScript can't send it behind the title — right-click the image and choose Arrange → Send to Back."* Then stop.

**Do NOT** "fix" this by blanking the title placeholder and re-adding the text with `add-text-box` so it stacks on top. It looks like it works, but it swaps a themed master placeholder for a loose text box, which silently breaks the deck's typography inheritance and any later master change. This exact mistake was made once; don't repeat it.

The only legitimate way to avoid the collision is to **not** cover the region in the first place: render the image so its content sits below the title band and insert it at a y-offset, leaving the title area untouched.

### No shape fill color

`background fill type` on `shape` and `text item` is **read-only** (`access="r"`), and it is an enum (`no fill` / `color fill` / `gradient fill` / `advanced gradient fill`), not a color value. There is no writable fill property anywhere in the dictionary. You cannot recolor a shape.

What *is* writable: `color` of `character`/`paragraph`/`text` (font color, as RGB 0–65535, e.g. `{65535, 0, 0}`), plus `opacity` and `rotation` on the item itself.

The tempting workaround also fails: `selection` on the document *is* read-write, so you can select a specific shape from AppleScript, but driving Keynote's own Copy Style (⌥⌘C) / Paste Style (⌥⌘V) through System Events dies with `osascript is not allowed to send keystrokes` unless the parent process has been granted Accessibility permission. Don't build on it.

So: **shape fills are a manual step.** Sample the existing fill from an exported PNG if you need to match it (`export-images`, then read the pixel), give the user the hex, and let them apply it.

### Reading geometry you cannot set

`extract-text --positions` covers text items. For shapes and images, read `position`, `width`, and `height` directly — but coerce numerics explicitly or you get `-1700`:

```applescript
set p to position of sh
set out to ((item 1 of p) as integer) & "," & ((item 2 of p) as integer)
```

## Safety

- Write scripts automatically back up the deck to `<deck-dir>/.keynote-skill/backups/` before modifying. Read-only scripts (`extract-text`, `export-images`) make no backup.
- **Hand-rolled AppleScript that mutates a deck does NOT get the automatic backup.** If you're deleting or replacing objects outside the provided scripts, `cp -R` the deck into `.keynote-skill/backups/` yourself first.
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

**Read `style-guide.md` (alongside this file in the skill dir) before styling any deck — new *or* existing — not only when building from scratch.** It carries exact specs for recurring elements (reference citation markers, footers, the title formula, pros/cons color). Adding or restyling one of those on a deck the user already has is exactly when the spec matters most: e.g. references are small bracketed markers in the **bottom-left**, flush to the page-number footer line at a fixed position/font — *not* superscripts next to the subtitle. Reaching for a "reasonable-looking" placement instead of the documented one is the failure mode here. When building a full deck, also follow its narrative-structure and content patterns.

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
- `docForPath(filePath)` — returns the Keynote document whose own file path matches, opening it if needed. **Every script resolves its target this way; never use `front document`** (see pitfalls).
- `backupDeck(filePath)` — copies the deck to `<deck-dir>/.keynote-skill/backups/<name>.<timestamp>.key`, then prunes so only the 3 most recent backups for that deck remain

## Common pitfalls

- **-1700 errors**: Avoid referencing `slide N of doc` immediately after creation in the same tell block. Use direct references from `make new slide` or operate in a separate open/save/close cycle.
- **AppleEvent timeouts (-1712)**: Never populate more than ~5 slides per open/save/close cycle. The `populate-deck` script handles this automatically.
- **Wrong text field**: Always check which layout a slide uses before setting text. Title layout has the title at item 2; Title Only has it at item 1.
- **Image corruption**: When inserting images via raw AppleScript, always pass `width` (and `position`/`file`) as **creation properties** to `make new image`. Setting `width` or `height` *after* the image is created has been observed to corrupt the .key file. The `insert-image` script handles this correctly.
- **`-10000` creating a text box**: A new text item must be created **inside a `tell <slide>` block** with `make new text item with properties {object text:…, position:…, width:…, height:…}` — the `height` property is required. Using `make new text item at end of slide`, or omitting `height`, throws `AppleEvent handler failed (-10000)`. This is a creation-structure problem, **not** a special-character/Unicode issue — don't waste time stripping `°`/arrows/etc. Set `font`/`size` on `object text` *after* creation. The `add-text-box` script encapsulates the working pattern, so reach for it instead of hand-rolling.
- **`text items` shadowing inside Keynote `tell` blocks**: Inside `tell application "Keynote"`, the term `text items` refers to slide text-item objects, not string parts. If you parse comma-separated args (e.g. `"180,550"`) by setting `AppleScript's text item delimiters` and reading `text items of <string>`, do it **outside** the Keynote tell block — otherwise you'll get error -1728 ("Can't get every text item of '180,550'"). Same applies to any keyword that overlaps Keynote's vocabulary.
- **Don't rebuild from JSON to fix one slide**: If the user has edited the deck, `populate-deck` will wipe their changes. Use `set-slide-text` for text fixes and `insert-image` for adding visuals.
- **Setting `object text` wholesale strips hyperlinks**: Overwriting a text box's `object text` (e.g. to reorder a references list) flattens any auto-detected URL links/underlines to plain text — Keynote does **not** re-autolink text set via AppleScript. To renumber/reorder a list while keeping only *some* lines intact, set individual `paragraph i of object text` (leaves untouched paragraphs' links alone). If the whole box must be rewritten, warn the user the URLs became plain text (they re-link by clicking into each line in the app).
- **`front document` is the wrong deck whenever a second one is open**: `open <file>` does not reliably bring an already-open deck to the front, so `open fileRef` + `set theDoc to front document` silently operates on whichever deck Keynote happened to have frontmost. Read scripts then return another deck's content — which looks like the user's deck mysteriously changed — and **write scripts edit the wrong file**, with the backup taken against the intended path, so the damage lands somewhere the backup can't undo. Resolve the target by matching each document's own file path (`docForPath`), never by front-most position. This applies to any new script you write against Keynote, not just the ones shipped here. The obvious shortcut `first document whose file is (POSIX file "…")` doesn't work either — it throws -1700 ("Can't make file into type specifier"); load `docForPath` from `_helpers.scpt` or loop over `documents` comparing `POSIX path of (file of d as alias)`.
- **`item N of (position of <image>)` throws -1700 when inlined**: Keynote returns `position` as a coercion-resistant record. `set py to (item 2 of (position of im)) as integer` fails; `set pp to position of im` then `set py to (item 2 of pp) as integer` works. Same for `width`/`height` — coerce `as integer` before concatenating into a string.
- **Image index ≠ insertion order**: `image i of slide N` follows z-order, which drifts from the order you inserted. To identify a specific logo in a row, match on its **position**, never its index. To clear one band of a slide (e.g. rebuild an app row while leaving a logo row above it untouched), iterate images in reverse and `delete` those whose y exceeds a threshold — deleting forward reindexes underneath you.
- **A batch of write-script calls outruns the backup window**: every write script takes a backup and then prunes to the 3 most recent, so the fourth call in a row silently discards the pre-batch snapshot — and a failed call (bad args) still backs up first, burning a slot without changing anything. Before running more than three write scripts against one deck (e.g. a row of six logos), `cp` the deck into `.keynote-skill/backups/<name>.prebatch-<timestamp>.key` yourself so the clean starting point survives.
- **zsh does not word-split unquoted variables**: a loop like `for spec in "word.png 150,655"; do set -- $spec; osascript ... "$1" "$2"` passes the whole spec as `$1` and an empty `$2`, so `insert-image` errors "Invalid position" (and still backs up, see above). Write the calls out explicitly, or split with `${=spec}` — `set -- $spec` only works in bash.
- **Stale exports fool pixel-measurement**: When verifying placement by measuring the exported PNG, make sure the export actually refreshed first. `export-images` writes to the output dir you pass literally — if you've `cd`'d elsewhere, a `$(pwd)/.keynote-skill/images/...` arg resolves to a *different, nested* dir and you'll keep measuring the old PNG (and chase a bug that isn't there). Pass an absolute output path, or check the file's mtime, before trusting the pixels.

## Notes

- Keynote must be installed on the system
- The AppleScripts open and close documents in Keynote automatically
- For large presentations, text extraction is usually sufficient; only export images when visuals matter
- The `populate-deck` script requires Python 3 (for JSON parsing)
- **Slides after the blank black end slide are backups, not misordered content.** In the user's talk decks, a blank black slide marks the end of the talk. Anything after it (welcome slide, alternate title, detail slides) is extra material he pulls up on demand. When reviewing a deck, judge flow and order only up to that blank slide.
