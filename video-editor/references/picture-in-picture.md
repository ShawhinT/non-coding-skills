# Dual-Source Picture-in-Picture Reference

**Rare path.** Use only when the shoot produced **two recordings of the same talk** and you want one full-screen as the main show with the other as a synced inset (PiP) in a corner — typically a speaker camera + a separate slides/screen capture. You usually keep the *better* recording's audio (often the camera's) and mute the other.

The standard Step 7 (`generate_fcpxml.py`) lays down a single-source spine. This path emits that spine **plus a per-segment, source-synced PiP** on lane 1 that gets cut alongside the spine automatically. Because each kept segment carries its own independently-synced inset, the PiP never drifts across cuts.

Cut the edit normally through Step 6 (the EDL is built from the **main/spine** recording — its transcript, its timeline). Then run this path instead of Step 7.

---

## Step A — Discover the audio sync offset

The two files almost never start at the same instant. You need a single constant offset:

```
pip_source_time = main_source_time - OFFSET
```

**Find it by audio cross-correlation. Do NOT eyeball it.** Extract a low-rate mono WAV from each file, correlate energy envelopes for a coarse lag, refine at sample level on a mid-talk window, then verify the lag is stable across the whole timeline (60 fps vs 29.97 fps sources *can* drift).

```bash
# 1. Extract mono 8 kHz WAVs (small, fast) from both files
ffmpeg -y -i MAIN.mp4   -vn -ac 1 -ar 8000 -c:a pcm_s16le main.wav  -loglevel error
ffmpeg -y -i PIP.mov    -vn -ac 1 -ar 8000 -c:a pcm_s16le pip.wav   -loglevel error
```

```python
# 2. Coarse lag via energy-envelope FFT cross-correlation
#    run with: uv run --with numpy python sync.py main.wav pip.wav
import wave, sys, numpy as np

def envelope(path, sr=8000, hop_hz=100):
    w = wave.open(path, "rb"); raw = w.readframes(w.getnframes()); w.close()
    x = np.frombuffer(raw, "<i2").astype(np.float32)
    hop = sr // hop_hz; m = (len(x)//hop)*hop
    env = np.sqrt((x[:m].reshape(-1, hop)**2).mean(1) + 1e-6)
    return env - env.mean()

main, pip = envelope(sys.argv[1]), envelope(sys.argv[2]); hop_hz = 100
n = len(main) + len(pip); nfft = 1 << (n-1).bit_length()
corr = np.fft.irfft(np.fft.rfft(main, nfft) * np.conj(np.fft.rfft(pip, nfft)), nfft)
corr = np.concatenate((corr[-(len(pip)-1):], corr[:len(main)]))
lag = np.arange(-(len(pip)-1), len(main))[np.argmax(corr)] / hop_hz
print(f"OFFSET ≈ {lag:.3f} s   (pip_time = main_time - OFFSET)")
```

Refine on a mid-talk window (correlate raw samples of a ~60 s slice of PIP against the expected region of MAIN) to get sub-frame precision, then sample the lag at ~5 points across the timeline — if it holds to within a few ms, a constant offset is safe. (In the AgentCon 2026 edit the offset was 15.771 s, stable end-to-end.) If it drifts, the constant-offset model is wrong and the PiP needs a time-warp instead — stop and flag it.

> numpy isn't in the skill venv by default — invoke with `uv run --with numpy python …` (or add it to `pyproject.toml` if this path becomes common).

---

## Step B — Emit the PiP FCPXML

```
uv run scripts/make_pip_fcpxml.py <project_dir>/edl.json \
    --slides <pip_source.mov> --slides-offset <OFFSET> \
    --project-name <video-name>_draft -o <project_dir>/edit.fcpxml \
    [--scale 0.3 --pos-x 632 --pos-y -338 --seq-w 1920 --seq-h 1080]
```

