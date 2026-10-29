# Cards & End Screens

Cards and end screens are post-publish packaging — the only in-video levers still available once a video is live (published videos are immutable; see the ABA youtube skill's analytics reference). Treat them like the description: a routing surface that respects the viewer's attention.

## Where the data comes from

- **Channel inventory + performance:** the ABA `youtube` skill — a *project-level* skill that lives only on Shaw's Mac inside the ABA repo at `~/Documents/_code/_stv/_products/aba/.claude/skills/youtube` (it is not in the skills pipeline, so no session sees it auto-listed; read its SKILL.md from that path). Its Data API pulls the full video list, its Analytics API pulls windowed views / `averageViewPercentage` / `subscribersGained`, and its OAuth token is cached at the skill root — scripts run with `uv` from that directory. Reads cost 1 unit each; use a 90-day window so the ranking reflects what's pulling *now*, not lifetime totals. Data lags 24–48h.
- **Placement timestamps:** transcribe the final render and locate the exact spoken moment (same rule as chapters in `descriptions.md` — never timeline math from an edit, never memory). A card that fires seconds before its trigger line reads as an interruption; one that fires as the line lands reads as a footnote.

## Placement principles

- **Relevance first, performance as tiebreaker.** A card earns its slot when the script *verbally hands off* to the target video — a term defined ("an LLM plus an agent harness" → the harness video), a tool named, a workflow demoed that another video covers in depth. Rank candidate targets by recent views/retention only after the relevance match is made; a big video with no textual hook is a worse card than a small video the line points straight at.
- **A card can deliberately revive a low-view video.** When an older video is the natural deep-dive for the avatar at that moment, low recent views are a reason *for* the card, not against it — the new video's traffic is the distribution the old one didn't get.
- **Skip the first ~2 minutes.** Retention is most fragile during the hook; a card there competes with the video's own promise. Note the passed-over candidate and its reason so the decision is auditable.
- **Five cards max (platform cap); space them out.** When two trigger moments fall close together (e.g. connectors at 3:27, skills at 3:49), pick the one target that covers both rather than stacking.
- **ICP lens on every target.** High views ≠ right audience (the ABA youtube skill's analytics reference documents this pitfall). Prefer the target whose title speaks to the avatar the current video attracted.

## End screen

Pair the subscribe element with the strongest *next-step* video for the avatar — judged by average-watch % and ICP fit, not raw views. The viewer at the end screen just finished the whole video; give them the video that deepens the relationship, not the one that merely trends.

## Mechanics

- Cards and end screens are set **manually in YouTube Studio** — the ABA youtube skill's write scripts cover descriptions only.
- Output format: a table of `time → target video (ID) → why`, plus an end-screen recommendation, plus the near-miss candidates with reasons. Timestamps word-accurate from the final-render transcript.
- Follow up ~2 weeks later with `cardClicks` / `cardClickRate` (Analytics API metrics) to see which placements actually pull, and fold that back into the next video's card choices.
