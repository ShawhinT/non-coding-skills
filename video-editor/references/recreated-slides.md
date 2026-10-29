# Recreated Slides Reference (no screen recording)

**Use when** a talk was filmed on camera only (podium/speaker cam) and the screen wasn't recorded, but the slide deck exists. You rebuild the screen as a synced slides track from the deck and composite the camera over it. Run Steps 0–6 of the main pipeline normally on the camera recording, then use this path instead of Step 7.

Worked example: Secure Dallas 2026 (`2-drafts/secure-dallas-2026/`) — 48 Keynote build stages + one embedded demo video, ~19 min final.

---

## Why this shape

- **Build on the raw camera timeline, not the edit.** Render the slides track (and the camera inset) starting at a frame-aligned raw-camera time `t0`. The overlays then sync to every spine clip with one constant offset — `overlay_time = camera_time - t0` — exactly like the dual-source PiP path, so cuts never drift the slides and re-cutting the EDL needs no re-render.
- **Cue on the words, not on guesses.** Each build stage appears when the speaker *says* the thing it reveals ("Toyota Financial", "Claude isn't secure"). Find those times in the word-level transcript; one stage per cue phrase.
- **Slides drive what must survive the cut.** Anything a slide visibly builds on (credentials, named examples, list items) must stay in the edit, or a build appears with nothing said about it. Tell chunk agents this in the brief — otherwise a credential line reads as "career tangent" filler and gets cut (it happened with the Toyota line).

## Step 1 — Export every build stage

Keynote's slide-image export takes `all stages:true` to emit one PNG per build step (the keynote skill's `export-images` has an `--all-stages` flag). Map stage numbers to slides by contact-sheeting the PNGs (`ffmpeg … tile=6x5`); the talk usually ends at the blank black slide, and slides past it are backups.

Embedded movies live inside the `.key` zip under `Data/` — `unzip -l deck.key | grep -E 'mp4|mov'`, then `unzip -j` the file out. Use the original rather than a screen grab.

## Step 2 — Write the timeline spec and render

`scripts/render_slides_track.py spec.json -o assets/slides_track.mp4` — the spec format is in the script's docstring. Events are `{"t", "image"}` (holds until the next event) or `{"t", "video", "anchors"}`.

**Videos are time-warped to the narration.** A demo video rarely plays in step with the speaker's commentary. Find the video's own beat changes (caption changes are easy to detect: diff a cropped caption strip at 4 fps), pair each with the transcript time the speaker narrates it, and pass those as `anchors` `[[video_s, camera_s], …]`. Each span is sped up or slowed to fit; keep ratios roughly within 0.6–1.9× or it looks wrong. If the speaker later re-describes the demo, play it again (a second event with its own anchors).

The script prints the frame-snapped `t0` — use it in Step 4. Check the output frame count equals `round((t1 - t0) * fps)`.

## Step 3 — Render the camera inset (alpha)

Shaw's layout for this case: **slides full frame, camera as a rounded tall (3:4) inset top-right** with a thin light border so it separates from white slides. Pre-render it as an alpha clip on the same raw timeline, because FCPXML has no clean rounded-corner control:

```bash
# mask.png / ring.png: 540x720 rounded rect (radius ~40) fill / 4px border (PIL)
ffmpeg -ss <t0> -i CAMERA.MP4 -loop 1 -i mask.png -loop 1 -i ring.png -filter_complex \
  "[0:v]crop=<w>:<h>:<x>:<y>,scale=540:720,format=rgba[c];[1:v]format=gray[m];\
   [c][m]alphamerge[a];[a][2:v]overlay=format=auto,format=yuva444p10le[o]" \
  -map "[o]" -an -frames:v <same frame count> -r <fps> -c:v prores_ks -profile:v 4444 -qscale:v 9 \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 inset_4444.mov   # scratch, ~4 GB
avconvert -s inset_4444.mov -o assets/camera_inset.mov -p PresetHEVCHighestQualityWithAlpha
```

- Pick the crop from a few frames across the talk — a locked-off camera needs one static crop around the speaker.
- Apple's encoder (`avconvert`) is the FCP-safe route: ~15× smaller than ProRes 4444 and correctly color-tagged. (ffmpeg's `hevc_videotoolbox -pix_fmt bgra` also produces alpha — ffprobe misleadingly reports `yuv420p`; `mdls -name kMDItemCodecs` shows "HEVC with Alpha" — but leaves the color matrix unspecified.)
- Before handing off, composite the inset over a few stage PNGs to spot slides whose content it covers; flag those to Shaw rather than auto-moving the inset.

## Step 4 — Emit the FCPXML

```bash
uv run scripts/make_slides_inset_fcpxml.py <project_dir>/edl.json \
    --slides assets/slides_track.mp4 --inset assets/camera_inset.mov \
    --track-t0 <t0> --project-name <video-name>_draft -o <project_dir>/edit.fcpxml
```

Per kept segment: spine = camera clip (audio; its picture sits hidden under the slides), lane 1 = slides (full frame), lane 2 = inset. Inset defaults: `--inset-scale 1/3` (a 540×720 clip is fit to canvas height → 810×1080, so 1/3 = 270×360), top-right with a 24 px margin (`--inset-x 801 --inset-y 336`, pixels; the script converts to FCPXML's percent-of-height units — see `picture-in-picture.md`).

Verify as in `picture-in-picture.md` ("Verify before handing off"): spine contiguous, every spine clip has both connected clips, `spine.start - overlay.start ≈ t0`, all `media-rep` paths resolve.
