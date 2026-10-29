#!/usr/bin/env python3
"""Render a recreated-slides video track on the RAW camera timeline.

Used when a talk's screen wasn't recorded: slide build-stage PNGs (and any
embedded demo videos) are laid out at the camera-source times where the speaker
reached them, so the track syncs to the camera with one constant offset (t0).

Spec JSON:
{
  "t0": 600.0,            # raw-camera seconds where the track starts (snapped to a frame)
  "t1": 2015.0,           # raw-camera seconds where it ends
  "fps": "30000/1001",    # camera frame rate
  "events": [
    {"t": 600.0,  "image": "/abs/stages.001.png"},
    {"t": 1269.3, "video": "/abs/demo.mp4",
     "anchors": [[0, 1269.3], [4.25, 1275.6], ..., [83.9, 1346.0]]},
    {"t": 1453.8, "image": "/abs/stages.044.png"}
  ]
}
An image holds until the next event. A video is time-warped piecewise so each
anchor [video_s, camera_s] lands on the camera time where the speaker narrates
that moment; after the last anchor its final frame holds until the next event.

Prints t0 (frame-snapped) — pass it to make_slides_inset_fcpxml.py --track-t0.

Usage: render_slides_track.py spec.json -o slides_track.mp4 [--work-dir DIR]
"""
import argparse, json, os, subprocess, tempfile
from fractions import Fraction


def run(cmd):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y"] + cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--work-dir", default=None)
    a = ap.parse_args()
    spec = json.load(open(a.spec))
    fps = Fraction(spec.get("fps", "30000/1001"))
    work = a.work_dir or tempfile.mkdtemp(prefix="slides_track_")
    os.makedirs(work, exist_ok=True)

    f0 = round(Fraction(spec["t0"]).limit_denominator(10**6) * fps)
    t0 = float(f0 / fps)
    frame = lambda t: round(Fraction(t).limit_denominator(10**6) * fps) - f0

    # Flatten events into (time, kind, payload): stills and warped video spans.
    tl = []
    for i, ev in enumerate(spec["events"]):
        if "image" in ev:
            tl.append((ev["t"], "img", ev["image"]))
            continue
        anchors = ev["anchors"]
        for (d0, c0), (d1, c1) in zip(anchors, anchors[1:]):
            tl.append((c0, "vid", (ev["video"], d0, d1)))
        last = os.path.join(work, f"last_{i}.png")
        run(["-sseof", "-0.2", "-i", ev["video"], "-frames:v", "1", last])
        tl.append((anchors[-1][1], "img", last))
    tl.sort(key=lambda x: x[0])

    enc = ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
           "-r", str(fps), "-an"]
    pieces = []
    for i, (t, kind, p) in enumerate(tl):
        start = max(frame(t), 0)
        end = frame(tl[i + 1][0]) if i + 1 < len(tl) else frame(spec["t1"])
        n = end - start
        if n <= 0:
            continue
        out = os.path.join(work, f"p{i:04d}.mp4")
        if kind == "img":
            run(["-loop", "1", "-framerate", str(fps), "-i", p,
                 "-vf", "scale=1920:1080,setsar=1", "-frames:v", str(n)] + enc + [out])
        else:
            src, d0, d1 = p
            k = float(n / fps) / (d1 - d0)   # >1 slows the clip, <1 speeds it up
            run(["-ss", str(d0), "-i", src, "-vf",
                 f"trim=duration={d1 - d0},setpts=(PTS-STARTPTS)*{k},fps={fps},"
                 "scale=1920:1080,setsar=1,tpad=stop_mode=clone:stop_duration=2",
                 "-frames:v", str(n)] + enc + [out])
        pieces.append(out)

    lst = os.path.join(work, "list.txt")
    with open(lst, "w") as f:
        f.writelines(f"file '{p}'\n" for p in pieces)
    run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", a.out])
    print(json.dumps({"out": a.out, "t0": round(t0, 6), "frames": frame(spec["t1"]),
                      "pieces": len(pieces)}))


if __name__ == "__main__":
    main()