- The EDL's `source_file` is the **main/spine** recording — its audio is kept (`hasAudio="1"`). `--slides` is the **PiP** recording, declared muted (`hasAudio="0"`, `videoSources="1"`).
- `--slides-offset` is the `OFFSET` from Step A.
- The script declares three formats (sequence canvas, main native, PiP native), then for each kept segment writes a spine `<asset-clip ref=main>` with a nested `<asset-clip lane="1" ref=slides>`:
  - PiP `offset` = the segment's **main-source** time (the host clip's coordinate system — connected clips are offset in host source-time, not timeline time).
  - PiP `start` = `seg.start - OFFSET` (the in-point in the PiP's own media — this is what keeps it synced).
  - PiP `duration` = the segment duration, clamped to available PiP footage at the tail.
  - A child `<adjust-transform scale="sx sy" position="x y">` does the corner inset.
- Segments that begin **before PiP footage exists** (`seg.start < OFFSET`) get no inset — the main plays full-screen there.

**The PiP source must be video-only.** FCP re-scans the referenced media on import and **attaches its audio track even when the asset declares `hasAudio="0"`** — which causes *two* failures at once: double audio (you hear both recordings) AND the connected clip importing as audio-only, so the **PiP never shows on screen**. The declaration alone is not enough. The emitter handles this automatically: if `--slides` has an audio track it stream-copies a video-only sibling (`<stem>_video_only.<ext>`, `-an -c:v copy`) **into the project folder** (never next to the raw source) and references that. If you build the FCPXML by other means, strip the audio yourself first:

```bash
ffmpeg -y -i PIP.mov -an -c:v copy <project_dir>/PIP_video_only.mov
```

The sync OFFSET still applies unchanged — a video stream copy doesn't alter timing.

Sequence defaults to **1080p at the main recording's fps** (a 4K main conforms down to fill frame — the standard YouTube master, and it keeps the transform math in a predictable 1920×1080 pixel space). The spine times use the main recording's frame grid, so they stay exact.

---

## FCP transform coordinate system (the part that bites)

`<adjust-transform>` inside an `<asset-clip>` controls the inset. Getting the units wrong puts the PiP off-screen.

- `scale="sx sy"` — multiplier, `1.0` = 100%. `0.3` = 30%.
- `position="x y"` — translation of the clip's **center**, in **pixels of the FCP project/preview resolution**, origin at canvas center, **+X right, +Y up** (so *down* is negative Y).
- Before scale/position, FCP spatially conforms the clip to the canvas (default = Fit). A PiP source matching the canvas resolution (e.g. 1080p slides on a 1080p sequence) conforms 1:1, so `scale` acts on its true pixel size.

> **Position pixels are relative to the FCP PROJECT resolution, which is almost always 1080p — NOT the 4K source.** This bit us: a first attempt assumed a larger canvas and the inset landed off-frame. Confirm the project/preview is 1920×1080 (the generator sets the sequence to 1080p by default) and compute positions against 1920×1080. If the project is 4K, every position value must be recomputed against 3840×2160.

**Shaw's confirmed default (1920×1080 project):** bottom-right *quadrant*, flush to the corner — `--scale 0.5 --pos-x 480 --pos-y -275` (the generator's defaults, verified by Shaw in FCP). 50% scale = a 960×540 inset; centering it flush in the corner gives X = 960−480 = **480**, Y = −(540−270) = **−275**.

**Corner-placement math** (1920×1080 canvas, center origin):

```python
W, H = 1920, 1080
scale, margin = 0.50, 0            # 50% inset (quadrant), flush to the corner
pw, ph = W*scale, H*scale          # 960 x 540
# bottom-right:
pos_x =  (W/2 - pw/2 - margin)     #  480
pos_y = -(H/2 - ph/2 - margin)     # -275   (negative = down)
# add a margin (e.g. 40) to inset from the edges; flip signs for other corners:
# top-right (+,+), top-left (-,+), bottom-left (-,-)
```

**4K master caveat:** if you raise `--seq-w/--seq-h` to 3840×2160, `position` is now in 4K pixels — recompute with `W,H = 3840,2160` (same formula → bottom-right quadrant becomes 960 / −540). A 1080p PiP on a 4K sequence conforms *up* to fill first, so `scale` still measures against the 4K canvas. Prefer the 1080p sequence unless a 4K master is explicitly requested.

---

## Verify before handing off

PiP FCPXML failure modes are silent — an off-by-one rational drifts every inset, a malformed nesting makes FCP drop the connected clip on import without an error. Check:

```python
import xml.etree.ElementTree as ET
from fractions import Fraction
def fr(s): n,d = s.rstrip("s").split("/"); return Fraction(int(n), int(d))
root = ET.parse("edit.fcpxml").getroot()
ET.tostring(root)                                   # well-formed?
clips = root.findall(".//spine/asset-clip")
exp = Fraction(0); gaps = 0
for c in clips:                                     # spine contiguous, no gaps/overlaps?
    if fr(c.attrib["offset"]) != exp: gaps += 1
    exp += fr(c.attrib["duration"])
assert gaps == 0
assert all(c.find("asset-clip") is not None for c in clips)   # every clip has a PiP?
for c in (clips[0], clips[len(clips)//2], clips[-1]):         # sync ≈ OFFSET (within a frame)?
    print(fr(c.attrib["start"]) - fr(c.find("asset-clip").attrib["start"]))
```

Also confirm every `<media-rep src="file://…">` path resolves on disk — **decode `%20`→space and `%40`→`@`** first (Shaw's Drive path contains both). This matters because the project folder lives in `2-drafts/` while the media stays in `1-raw/` (see SKILL.md output SOP) — they're intentionally not colocated, and the FCPXML binds them by absolute `file://` URL.

See `fcpxml-format.md` ("Connected Clips and Lanes", "DTD Content Order", "Mixed Formats") for the structural rules the emitter relies on.
