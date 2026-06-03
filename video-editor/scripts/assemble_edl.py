#!/usr/bin/env python3
"""Assemble the final EDL: filter dedup drops, merge small gaps, pad, clamp, validate.

Self-contained — no imports outside stdlib. Carries its own EDL schema check
so this script stays portable across projects.

Usage:
    assemble_edl.py <validated_segments.json> <dedup_drops.json> \\
        --source-file <src> --parent-file <parent> --source-duration <dur> \\
        -o <edl.json> [--merge-gap 0.3] [--lead-in 0.08] [--tail-pad 0.15]
"""

import argparse
import json
import sys
from pathlib import Path

DEFAULT_MERGE_GAP_S = 0.3     # merge two segments if their gap is smaller than this
DEFAULT_LEAD_IN_S = 0.08      # audio padding before each segment
DEFAULT_TAIL_S = 0.15         # audio padding after each segment
MIN_DURATION_S = 0.5          # drop segments shorter than this after padding


def validate_edl(edl):
    """Schema check: monotonic, non-overlapping, within [0, source_duration]."""
    for key in ("source_file", "source_duration", "parent_file", "segments"):
        if key not in edl:
            raise ValueError(f"EDL missing required key: {key}")
    dur = edl["source_duration"]
    prev_end = 0.0
    for i, seg in enumerate(edl["segments"]):
        s, e = seg["start"], seg["end"]
        if e <= s:
            raise ValueError(f"segment {i}: end ({e}) <= start ({s})")
        if s < prev_end:
            raise ValueError(f"segment {i}: start ({s}) overlaps previous end ({prev_end})")
        if e > dur + 1e-6:
            raise ValueError(f"segment {i}: end ({e}) exceeds source_duration ({dur})")
        prev_end = e


def should_drop(seg, drops, tol=0.5):
    for ds, de in drops:
        if seg["start"] >= ds - tol and seg["end"] <= de + tol:
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("validated", type=Path)
    ap.add_argument("dedup_drops", type=Path)
    ap.add_argument("--source-file", required=True)
    ap.add_argument("--parent-file", required=True)
    ap.add_argument("--source-duration", type=float, required=True)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--merge-gap", type=float, default=DEFAULT_MERGE_GAP_S,
                    dest="merge_gap",
                    help=f"Merge adjacent kept segments separated by less than this many "
                         f"seconds (default {DEFAULT_MERGE_GAP_S}).")
    ap.add_argument("--lead-in", type=float, default=DEFAULT_LEAD_IN_S,
                    dest="lead_in",
                    help=f"Audio pad before each segment, seconds (default {DEFAULT_LEAD_IN_S}).")
    ap.add_argument("--tail-pad", type=float, default=DEFAULT_TAIL_S,
                    dest="tail_pad",
                    help=f"Audio pad after each segment, seconds (default {DEFAULT_TAIL_S}).")
    args = ap.parse_args()

    segments = json.loads(args.validated.read_text())
    drops_raw = json.loads(args.dedup_drops.read_text()) if args.dedup_drops.exists() else []
    drops = [(d["start"], d["end"]) for d in drops_raw]

    kept = [s for s in segments if not should_drop(s, drops)]
    dropped = len(segments) - len(kept)

    kept.sort(key=lambda x: x["start"])

    if not kept:
        print(json.dumps({"error": "no segments after drops"}), file=sys.stderr)
        sys.exit(1)

    merged = [dict(start=kept[0]["start"], end=kept[0]["end"])]
    for seg in kept[1:]:
        gap = seg["start"] - merged[-1]["end"]
        if 0 <= gap < args.merge_gap:
            merged[-1]["end"] = seg["end"]
        else:
            merged.append(dict(start=seg["start"], end=seg["end"]))

    dur = args.source_duration
    padded = []
    for seg in merged:
        s = max(0.0, seg["start"] - args.lead_in)
        e = min(dur, seg["end"] + args.tail_pad)
        padded.append({"start": round(s, 4), "end": round(e, 4)})

    for i in range(1, len(padded)):
        if padded[i]["start"] < padded[i - 1]["end"]:
            padded[i]["start"] = padded[i - 1]["end"]

    final = [s for s in padded if s["end"] - s["start"] >= MIN_DURATION_S]

    edl = {
        "source_file": args.source_file,
        "parent_file": args.parent_file,
        "source_duration": dur,
        "segments": final,
    }
    validate_edl(edl)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(edl, indent=2))

    total_kept = sum(s["end"] - s["start"] for s in final)
    retention_pct = total_kept / dur * 100 if dur else 0.0

    print(json.dumps({
        "edl": str(args.out),
        "n_segments": len(final),
        "n_dropped_dedup": dropped,
        "retention_pct": round(retention_pct, 2),
    }))


if __name__ == "__main__":
    main()
