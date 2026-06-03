#!/usr/bin/env python3
"""Place overlay MP4s as connected clips above an existing FCPXML spine.

Thin emitter — overlay timeline positions are decided upstream by a Claude
sub-agent reading the script + transcript and written to a placements.json:

    {"placements": [
        {"asset": "/abs/path.mp4", "start": 52.3, "duration": 4.0},
        {"asset": "/abs/path.mp4", "start": 78.4},
        ...
    ]}

`start` is the absolute timeline position in seconds. `duration` is optional;
omitted means "use the asset's natural render length" (probed via ffprobe).

For each placement this script: finds the primary spine clip containing
`start`, computes the local source-time offset, and inserts a connected
<asset-clip lane="1"> nested inside that host clip in DTD-correct position
(before any audio-channel-source / filter / metadata children). Adds a
<format> resource for any overlay shape that differs from the spine.

No phrase matching, no kind-based offset arithmetic — those are upstream of
this script.
"""
import argparse, json, subprocess, urllib.parse
from pathlib import Path
import xml.etree.ElementTree as ET

# Media suffixes accepted as auto-wrap input (anything else assumed to be FCPXML).
MEDIA_SUFFIXES = {".mp4", ".mov", ".mkv", ".m4v"}


def parse_rational(s: str) -> float:
    s = s.rstrip("s")
    if "/" in s:
        n, d = s.split("/")
        return int(n) / int(d)
    return float(s)


def to_frame_str(seconds: float, num: int, den: int) -> str:
    if seconds <= 0:
        return "0s"
    frames = round(seconds * den / num)
    return f"{frames * num}/{den}s"


def ffprobe(path: Path):
    """Return (duration_s, width, height, fps_num, fps_den)."""
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate",
        "-show_entries", "format=duration",
        "-of", "json", str(path),
    ])
    j = json.loads(out)
    s = j["streams"][0]
    dur = float(j["format"]["duration"])
    num, den = (int(x) for x in s["r_frame_rate"].split("/"))
    return dur, int(s["width"]), int(s["height"]), num, den


# DTD: <asset-clip> storyline children (group 4) must precede group 5 tags below.
TRAILING_TAGS = {"audio-channel-source", "audio", "filter-video", "filter-audio",
                 "metadata", "marker"}


