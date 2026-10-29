#!/usr/bin/env python3
"""Generate an FCPXML where the camera (spine) is the main show and the slides
recording rides as a synced picture-in-picture in the bottom-right corner.

- Spine = camera asset-clips (one per kept EDL segment). Camera audio is used.
- PiP   = slides asset-clip on lane 1, nested in each spine clip, source-synced
          via a constant offset, scaled + positioned bottom-right, muted.

sync: slides_source_time = camera_source_time - SLIDES_OFFSET

Usage:
  make_pip_fcpxml.py <edl.json> --slides <slides.mov> --slides-offset 15.771 \
      -o out.fcpxml --project-name NAME [--scale 0.3 --pos-x 632 --pos-y -338]
"""
import argparse, json, os, subprocess
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path
from urllib.parse import quote
from xml.dom import minidom


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height,r_frame_rate,avg_frame_rate",
                        "-of", "json", path], capture_output=True, text=True, check=True)
    s = json.loads(r.stdout)["streams"][0]
    rate = s.get("avg_frame_rate")
    if not rate or rate == "0/0":
        rate = s["r_frame_rate"]
    n, d = (int(x) for x in rate.split("/"))
    return {"w": int(s["width"]), "h": int(s["height"]), "num": n, "den": d}


def has_audio(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a",
                          "-show_entries", "stream=index", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    return bool(out)


def ensure_video_only(path, out_dir):
    """FCP re-scans PiP media and attaches its audio track despite hasAudio="0",
    causing double audio AND importing the connected clip as audio-only (the PiP
    never shows). So the PiP source MUST be a video-only file. If `path` has an
    audio track, stream-copy a video-only copy into out_dir (the project folder,
    NOT next to the raw source) and use that."""
    if not has_audio(path):
        return path
    p = Path(path)
    vo = os.path.join(out_dir, p.stem + "_video_only" + p.suffix)
    if not os.path.exists(vo):
        os.makedirs(out_dir or ".", exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-i", path, "-an", "-c:v", "copy", vo,
                        "-loglevel", "error"], check=True)
    print(f"  PiP source had audio -> using video-only copy: {vo}")
    return vo


def rational(seconds, fps_num, fps_den):
    fd = Fraction(fps_den, fps_num)
    frames = round(Fraction(seconds).limit_denominator(10**9) / fd)
    r = frames * fd
    return f"{r.numerator}/{r.denominator}s"


