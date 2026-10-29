# Asset Library

A running index of reusable assets bundled with this skill. **Add to this index whenever you fetch a new asset.** The point is that next time, you don't have to re-fetch.

## How to use

When an animation needs an asset listed here:

1. Copy from `~/.claude/skills/animation-builder/assets/<path>` into the working `animations/assets/` folder.
2. Reference it from the HTML with a relative path (e.g. `assets/claude-color.png`).

Don't reference the skill's bundled assets directly from the rendered HTML — each animation should be self-contained so it's portable.

## How to add a new asset

When you fetch a logo or icon to use in an animation:

1. Save the canonical copy into `assets/logos/` (or `icons/`, or a new subfolder).
2. Add a one-line entry to the relevant section below: filename, dimensions, source URL, one-line description.
3. Commit the change so the library actually grows.

---

## Logos

| File | Source | Notes |
|---|---|---|
| `logos/atlassian.png` / `.svg` | Wikimedia Commons | Atlassian "A" mark, blue gradient. |
| `logos/calendly.png` / `.svg` | Wikimedia Commons | Calendly C mark, blue. |
| `logos/chrome.png` | Wikimedia Commons | Google Chrome browser icon, color. |
| `logos/claude-color.png` | lobehub icons-static-png (`light/claude-color.png`) | Anthropic Claude sparkle, orange on transparent. Use on light avatar backgrounds for contrast. |
| `logos/claude-color.svg` | lobehub icons-static-svg (`icons/claude-color.svg`) | Vector Claude sparkle. Prefer this over the PNG at any size above ~48px; the PNG is colormapped and goes jagged when scaled. Also bundled in `templates/claude-ui/`. |
| `logos/github.png` | Wikimedia Commons | GitHub Octocat / wordmark, black. |
| `logos/gmail.png` | Wikimedia Commons (`Gmail_icon_(2020).svg`) | Gmail icon, color, 2020 variant. |
| `logos/google-calendar.png` | Wikimedia Commons (`Google_Calendar_icon_(2020).svg`) | Google Calendar icon, color, 2020 variant (shows current day's number). |
| `logos/google-drive.png` | Wikimedia Commons | Google Drive triangle, color. |
| `logos/google-sheets.svg` | Wikimedia Commons | Google Sheets icon, color. |
| `logos/linkedin.png` | Wikimedia Commons | LinkedIn "in" mark, blue. |
| `logos/notion.png` | Wikimedia Commons | Notion N, black on white. |
| `logos/slack.png` | Wikimedia Commons (`Slack_icon_2019.svg`) | Slack four-color hashmark. |

> For more brand logos, see the keynote skill (`~/.claude/skills/keynote/SKILL.md` § "Fetching assets from the web") — same Wikimedia/lobehub fetch pattern.

## Icons

| File | Notes |
|---|---|
| `icons/heroicons.md` | Quick-reference list of common Heroicons outline paths (wrench-screwdriver, sparkles, arrow-right, check, plus, x-mark, light-bulb, document-text, cog, user, users, briefcase). Default icon source for this skill. |

---

## Fetching new assets — quick patterns

### AI/tech brand logos (Claude, ChatGPT, Gemini, Cursor, etc.)
```bash
curl -sL -A "AnimationBuilder/1.0" \
  "https://unpkg.com/@lobehub/icons-static-png@latest/light/<name>-color.png" \
  -o "logos/<name>-color.png"
```
The `-color` suffix is the full-color variant. Drop it for monochrome.

### Generic brand logos
Wikimedia Commons via WebSearch/WebFetch. Use a descriptive User-Agent (Wikimedia 403s default UAs):
```bash
curl -sL -A "AnimationBuilder/1.0 (<your-email>)" "<wikimedia-url>" -o "logos/<name>.png"
```

### Verifying the download
```bash
file logos/<name>.png
```
Must report `PNG image data` — `HTML document` means you got an error page.

### Heroicons
Default source. Copy SVG paths directly from https://heroicons.com. Outline variants are the house style: 24×24 viewBox, stroke 1.5, currentColor, fill="none".
