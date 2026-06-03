#!/usr/bin/env python3
"""Convert a word-level transcript into segment-level JSON.

Walks the word array and starts a new segment whenever the gap between
consecutive words meets or exceeds a silence threshold.  No take detection,
no filler removal, no trimming, no merging — purely mechanical segmentation.

Input:  {"words": [{"word": str, "start": float, "end": float}, ...]}
Output: {"segments": [{"text": str, "start": float, "end": float}, ...]}

Usage:
    preprocess.py <transcript.json> -o <segments.json> [--silence-gap 0.5]
"""

import argparse
import json
import sys
from pathlib import Path

DEFAULT_SILENCE_GAP = 0.35


def segment_words(words, silence_gap):
    if not words:
        return []

    segments = []
    buf = [words[0]]
    for prev, cur in zip(words, words[1:]):
        gap = cur["start"] - prev["end"]
        if gap >= silence_gap:
            segments.append(_finalize(buf))
            buf = [cur]
        else:
            buf.append(cur)
    segments.append(_finalize(buf))
    return segments


def _finalize(buf):
    return {
        "text": " ".join(w["word"] for w in buf),
        "start": buf[0]["start"],
        "end": buf[-1]["end"],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("transcript", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--silence-gap", type=float, default=DEFAULT_SILENCE_GAP)
    args = ap.parse_args()

    data = json.loads(args.transcript.read_text())
    words = data["words"]
    segments = segment_words(words, args.silence_gap)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"segments": segments}, indent=2))

    total_chars = sum(len(s["text"]) for s in segments)
    print(json.dumps({
        "n_words": len(words),
        "n_segments": len(segments),
        "total_chars": total_chars,
    }))


if __name__ == "__main__":
    main()
