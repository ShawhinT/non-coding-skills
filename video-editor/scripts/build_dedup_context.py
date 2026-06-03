#!/usr/bin/env python3
"""Reconstruct segment text for the global-dedup sub-agent.

Reads the validated segments list and the source transcript, rebuilds the
text of each kept segment from the word array, and writes a human-readable
context file the dedup sub-agent can read. One line per segment:

    [idx 003 | 42.10-58.40] lorem ipsum dolor sit amet...

Usage:
    build_dedup_context.py <validated_segments.json> <transcript.json> -o <out.txt>
"""

import argparse
import bisect
import json
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("segments", type=Path)
    ap.add_argument("transcript", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    args = ap.parse_args()

    segments = json.loads(args.segments.read_text())
    words = json.loads(args.transcript.read_text())["words"]

    # bisect-indexed lookup: find words whose start >= seg.start and end <= seg.end
    word_starts = [w["start"] for w in words]

    lines = []
    for i, seg in enumerate(segments):
        lo = bisect.bisect_left(word_starts, seg["start"] - 0.01)
        hi = lo
        while hi < len(words) and words[hi]["end"] <= seg["end"] + 0.01:
            hi += 1
        text = " ".join(w["word"] for w in words[lo:hi])
        lines.append(f'[idx {i:03d} | {seg["start"]:.2f}-{seg["end"]:.2f}] {text}')

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n")

    print(json.dumps({
        "path": str(args.out),
        "n_segments": len(segments),
    }))


if __name__ == "__main__":
    main()
