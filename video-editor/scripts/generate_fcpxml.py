"""Phase 3: Convert an EDL (Edit Decision List) + analysis JSON into FCPXML v1.11."""

import json
import os
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path
from urllib.parse import quote
from xml.dom import minidom


def seconds_to_rational(seconds: float, fps_num: int, fps_den: int) -> str:
    """Convert seconds to FCPXML rational time string.

    For 29.97fps: fps_num=30000, fps_den=1001
    For 30fps: fps_num=30, fps_den=1
    """
    frame_duration = Fraction(fps_den, fps_num)
    total_frames = round(Fraction(seconds) / frame_duration)
    rational = total_frames * frame_duration
    return f"{rational.numerator}/{rational.denominator}s"


def get_format_name(width: int, height: int, fps: float) -> str:
    """Generate FCP format name string."""
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


def generate_fcpxml(analysis: dict, edl: dict, output_path: str) -> str:
    """Generate FCPXML v1.11 from analysis and EDL.

    Args:
        analysis: Analysis JSON with metadata, source_file
        edl: EDL JSON with 'segments' list, each having:
            - start: float (source start time in seconds)
            - end: float (source end time in seconds)
            - action: "keep" or "cut"
            - volume_adjust_db: optional float
        output_path: Path to write FCPXML file
    """
    meta = analysis["metadata"]
    video_info = meta.get("video", {})
    source_file = analysis["source_file"]
    stem = Path(source_file).stem

    fps_num = video_info.get("fps_num", 30)
    fps_den = video_info.get("fps_den", 1)
    width = video_info.get("width", 1920)
    height = video_info.get("height", 1080)
    fps = video_info.get("fps", 30.0)
    total_duration = meta["duration"]

    format_name = get_format_name(width, height, fps)
    frame_dur = seconds_to_rational(fps_den / fps_num, fps_num, fps_den)

    # Filter to kept segments only
    kept_segments = [s for s in edl["segments"] if s.get("action") == "keep"]

    # Calculate total timeline duration
    timeline_dur = sum(s["end"] - s["start"] for s in kept_segments)

    # Build XML
    fcpxml = ET.Element("fcpxml", version="1.11")

    # Resources
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

    # Library > Event > Project > Sequence > Spine
    library = ET.SubElement(fcpxml, "library")
    event = ET.SubElement(library, "event", name=f"{stem} Edit")
    project = ET.SubElement(event, "project", name=f"{stem}_edit")
    sequence = ET.SubElement(project, "sequence",
                             format="r1",
                             duration=seconds_to_rational(timeline_dur, fps_num, fps_den),
                             tcStart="0s", tcFormat="NDF")
    spine = ET.SubElement(sequence, "spine")

    # Add clips
    timeline_offset = 0.0
    for i, seg in enumerate(kept_segments):
        seg_start = seg["start"]
        seg_dur = seg["end"] - seg["start"]

        clip = ET.SubElement(spine, "asset-clip",
                             ref="r2",
                             offset=seconds_to_rational(timeline_offset, fps_num, fps_den),
                             name=f"Segment {i + 1}",
                             duration=seconds_to_rational(seg_dur, fps_num, fps_den),
                             start=seconds_to_rational(seg_start, fps_num, fps_den),
                             tcFormat="NDF")

        # Volume adjustment
        vol_db = seg.get("volume_adjust_db", 0)
        if vol_db != 0:
            ET.SubElement(clip, "adjust-volume", amount=f"{vol_db:+.1f}dB")

        timeline_offset += seg_dur

    # Write XML with pretty printing
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    rough = ET.tostring(fcpxml, encoding="unicode")
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n' + rough
    parsed = minidom.parseString(xml_str)
    pretty = parsed.toprettyxml(indent="  ")
    # Remove the extra xml declaration minidom adds
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

    print(f"FCPXML written to {output_path}")
    print(f"  {len(kept_segments)} clips on timeline")
    print(f"  Timeline duration: {timeline_dur:.1f}s (original: {total_duration:.1f}s)")
    print(f"  Removed: {total_duration - timeline_dur:.1f}s ({(1 - timeline_dur/total_duration)*100:.0f}%)")

    return output_path


def _find_project_root(start_path: str) -> str:
    """Walk up from start_path to find the project root (contains .claude/ or .git/)."""
    current = os.path.dirname(start_path) if os.path.isfile(start_path) else start_path
    while current != os.path.dirname(current):
        if os.path.isdir(os.path.join(current, ".claude")) or os.path.isdir(os.path.join(current, ".git")):
            return current
        current = os.path.dirname(current)
    return os.path.dirname(start_path) if os.path.isfile(start_path) else start_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: uv run generate_fcpxml.py <analysis_json> <edl_json> [--output-dir <dir>]")
        sys.exit(1)

    analysis_path = sys.argv[1]
    edl_path = sys.argv[2]
    output_dir = None

    args = sys.argv[3:]
    i = 0
    while i < len(args):
        if args[i] == "--output-dir" and i + 1 < len(args):
            output_dir = args[i + 1]
            i += 2
        else:
            i += 1

    with open(analysis_path) as f:
        analysis = json.load(f)

    with open(edl_path) as f:
        edl = json.load(f)

    stem = Path(analysis["source_file"]).stem

    if output_dir is None:
        # Default to claude-edits/ in the project root
        source_file = analysis.get("source_file", analysis_path)
        project_root = _find_project_root(os.path.abspath(source_file))
        output_dir = os.path.join(project_root, "claude-edits")

    output_path = os.path.join(output_dir, f"{stem}_edit.fcpxml")
    generate_fcpxml(analysis, edl, output_path)
