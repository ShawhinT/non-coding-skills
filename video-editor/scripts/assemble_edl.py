#!/usr/bin/env python3
"""Assemble the final EDL: filter dedup drops, merge small gaps, pad, clamp, validate.

Self-contained — no imports outside stdlib. Carries its own EDL schema check
so this script stays portable across projects.

Usage:
    assemble_edl.py <validated_segments.json> <dedup_drops.json> \\
        --source-file <src> --parent-file <parent> --source-duration <dur> \\
        -o <edl.json> [--merge-gap 0.3] [--lead-in 0.08] [--tail-pad 0.15] \\
        [--transcript <words.json>] [--max-internal-gap 0.6]
"""

import argparse
import json
import sys
from pathlib import Path

DEFAULT_MERGE_GAP_S = 0.3     # merge two segments if their gap is smaller than this
DEFAULT_LEAD_IN_S = 0.08      # audio padding before each segment
DEFAULT_TAIL_S = 0.15         # audio padding after each segment
MIN_DURATION_S = 0.5          # drop segments shorter than this after padding
DEFAULT_MAX_INTERNAL_GAP_S = 0.6  # split a kept segment at interior dead air longer than this


def split_internal_gaps(seg, words, max_gap):
    """Split one kept segment at interior word-gaps longer than max_gap.

    A hand-authored keep range often spans several sentences, so a breath or
    thinking-pause between them lives *inside* the range where merge/pad can't
    reach it — the viewer hears dead air. Cutting there (a human editor's most
    common tightening move) means ending the piece at the last word before the
    gap and resuming at the first word after it. Segment boundaries stay on the
    range's own start/end; only interior cuts move, and they land on real word
    boundaries, so nothing is ever clipped mid-word.
    """
    ws = [w for w in words if w["end"] > seg["start"] + 1e-6 and w["start"] < seg["end"] - 1e-6]
    if len(ws) < 2:
        return [seg]
    pieces = []
    cur_start = seg["start"]
    prev_end = ws[0]["end"]
    for w in ws[1:]:
        if w["start"] - prev_end > max_gap:
            pieces.append({"start": cur_start, "end": prev_end})
            cur_start = w["start"]
        prev_end = w["end"]
    pieces.append({"start": cur_start, "end": seg["end"]})
    return pieces


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
    ap.add_argument("--transcript", type=Path, default=None,
                    help="Word-level transcript JSON. When given, kept segments are split "
                         "at interior dead air (see --max-internal-gap) so pauses inside a "
                         "multi-sentence keep range are tightened, not just gaps between ranges.")
    ap.add_argument("--max-internal-gap", type=float, default=DEFAULT_MAX_INTERNAL_GAP_S,
                    dest="max_internal_gap",
                    help=f"Split a kept segment wherever an interior word-gap exceeds this many "
                         f"seconds (default {DEFAULT_MAX_INTERNAL_GAP_S}). Needs --transcript.")
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

    n_internal_splits = 0
    if args.transcript:
        words = json.loads(args.transcript.read_text()).get("words", [])
        tightened = []
        for seg in merged:
            pieces = split_internal_gaps(seg, words, args.max_internal_gap)
            n_internal_splits += len(pieces) - 1
            tightened.extend(pieces)
        merged = tightened

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
        "n_internal_splits": n_internal_splits,
        "retention_pct": round(retention_pct, 2),
    }))


if __name__ == "__main__":
    main()
