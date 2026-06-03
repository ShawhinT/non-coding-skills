#!/usr/bin/env python3
"""Split segments.json into per-chunk files given a partition.

The partition is a JSON blob describing contiguous segment-index ranges
plus a title and rationale for each chunk.  The Opus chunker sub-agent
decides the partition editorially, then invokes this script to emit all
per-chunk files mechanically.

Partition format (stdin or --partition-file):
  {"chunks": [
    {"id": 0, "start_seg_idx": 0, "end_seg_idx": 42,
     "title": "Intro and hook", "rationale": "Multiple takes..."},
    ...
  ]}

Outputs to <out_dir>/:
  - chunks.json          enriched partition (adds start_time, end_time,
                         n_segments, json path, txt path per chunk)
  - chunk_N.json         {"segments": [...]} for each chunk
  - chunk_N.txt          human-readable transcript with silence markers

Validation:
  - indices cover [0, n_segments-1] contiguously, no gaps, no overlaps
  - every chunk has non-empty title and rationale
  - end_seg_idx >= start_seg_idx

Usage:
  split_chunks.py <segments.json> <out_dir> --partition-file <partition.json>
  split_chunks.py <segments.json> <out_dir>            # reads partition from stdin

Prints a JSON manifest to stdout.
"""

import argparse
import json
import sys
from pathlib import Path


def validate_partition(chunks, n_segments):
    if not chunks:
        raise ValueError("partition has no chunks")

    sorted_chunks = sorted(chunks, key=lambda c: c["start_seg_idx"])
    expected_start = 0
    for c in sorted_chunks:
        if c["start_seg_idx"] != expected_start:
            raise ValueError(
                f"gap/overlap: chunk {c['id']} starts at {c['start_seg_idx']}, "
                f"expected {expected_start}"
            )
        if c["end_seg_idx"] < c["start_seg_idx"]:
            raise ValueError(
                f"chunk {c['id']} end_seg_idx {c['end_seg_idx']} < start {c['start_seg_idx']}"
            )
        if not c.get("title"):
            raise ValueError(f"chunk {c['id']} missing title")
        if not c.get("rationale"):
            raise ValueError(f"chunk {c['id']} missing rationale")
        expected_start = c["end_seg_idx"] + 1

    if expected_start != n_segments:
        raise ValueError(
            f"partition ends at {expected_start - 1}, "
            f"expected last seg {n_segments - 1}"
        )


def write_chunk_txt(segs, txt_path):
    lines = []
    for i, seg in enumerate(segs):
        lines.append(f'[{seg["start"]:.2f}-{seg["end"]:.2f}] {seg["text"]}')
        if i + 1 < len(segs):
            gap = segs[i + 1]["start"] - seg["end"]
            if gap >= 1.5:
                lines.append(f'        --- [{gap:.1f}s silence] ---')
    txt_path.write_text("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("segments", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--partition-file", type=Path,
                    help="JSON file with chunk partition; omit to read from stdin")
    args = ap.parse_args()

    segments = json.loads(args.segments.read_text())["segments"]

    if args.partition_file:
        partition = json.loads(args.partition_file.read_text())
    else:
        partition = json.loads(sys.stdin.read())

    chunks = partition["chunks"]
    validate_partition(chunks, len(segments))

    args.out_dir.mkdir(parents=True, exist_ok=True)

    enriched = []
    for c in sorted(chunks, key=lambda x: x["start_seg_idx"]):
        cid = c["id"]
        chunk_segs = segments[c["start_seg_idx"]:c["end_seg_idx"] + 1]
        json_path = args.out_dir / f"chunk_{cid}.json"
        txt_path = args.out_dir / f"chunk_{cid}.txt"

        json_path.write_text(json.dumps({"segments": chunk_segs}, indent=2))
        write_chunk_txt(chunk_segs, txt_path)

        enriched.append({
            "id": cid,
            "start_seg_idx": c["start_seg_idx"],
            "end_seg_idx": c["end_seg_idx"],
            "start_time": chunk_segs[0]["start"],
            "end_time": chunk_segs[-1]["end"],
            "n_segments": len(chunk_segs),
            "title": c["title"],
            "rationale": c["rationale"],
            "json": str(json_path),
            "txt": str(txt_path),
        })

    chunks_path = args.out_dir / "chunks.json"
    chunks_path.write_text(json.dumps({"chunks": enriched}, indent=2))

    print(json.dumps({
        "chunks": enriched,
        "total_chunks": len(enriched),
        "chunks_file": str(chunks_path),
    }))


if __name__ == "__main__":
    main()
