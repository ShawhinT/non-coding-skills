# Redaction — obscuring on-screen content (on request only)

Covering PII visible in the frame (emails, names, keys, account data) without cutting the content around it. **This is never a default pipeline step** — run it only when the user explicitly asks to obscure something. Don't proactively scan for PII or add redaction questions to the editorial brief.

## Workflow: map first, design second

1. **Locate the moment via transcript**, then bracket the exposure with extracted frames (`ffmpeg -ss <t> -frames:v 1`). Find the first frame where the content appears and the first frame where it's gone. Streaming text usually renders top-down without reflowing earlier lines, so content often sits at its final position from the moment it appears.
2. **Sweep beyond the flagged moment.** The same content reappears in ways the user may not have fully mapped: chat auto-scrolls bring it back at a *new* position; opening a menu dims it but leaves it legible behind the overlay; closing a menu can sharpen it briefly before a scroll removes it. Sample frames across the whole demo section, not just the reported window, and check adjacent features (e.g. an inbox demo after a calendar demo) for fresh leaks.
3. **Classify transitions computationally, not by eyeball.** Crop the target strip from frames at 5 fps, compare each against reference crops of the known states (RMS pixel distance), print state changes; refine the boundaries at 25 fps. This pins every patch swap to within a frame in two commands.

## Cover design

- **Static UI wants static patches.** Screen-share layouts are pixel-stable for long stretches. Sample the actual background color from the frame (`im.getpixel`) and cover with an exact-color rectangle — on flat UI backgrounds this is invisible. Patch the *whole line*, not just the sensitive substring: a fully absent line reads more naturally than a half-erased one.
- Each stable phase gets its own patch: a dimmed-behind-a-menu phase needs a patch in the dimmed color (sample it too), and a phase fully covered by a menu needs nothing.
- **Blur is the fallback**, when the user wants a visible redaction or the background isn't flat. Make it unrecoverable: downscale the region to a few pixels and upscale (mosaic), never a light Gaussian — blurred text in a known font can be reconstructed.
- **Don't chase moving or fading targets.** When the content sharpens/scrolls during a menu-close or scroll animation, a sub-second **spine cut** is cleaner than keyframed patches. Check the transcript for words inside the cut range and land both edges on word boundaries or silence; a trimmed "Okay, cool. So" costs nothing.

## Build and place

- Overlay asset: full-frame 1920×1080 transparent PNG with the patches, rendered to ProRes 4444 with alpha at the **sequence frame rate**:
  `ffmpeg -loop 1 -framerate <fps> -i patch.png -t <dur> -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le patch.mov`
  The PNG→MOV detour exists because `place_overlays.py` accepts video assets only — it ffprobes each placement and emits `<asset-clip>`, so still images must be wrapped first.
- **Prefer the flat draft render as the placement source** when one exists (`place_overlays.py <draft>.mp4 placements.json -o …`). Pixel positions and timings can then be verified directly against the frames the viewer will see, and the result is self-contained.
- Full-frame patches need no positioning in FCP — but if the project scales or crops the screen-share, the overlay needs the same transform copied onto it.
- **Spine micro-cut surgery** (no script support yet): split the single wrapped `<asset-clip>` into two — first keeps `duration` up to the cut-in; second gets `offset` = same timeline point, `start` = cut-out source time, `duration` = remainder. Keep all rationals frame-aligned (`round(s*fps)` frames) and update the `<sequence duration>`. Connected overlay clips must remain inside the host clip whose range contains them.

## Verify

- Composite each patch PNG over real extracted frames from its phase and view the result before rendering MOVs.
- Re-check the words at every cut boundary against the word-level transcript.
- After placement, re-parse the emitted FCPXML and confirm overlay timeline positions and durations arithmetically.

## FCPXML round-trip gotchas

- **`colorSpace` warning on re-import:** FCP exports non-standard values (e.g. `"5-1-2"`, from sources tagged bt470bg like Zoom recordings) that FCP itself then warns about when importing. Harmless (FCP falls back to Rec. 709) but noisy — sanitize to `colorSpace="1-1-1 (Rec. 709)"` when re-emitting an FCPXML that came from an FCP export.
- A connected clip anchored inside one spine clip may extend past that clip's end across later spine clips; FCP handles this, so one overlay can span many jump cuts.

## Style preference

Shaw prefers invisible exact-color patches over visible blur bars — the content should look like it was never there.
