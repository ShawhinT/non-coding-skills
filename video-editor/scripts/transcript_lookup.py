#!/usr/bin/env python3
"""Look up word-level timestamps in the source transcript.

A pure-DATA navigation tool for chunk sub-agents. It performs NO take
detection and NO trimming — it only answers "what words (with exact
start/end times) live here?" so the agent can choose a real word boundary
to head-trim or split a segment that fused two takes together.

The agent reasons about WHAT to cut; this tool resolves WHERE the cut
lands, using ground-truth timestamps instead of a guessed number.

Input transcript shape: {"words": [{"word": str, "start": float, "end": float}, ...]}

Modes (exactly one):
  --start T0 --end T1
      Print every word overlapping the time window [T0, T1], each with a
      `gap_before` (silence, in seconds, since the previous printed word).
      Use this on a kept segment whose text repeats its own opening or
      opens/ends on a stutter: read the words, find the last clean
      occurrence, and set your segment's start/end to that word's boundary.

  --phrase "some words"
      Find every occurrence of a phrase (case-insensitive, punctuation- and
      whitespace-insensitive) and print each match's start/end. Optionally
      restrict the search to [--start, --end]. Use this to locate where a
      restated line actually begins.

Usage:
  transcript_lookup.py <transcript.json> --start 3.64 --end 22.31
  transcript_lookup.py <transcript.json> --phrase "hey everyone i'm shaw"
  transcript_lookup.py <transcript.json> --phrase "in this video" --start 0 --end 30

Output: JSON to stdout (a list for --start/--end, an object for --phrase).
All times are seconds on the same clock as segments.json and the EDL.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def normalize(w):
    """Lowercase, strip non-alphanumeric — for phrase matching."""
    return re.sub(r"[^a-z0-9]", "", w.lower())


def words_in_range(words, t0, t1):
    out = []
    prev_end = None
    for w in words:
        if w["end"] > t0 and w["start"] < t1:  # overlaps the window
            gap = None if prev_end is None else round(w["start"] - prev_end, 3)
            out.append({
                "word": w["word"],
                "start": round(w["start"], 3),
                "end": round(w["end"], 3),
                "gap_before": gap,
            })
            prev_end = w["end"]
    return out


def find_phrase(words, phrase, t0, t1):
    toks = [normalize(t) for t in phrase.split() if normalize(t)]
    if not toks:
        return []
    n = len(toks)
    norm = [normalize(w["word"]) for w in words]
    matches = []
    for i in range(len(words) - n + 1):
        if norm[i:i + n] == toks:
            start = words[i]["start"]
            end = words[i + n - 1]["end"]
            if (t0 is None or end > t0) and (t1 is None or start < t1):
                matches.append({
                    "match_start": round(start, 3),
                    "match_end": round(end, 3),
                    "text": " ".join(words[j]["word"] for j in range(i, i + n)),
                })
    return matches


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("transcript", type=Path)
    ap.add_argument("--start", type=float, default=None)
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--phrase", type=str, default=None)
    args = ap.parse_args()

    words = json.loads(args.transcript.read_text())["words"]

    if args.phrase is not None:
        result = find_phrase(words, args.phrase, args.start, args.end)
        print(json.dumps({"phrase": args.phrase, "matches": result}, ensure_ascii=False))
        return

    if args.start is None or args.end is None:
        print("provide either --phrase, or both --start and --end", file=sys.stderr)
        sys.exit(2)

    result = words_in_range(words, args.start, args.end)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
