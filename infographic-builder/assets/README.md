# Logo library — infographic-builder

Running index of bundled logos. Before fetching anything from the web, check this list and `ls logos/`. If you fetch a new asset, **add a line here** — without an entry, the file is invisible to future runs.

Format: `filename — source, brand color (if applicable), date added`

## logos/

- `claude.png` — lobehub `claude-color.png`, Anthropic orange, 2026-05-13
- `gmail.png` — Wikimedia Commons 500px thumb, multicolor, 2026-05-13
- `google-calendar.png` — Wikimedia Commons 500px thumb, multicolor, 2026-05-13
- `notion.svg` — simpleicons.org, #000000 (black), 2026-05-13
- `stripe.svg` — simpleicons.org, #635BFF, 2026-05-13
- `jira.svg` — simpleicons.org, #0052CC (Atlassian blue), 2026-05-13

## How to add a new logo

See SKILL.md § "Asset library" for the full source priority. Quick reference:

| Need | Source | Pattern |
|---|---|---|
| AI brand logo (Claude, GPT, Gemini…) | lobehub | `https://unpkg.com/@lobehub/icons-static-png@latest/light/<name>-color.png` |
| SaaS / app logo (Notion, Stripe, Slack…) | simpleicons.org | `https://cdn.simpleicons.org/<slug>/<hex-no-hash>` |
| Google / Microsoft / niche | Wikimedia Commons | `…/thumb/<x>/<xy>/<File.svg>/500px-<File.svg>.png` with descriptive UA |

After fetching:
1. Save to `logos/<name>.<ext>`.
2. Copy into the project's local `assets/` folder.
3. Append a line here.
4. Verify with `file <path>` — should report PNG or SVG, not HTML/ASCII (those are error pages).
