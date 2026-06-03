#!/usr/bin/env python3
"""Snap sub-agent segment timestamps to real word boundaries, sort, dedup.

Reads every <chunks_dir>/chunk_*_segments.json (as written by chunk sub-agents)
and the source transcript, snaps each segment's start/end to the nearest real
word boundary via bisect, drops collapsed segments, sorts chronologically, and
writes <out>. Segments keep their "reason" field for downstream dedup.

Usage:
    validate_segments.py <chunks_dir> <transcript.json> -o <out.json>
"""

import argparse
import bisect
import json
import sys
from pathlib import Path


def snap(val, sorted_list):
    idx = bisect.bisect_left(sorted_list, val)
    candidates = []
    if idx > 0:
        candidates.append(sorted_list[idx - 1])
    if idx < len(sorted_list):
        candidates.append(sorted_list[idx])
    return min(candidates, key=lambda x: abs(x - val))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("chunks_dir", type=Path)
    ap.add_argument("transcript", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    args = ap.parse_args()

    words = json.loads(args.transcript.read_text())["words"]
    source_duration = words[-1]["end"]

    valid_starts = sorted({round(w["start"], 4) for w in words})
    valid_ends = sorted({round(w["end"], 4) for w in words})
    valid_start_set = set(valid_starts)
    valid_end_set = set(valid_ends)

    seg_files = sorted(args.chunks_dir.glob("chunk_*_segments.json"))
    if not seg_files:
        print(f"no chunk_*_segments.json files in {args.chunks_dir}", file=sys.stderr)
        sys.exit(1)

    all_segments = []
    snaps = 0
    loaded = 0
    for sf in seg_files:
        segments = json.loads(sf.read_text())
        loaded += len(segments)
        for seg in segments:
            s = round(seg["start"], 4)
            e = round(seg["end"], 4)
            if s not in valid_start_set:
                s = snap(s, valid_starts)
                snaps += 1
            if e not in valid_end_set:
                e = snap(e, valid_ends)
                snaps += 1
            if s < e:
                all_segments.append({
                    "start": s,
                    "end": e,
                    "reason": seg.get("reason", ""),
                })

    all_segments.sort(key=lambda x: x["start"])

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(all_segments, indent=2))

    total_kept = sum(s["end"] - s["start"] for s in all_segments)
    retention_pct = total_kept / source_duration * 100 if source_duration else 0.0

    print(json.dumps({
        "n_segments": len(all_segments),
        "n_loaded": loaded,
        "snaps": snaps,
        "retention_pct": round(retention_pct, 2),
        "out": str(args.out),
    }))


if __name__ == "__main__":
    main()
