# Redaction — obscuring on-screen content (on request only)

Covering PII visible in the frame (emails, names, keys, account data) without cutting the content around it. **This is never a default pipeline step** — run it only when the user explicitly asks to obscure something. Don't proactively scan for PII or add redaction questions to the editorial brief.

## Scope the brief before touching a frame

A redaction request names a *category* far more often than a string — "obscure any real client names" — and the category is narrower than it sounds. Confirm two things in one short question before mapping, and recommend a default so the user can answer "ok":

- **Which categories are sensitive, and which are the demo.** On Shaw's channel the answer so far: company and organization names (and corporate email domains) are sensitive; first names, full personal names, times, venues, addresses and meeting links stay. A calendar demo whose events have been wiped to blank blocks no longer shows the viewer anything, and "people need to see the event details" was the correction that forced a full redo. The surrounding content is usually the payload, so err toward covering less.
- **Visible or invisible.** Invisible exact-color patches are the default (see Cover design); blur only when the user wants the redaction to read as a redaction.

Getting this wrong is expensive: a whole-block pass on this kind of demo costs an hour of agent time and hundreds of MB of alpha video, all of it thrown away. Classification ambiguity does not get resolved silently either — when a string could be an org or could be a venue, nickname or acronym (an "LFC" event, "Neighborhood Services", a pitch competition's sponsor), decide one way, list it under **unsure** in the deliverable, and let the user flip it.

## Workflow: discover, map, then design

1. **Discover when the targets aren't enumerated.** If the user gave strings and moments, skip to step 2. If they gave a category, sweep: extract frames across every section where the sensitive app is on screen, OCR them, aggregate the unique strings, and classify. `scripts/ocr_frames.swift` (Apple Vision, build with `swiftc -O`) does the OCR — line mode writes one JSON per frame and skips frames already done, so it's safe to re-run over a growing frame set. Scope the sweep by *app context* rather than by the user's memory of when they switched: an anchor string in the OCR output (`calendar.google.com`, a GMT offset, an inbox header) tells you which frames show the app, and the hit list then tells you the exact timeline ranges. Sample at a few fps for discovery and go to every frame only for the ranges that have hits. Work in **timeline** frames (`timeline = clip.offset + source_t − clip.start`, from the spine) so the overlays line up with the cut; keep the timeline→source map handy for grabbing frames from the raw file.
2. **Bracket each exposure with extracted frames** (`ffmpeg -ss <t> -frames:v 1`). Find the first frame where the content appears and the first frame where it's gone. Streaming text usually renders top-down without reflowing earlier lines, so content often sits at its final position from the moment it appears.
3. **Sweep beyond the flagged moment.** The same content reappears in ways the user never mapped: chat auto-scrolls bring it back at a *new* position; opening a menu dims it but leaves it legible behind the overlay; closing a menu can sharpen it briefly before a scroll removes it; a horizontal scroll leaves a word fragment ("cme Corp", "s Connected") at the viewport edge that a string match on the full name misses. Match on fragments and case-insensitive stems, not whole words, and check adjacent features (an inbox demo after a calendar demo) for fresh leaks.
4. **Classify transitions computationally, not by eyeball.** Crop the target strip from frames at 5 fps, compare each against reference crops of the known states (RMS pixel distance), print state changes; refine the boundaries at 25 fps. For a sweep that already has per-frame OCR, the same idea is cheaper: hash the set of target boxes per frame, and a run of identical hashes is one stable phase with one patch.

## Cover design

- **Static UI wants static patches.** Screen-share layouts are pixel-stable for long stretches. Sample the actual background color from the frame (`im.getpixel`, or the modal color of the box for anti-aliased text) and cover with an exact-color rectangle — on flat UI backgrounds this is invisible.
- **Cover the identifying token, not the line, when the line is the demo.** A whole-line patch reads most naturally when the line is incidental (a stray email in a terminal). When the line *is* what the viewer is looking at — a calendar event, an inbox row, a contact in a dropdown — cover only the sensitive word(s) so the rest still reads: "▮ / ABA – Weekly AI", "Claude Code Workshop with ▮ – Dallas". Get word boxes from `ocr_frames --words` on a 3× upscaled crop of the line (far more accurate than full-frame word boxes), snap the patch's right edge into the inter-word gap so the next glyph isn't nicked, pad a few px vertically for blurry scroll frames, and clamp the box against neighbouring OCR lines so you don't clip the row below. A neighbouring block's edge, a slash, or a parenthesis clipped by a pixel is invisible at playback speed; a clipped time or the next event's first letter is not.
- Each stable phase gets its own patch: a dimmed-behind-a-menu phase needs a patch in the dimmed color (sample it too), and a phase fully covered by a menu needs nothing.
- **Exclusion zones.** Define regions the patch must never cross (the facecam inset, a cursor overlay) and mask every patch against them; a box that drifts a few px into the facecam circle is the one artifact viewers do notice.
- **Blur is the fallback**, when the user wants a visible redaction or the background isn't flat. Make it unrecoverable: downscale the region to a few pixels and upscale (mosaic), never a light Gaussian — blurred text in a known font can be reconstructed.
- **Incidental motion wants a cut; demonstrated motion wants a per-frame sequence.** When the content sharpens/scrolls during a menu-close or scroll animation that *isn't the point*, a sub-second **spine cut** is cleaner than keyframed patches. Check the transcript for words inside the cut range and land both edges on word boundaries or silence; a trimmed "Okay, cool. So" costs nothing. But when the scroll or drag is what the user is showing (dragging an event, paging through weeks), the patch has to follow: build one RGBA patch per stable phase from that phase's own OCR boxes, repeat it for the phase's frame run, and stream the frames straight into ffmpeg as rawvideo (`-f rawvideo -pix_fmt rgba -s WxH -r <fps> -i -`) so no intermediate PNGs are written. A phase missed by OCR (one blurry frame mid-scroll) is propagated from its neighbours, never left bare.

## Build and place

- Overlay asset: full-frame transparent image(s) at the sequence size, rendered to ProRes 4444 with alpha at the **sequence frame rate**:
  `ffmpeg -loop 1 -framerate <fps> -i patch.png -t <dur> -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le patch.mov`
  The PNG→MOV detour exists because `place_overlays.py` accepts video assets only — it ffprobes each placement and emits `<asset-clip>`, so still images must be wrapped first. Frame counts must be exact (`ffprobe -count_frames`); a one-frame-long MOV lands a patch on the frame after the content left.
- **Prefer the flat draft render as the placement source** when one exists (`place_overlays.py <draft>.mp4 placements.json -o …`). Pixel positions and timings can then be verified directly against the frames the viewer will see, and the result is self-contained.
- Full-frame patches need no positioning in FCP — but if the project scales or crops the screen-share, the overlay needs the same transform copied onto it.
- **Spine micro-cut surgery** (no script support yet): split the single wrapped `<asset-clip>` into two — first keeps `duration` up to the cut-in; second gets `offset` = same timeline point, `start` = cut-out source time, `duration` = remainder. Keep all rationals frame-aligned (`round(s*fps)` frames) and update the `<sequence duration>`. Connected overlay clips must remain inside the host clip whose range contains them.

## Fan out when the exposure is long

A sweep of a few thousand frames with hundreds of phases is a 40-minute job for one agent, most of it serial frame work. Do the shared pre-computation once in the parent — frame extraction, OCR, the phase index, the timeline↔source map, a small shared helper module — then split the hit ranges into contiguous time batches and give each to its own Opus sub-agent. Each batch returns its MOVs, a `placements_<batch>.json` fragment, and a short notes file (what it covered, what it left visible, anything unsure); the parent concatenates the placements and writes the map. Batches stay independent only if they never share a phase, so split on phase boundaries.

## Verify

- Composite each patch over real extracted frames from its phase and view the result before rendering MOVs. **Composite with PIL (`Image.alpha_composite`), not ffmpeg's `overlay` filter** — on these ProRes 4444 sources the filter has silently dropped the alpha and shown an unpatched frame, which reads as "patches missing" and sends you debugging the wrong thing.
- Re-OCR the composited frames and grep the result for the blocklist. A regex over OCR text catches a leaked fragment in frame 13987 that no amount of spot-viewing will.
- Re-check the words at every cut boundary against the word-level transcript.
- After placement, re-parse the emitted FCPXML and confirm overlay timeline positions and durations arithmetically.

## Deliverable

One final FCPXML, and next to the MOVs a `redaction_map.md` the user can audit without opening FCP: per clip, its timeline and source range, what it covers; then a list of what was considered and **left visible** and why, and the **unsure** items. Shaw un-redacts or extends from that list, so the "left visible" section is not optional. When a redo supersedes a pass, say which folder is now unreferenced and how big it is rather than deleting it unasked.

## FCPXML round-trip gotchas

- **`colorSpace` warning on re-import:** FCP exports non-standard values (e.g. `"5-1-2"`, from sources tagged bt470bg like Zoom recordings) that FCP itself then warns about when importing. Harmless (FCP falls back to Rec. 709) but noisy — sanitize to `colorSpace="1-1-1 (Rec. 709)"` when re-emitting an FCPXML that came from an FCP export.
- A connected clip anchored inside one spine clip may extend past that clip's end across later spine clips; FCP handles this, so one overlay can span many jump cuts.

## Style preference

Shaw prefers invisible exact-color patches over visible blur bars — the content should look like it was never there. Scope is company/organization names only; people's first and full names, times, venues and meeting links stay visible so the demo still reads.