def wrap_media_as_fcpxml(media: Path) -> ET.ElementTree:
    """Build an in-memory single-spine FCPXML wrapping a flat media file.

    Used when the caller wants to place overlays against a rendered MP4 rather
    than an upstream FCPXML — typical when the editor handed us a flat cut, or
    the cut FCPXML and its render have drifted apart.

    All frame-aligned rationals (sequence + asset + spine clip durations) come
    from to_frame_str — no string-interpolated numerators. Hand-authoring an
    FCPXML wrapper is a typo trap: a single-digit slip in `<numerator>/<den>s`
    drifts the project by sub-second amounts that look correct but misalign
    every overlay placement. Going through code makes the typo class impossible.
    """
    dur_s, w, h, fps_num, fps_den = ffprobe(media)
    # FCPXML uses frame DURATION (1/fps), not frame rate, in rationals.
    # frame_duration_num = fps_den, frame_duration_den = fps_num.
    fd_num, fd_den = fps_den, fps_num
    dur_str = to_frame_str(dur_s, fd_num, fd_den)
    src_url = "file://" + urllib.parse.quote(str(media.resolve()), safe="/:")

    fcpxml = ET.Element("fcpxml", {"version": "1.11"})
    resources = ET.SubElement(fcpxml, "resources")
    ET.SubElement(resources, "format", {
        "id": "r1",
        "name": f"FFVideoFormat{h}p{fps_num//fps_den}",
        "width": str(w), "height": str(h),
        "frameDuration": f"{fd_num}/{fd_den}s",
    })
    asset = ET.SubElement(resources, "asset", {
        "id": "r2", "name": media.stem,
        "start": "0s", "duration": dur_str,
        "hasVideo": "1", "hasAudio": "1",
        "format": "r1",
        "audioSources": "1", "audioChannels": "2",
    })
    ET.SubElement(asset, "media-rep", {"kind": "original-media", "src": src_url})

    library = ET.SubElement(fcpxml, "library")
    event = ET.SubElement(library, "event", {"name": media.stem})
    project = ET.SubElement(event, "project", {"name": media.stem})
    sequence = ET.SubElement(project, "sequence", {
        "format": "r1", "duration": dur_str,
        "tcStart": "0s", "tcFormat": "NDF",
    })
    spine = ET.SubElement(sequence, "spine")
    ET.SubElement(spine, "asset-clip", {
        "ref": "r2", "offset": "0s", "name": media.stem,
        "duration": dur_str, "start": "0s", "tcFormat": "NDF",
    })
    return ET.ElementTree(fcpxml)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path,
                    help="existing FCPXML, or a flat media file (.mp4/.mov/.mkv/.m4v) "
                         "to auto-wrap as a single-spine sequence")
    ap.add_argument("placements", type=Path, help="placements.json")
    ap.add_argument("-o", "--output", type=Path, required=True)
    args = ap.parse_args()

    if args.source.suffix.lower() in MEDIA_SUFFIXES:
        print(f"wrapping {args.source.name} as single-spine sequence")
        tree = wrap_media_as_fcpxml(args.source)
    else:
        tree = ET.parse(args.source)
    root = tree.getroot()
    spine = root.find(".//spine")
    spine_clips = list(spine.findall("asset-clip"))

    # Sequence frame grid (for timeline offsets/durations)
    seq = root.find(".//sequence")
    seq_fmt = root.find(f".//format[@id='{seq.attrib['format']}']")
    seq_num, seq_den = (int(x) for x in seq_fmt.attrib["frameDuration"].rstrip("s").split("/"))

    placements = json.load(open(args.placements))["placements"]

    # Probe each asset and resolve duration default
    resolved = []
    for p in placements:
        path = Path(p["asset"])
        dur_s, w, h, fps_num, fps_den = ffprobe(path)
        tl_dur = p.get("duration", dur_s)
        resolved.append({
            "path": path, "start": float(p["start"]), "duration": float(tl_dur),
            "asset_render_dur": dur_s,
            "w": w, "h": h, "fps_num": fps_num, "fps_den": fps_den,
        })
        print(f"  {path.name:42s} tl={p['start']:7.2f}s dur={tl_dur:.2f}s")

    # Allocate resource IDs, declaring one <format> per unique shape
    resources = root.find("resources")
    existing_ids = {el.attrib["id"] for el in resources}
    def next_rid(start=10):
        i = start
        while f"r{i}" in existing_ids:
            i += 1
        existing_ids.add(f"r{i}")
        return f"r{i}"

    fmt_by_shape = {}
    for p in resolved:
        key = (p["w"], p["h"], p["fps_num"], p["fps_den"])
        if key not in fmt_by_shape:
            fid = next_rid()
            fmt_by_shape[key] = fid
            ET.SubElement(resources, "format", {
                "id": fid,
                "name": f"FFVideoFormat{p['h']}p{p['fps_num']//p['fps_den']}",
                "frameDuration": f"{p['fps_den'] * 100}/{p['fps_num'] * 100}s",
                "width": str(p["w"]),
                "height": str(p["h"]),
                "colorSpace": "1-1-1 (Rec. 709)",
            })

    # Add <asset> resources
    for p in resolved:
        fid = fmt_by_shape[(p["w"], p["h"], p["fps_num"], p["fps_den"])]
        p["rid"] = next_rid()
        asset_dur = to_frame_str(p["asset_render_dur"], p["fps_den"] * 100, p["fps_num"] * 100)
        src_url = "file://" + urllib.parse.quote(str(p["path"]), safe="/:")
        asset_el = ET.SubElement(resources, "asset", {
            "id": p["rid"], "name": p["path"].stem,
            "start": "0s", "duration": asset_dur,
            "hasVideo": "1", "format": fid,
            "videoSources": "1", "hasAudio": "0",
        })
        ET.SubElement(asset_el, "media-rep", {
            "kind": "original-media", "src": src_url,
        })

    # Nest each overlay inside the host primary spine clip containing its start
    for p in resolved:
        host, host_o, host_s = None, None, None
        for clip in spine_clips:
            o = parse_rational(clip.attrib["offset"])
            d = parse_rational(clip.attrib["duration"])
            if o <= p["start"] < o + d:
                host = clip
                host_o = o
                host_s = parse_rational(clip.attrib["start"])
                break
        if host is None:
            host = min(spine_clips,
                       key=lambda c: abs(parse_rational(c.attrib["offset"]) - p["start"]))
            host_o = parse_rational(host.attrib["offset"])
            host_s = parse_rational(host.attrib["start"])
            print(f"  !! no host clip contains tl={p['start']:.2f}s; using nearest "
                  f"({host.attrib.get('name','?')})")

        local_off = host_s + (p["start"] - host_o)
        overlay_el = ET.Element("asset-clip", {
            "ref": p["rid"], "lane": "1",
            "offset": to_frame_str(local_off, seq_num, seq_den),
            "name": p["path"].stem,
            "start": "0s",
            "duration": to_frame_str(p["duration"], seq_num, seq_den),
            "format": fmt_by_shape[(p["w"], p["h"], p["fps_num"], p["fps_den"])],
        })
        insert_at = len(list(host))
        for i, ch in enumerate(list(host)):
            if ch.tag in TRAILING_TAGS:
                insert_at = i
                break
        host.insert(insert_at, overlay_el)

    # Rename event/project to output stem
    out_name = args.output.stem
    for tag in (".//project", ".//event"):
        el = root.find(tag)
        if el is not None:
            el.attrib["name"] = out_name

    ET.indent(tree, space="    ")
    body = ET.tostring(root, encoding="unicode")
    args.output.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n\n' + body + "\n"
    )
    print(f"\nwrote {args.output} with {len(resolved)} overlay clip(s) "
          f"(project='{out_name}')")


if __name__ == "__main__":
    main()
