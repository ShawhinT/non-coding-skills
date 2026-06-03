#!/usr/bin/env python3
"""Convert a v3 EDL into an FCPXML v1.11 project file.

Takes a single EDL JSON (with source_file, source_duration, segments) and
probes the video metadata via ffprobe. All segments are treated as keeps.
Non-destructive — the FCPXML references the original media file.

Usage:
    generate_fcpxml.py <edl.json> -o <edit.fcpxml>
"""

import argparse
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path
from urllib.parse import quote
from xml.dom import minidom


def probe_video(path: str) -> dict:
    """Return video metadata via ffprobe: width, height, fps, fps_num, fps_den."""
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate,avg_frame_rate",
            "-of", "json", path,
        ],
        capture_output=True, text=True, check=True,
    )
    stream = json.loads(result.stdout)["streams"][0]
    width = int(stream["width"])
    height = int(stream["height"])
    # Prefer avg_frame_rate (more accurate for VFR); fall back to r_frame_rate
    rate_str = stream.get("avg_frame_rate") or stream["r_frame_rate"]
    num_str, den_str = rate_str.split("/")
    fps_num, fps_den = int(num_str), int(den_str)
    if fps_den == 0:
        raise ValueError(f"Invalid frame rate from ffprobe: {rate_str}")
    fps = fps_num / fps_den
    return {
        "width": width, "height": height,
        "fps": fps, "fps_num": fps_num, "fps_den": fps_den,
    }


def seconds_to_rational(seconds: float, fps_num: int, fps_den: int) -> str:
    """Convert seconds to FCPXML rational time string aligned to whole frames."""
    frame_duration = Fraction(fps_den, fps_num)
    total_frames = round(Fraction(seconds) / frame_duration)
    rational = total_frames * frame_duration
    return f"{rational.numerator}/{rational.denominator}s"


def get_format_name(width: int, height: int, fps: float) -> str:
    """Generate FCP format name string (e.g. FFVideoFormat1080p30)."""
    fps_names = {
        23.976: "2398", 24.0: "24", 25.0: "25",
        29.97: "2997", 30.0: "30", 50.0: "50",
        59.94: "5994", 60.0: "60",
    }
    fps_key = min(fps_names.keys(), key=lambda k: abs(k - fps))
    fps_str = fps_names[fps_key]

    if height <= 1080:
        return f"FFVideoFormat1080p{fps_str}"
    elif height <= 2160:
        return f"FFVideoFormat2160p{fps_str}"
    else:
        return f"FFVideoFormat{height}p{fps_str}"


def file_url(path: str) -> str:
    """Convert a file path to a file:// URL."""
    abs_path = os.path.abspath(path)
    return "file://" + quote(abs_path, safe="/:")


def generate_fcpxml(edl: dict, output_path: str, project_name: str | None = None) -> str:
    """Generate FCPXML v1.11 from a v3 EDL.

    project_name, when provided, overrides the event and project labels inside
    the FCPXML. The media asset keeps the real file stem so Final Cut can
    resolve the underlying media.
    """
    source_file = edl["source_file"]
    total_duration = edl["source_duration"]
    segments = edl["segments"]
    stem = Path(source_file).stem
    label = project_name or stem

    video_info = probe_video(source_file)
    fps_num = video_info["fps_num"]
    fps_den = video_info["fps_den"]
    width = video_info["width"]
    height = video_info["height"]
    fps = video_info["fps"]

    format_name = get_format_name(width, height, fps)
    frame_dur = seconds_to_rational(fps_den / fps_num, fps_num, fps_den)

    timeline_dur = sum(s["end"] - s["start"] for s in segments)

    fcpxml = ET.Element("fcpxml", version="1.11")

    resources = ET.SubElement(fcpxml, "resources")
    ET.SubElement(resources, "format",
                  id="r1", name=format_name,
                  width=str(width), height=str(height),
                  frameDuration=frame_dur)
    asset = ET.SubElement(resources, "asset",
                          id="r2", name=stem,
                          start="0s",
                          duration=seconds_to_rational(total_duration, fps_num, fps_den),
                          hasVideo="1", hasAudio="1")
    ET.SubElement(asset, "media-rep", kind="original-media", src=file_url(source_file))

    library = ET.SubElement(fcpxml, "library")
    event = ET.SubElement(library, "event", name=label if project_name else f"{stem} Edit")
    project = ET.SubElement(event, "project", name=label if project_name else f"{stem}_edit")
    sequence = ET.SubElement(project, "sequence",
                             format="r1",
                             duration=seconds_to_rational(timeline_dur, fps_num, fps_den),
                             tcStart="0s", tcFormat="NDF")
    spine = ET.SubElement(sequence, "spine")

    frame_duration = Fraction(fps_den, fps_num)
    timeline_offset = Fraction(0)
    for i, seg in enumerate(segments):
        seg_start = seg["start"]
        seg_dur = seg["end"] - seg["start"]

        dur_frames = round(Fraction(seg_dur) / frame_duration)
        rational_dur = dur_frames * frame_duration

        ET.SubElement(spine, "asset-clip",
                      ref="r2",
                      offset=f"{timeline_offset.numerator}/{timeline_offset.denominator}s",
                      name=f"Segment {i + 1}",
                      duration=f"{rational_dur.numerator}/{rational_dur.denominator}s",
                      start=seconds_to_rational(seg_start, fps_num, fps_den),
                      tcFormat="NDF")

        timeline_offset += rational_dur

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    rough = ET.tostring(fcpxml, encoding="unicode")
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n' + rough
    parsed = minidom.parseString(xml_str)
    pretty = parsed.toprettyxml(indent="  ")
    lines = pretty.split("\n")
    final_lines = []
    seen_xml_decl = False
    for line in lines:
        if line.strip().startswith("<?xml") and not seen_xml_decl:
            seen_xml_decl = True
            final_lines.append(line)
        elif line.strip().startswith("<?xml"):
            continue
        else:
            final_lines.append(line)
    final = "\n".join(final_lines)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final)

    print(json.dumps({
        "fcpxml": output_path,
        "n_clips": len(segments),
        "timeline_duration_s": round(timeline_dur, 2),
        "source_duration_s": round(total_duration, 2),
    }))

    return output_path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("edl", type=Path, help="Path to EDL JSON")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output FCPXML path")
    ap.add_argument("--project-name", type=str, default=None,
                    help="Override event/project labels inside the FCPXML "
                         "(asset media name still uses the source file stem).")
    args = ap.parse_args()

    edl = json.loads(args.edl.read_text())
    generate_fcpxml(edl, str(args.out), project_name=args.project_name)


if __name__ == "__main__":
    main()