def file_url(path):
    return "file://" + quote(os.path.abspath(path), safe="/:")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("edl", type=Path)
    ap.add_argument("--slides", required=True)
    ap.add_argument("--slides-offset", type=float, required=True,
                    help="slides_time = camera_time - this")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--project-name", default=None)
    ap.add_argument("--seq-w", type=int, default=1920)
    ap.add_argument("--seq-h", type=int, default=1080)
    # --pos-x/--pos-y are PIXELS of the sequence canvas (center origin, +y up);
    # converted to FCPXML units below. Defaults = bottom-right quadrant, flush
    # to the corner, on 1920x1080 (see references/picture-in-picture.md).
    ap.add_argument("--scale", type=float, default=0.5)
    ap.add_argument("--pos-x", type=float, default=480.0)
    ap.add_argument("--pos-y", type=float, default=-275.0)
    ap.add_argument("--skip-ranges", default=None,
                    help='JSON list of [start,end] camera-time ranges where NO PiP is '
                         'placed (e.g. a live-demo section with no slide). '
                         'e.g. "[[709,2032],[2099,2176]]"')
    args = ap.parse_args()
    skip = json.loads(args.skip_ranges) if args.skip_ranges else []
    def in_skip(t):
        return any(a <= t < b for a, b in skip)

    edl = json.loads(args.edl.read_text())
    cam_file = edl["source_file"]
    cam_dur = edl["source_duration"]
    segs = edl["segments"]
    off = args.slides_offset
    # FCP needs a video-only PiP source; put any derived copy in the project folder.
    args.slides = ensure_video_only(args.slides, os.path.dirname(os.path.abspath(args.out)))

    cam = probe(cam_file)
    sld = probe(args.slides)
    sld_dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nk=1:nw=1", args.slides]).decode().strip())

    # Sequence runs at the camera frame grid (29.97) so spine times are exact.
    seq_num, seq_den = cam["num"], cam["den"]   # e.g. 30000/1001
    label = args.project_name or Path(cam_file).stem

    fcpxml = ET.Element("fcpxml", version="1.11")
    res = ET.SubElement(fcpxml, "resources")
    # Sequence/canvas format (1080p at camera fps)
    ET.SubElement(res, "format", id="r1",
                  name=f"FFVideoFormat{args.seq_h}p2997",
                  width=str(args.seq_w), height=str(args.seq_h),
                  frameDuration=rational(seq_den / seq_num, seq_num, seq_den))
    # Camera native format (4K)
    ET.SubElement(res, "format", id="r2f",
                  name=f"FFVideoFormat{cam['h']}p2997",
                  width=str(cam["w"]), height=str(cam["h"]),
                  frameDuration=rational(cam["den"] / cam["num"], cam["num"], cam["den"]))
    # Slides native format (1080p60)
    ET.SubElement(res, "format", id="r3f",
                  name=f"FFVideoFormat{sld['h']}p{sld['num']//sld['den']}",
                  width=str(sld["w"]), height=str(sld["h"]),
                  colorSpace="1-1-1 (Rec. 709)",
                  frameDuration=f"{sld['den']*100}/{sld['num']*100}s")
    # Camera asset (audio kept)
    cam_asset = ET.SubElement(res, "asset", id="r2", name=Path(cam_file).stem,
                              start="0s", duration=rational(cam_dur, seq_num, seq_den),
                              format="r2f", hasVideo="1", hasAudio="1",
                              audioSources="1", audioChannels="2")
    ET.SubElement(cam_asset, "media-rep", kind="original-media", src=file_url(cam_file))
    # Slides asset (video only, muted)
    sld_asset = ET.SubElement(res, "asset", id="r3", name=Path(args.slides).stem,
                              start="0s",
                              duration=rational(sld_dur, sld["num"], sld["den"]),
                              format="r3f", hasVideo="1", videoSources="1", hasAudio="0")
    ET.SubElement(sld_asset, "media-rep", kind="original-media", src=file_url(args.slides))

    library = ET.SubElement(fcpxml, "library")
    event = ET.SubElement(library, "event", name=label)
    project = ET.SubElement(event, "project", name=label)
    tl_dur = sum(s["end"] - s["start"] for s in segs)
    sequence = ET.SubElement(project, "sequence", format="r1",
                             duration=rational(tl_dur, seq_num, seq_den),
                             tcStart="0s", tcFormat="NDF")
    spine = ET.SubElement(sequence, "spine")

    fd = Fraction(seq_den, seq_num)
    # FCPXML position units are % of frame height (100 = seq_h px), not pixels;
    # raw pixels import fine but park the PiP far off-screen.
    px_to_xml = lambda px: px * 100.0 / args.seq_h
    tl_off = Fraction(0)
    n_pip = 0
    for i, seg in enumerate(segs):
        seg_dur = seg["end"] - seg["start"]
        dur_frames = round(Fraction(seg_dur).limit_denominator(10**9) / fd)
        rdur = dur_frames * fd
        rdur_str = f"{rdur.numerator}/{rdur.denominator}s"

        clip = ET.SubElement(spine, "asset-clip", ref="r2",
                             offset=f"{tl_off.numerator}/{tl_off.denominator}s",
                             name=f"Segment {i+1}",
                             duration=rdur_str,
                             start=rational(seg["start"], seq_num, seq_den),
                             tcFormat="NDF")

        # Synced slides PiP for this segment (only where slides footage exists
        # and the segment isn't inside a skip range, e.g. a live-demo section)
        sld_in = seg["start"] - off
        if sld_in >= 0 and sld_in < sld_dur and not in_skip(seg["start"]):
            # clamp duration to available slides footage
            avail = sld_dur - sld_in
            pip_dur = min(seg_dur, avail)
            pip_frames = round(Fraction(pip_dur).limit_denominator(10**9) / fd)
            pip_rdur = pip_frames * fd
            pip = ET.SubElement(clip, "asset-clip", ref="r3", lane="1",
                                offset=rational(seg["start"], seq_num, seq_den),
                                name="Slides",
                                start=rational(sld_in, sld["num"], sld["den"]),
                                duration=f"{pip_rdur.numerator}/{pip_rdur.denominator}s",
                                format="r3f")
            ET.SubElement(pip, "adjust-transform",
                          scale=f"{args.scale} {args.scale}",
                          position=f"{px_to_xml(args.pos_x):.4f} {px_to_xml(args.pos_y):.4f}")
            n_pip += 1
        tl_off += rdur

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    rough = ET.tostring(fcpxml, encoding="unicode")
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n' + rough
    pretty = minidom.parseString(xml_str).toprettyxml(indent="  ")
    lines, seen = [], False
    for ln in pretty.split("\n"):
        if ln.strip().startswith("<?xml"):
            if seen:
                continue
            seen = True
        if ln.strip():
            lines.append(ln)
    Path(args.out).write_text("\n".join(lines) + "\n")
    print(json.dumps({"fcpxml": args.out, "n_clips": len(segs), "n_pip": n_pip,
                      "timeline_duration_s": round(tl_dur, 2),
                      "source_duration_s": round(cam_dur, 2)}))


if __name__ == "__main__":
    main()
