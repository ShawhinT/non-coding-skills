#!/usr/bin/env bash
# speed-up-video.sh — speed up a video file using ffmpeg, preserving audio pitch.
# Usage: speed-up-video.sh <input> <speed> [output]
#   <speed>  multiplier (e.g. 2, 1.5, 4, 0.5). Audio pitch preserved via atempo.
#   [output] optional. Defaults to <input-stem>.<speed>x.<ext> next to the input.
#
# Examples:
#   speed-up-video.sh ~/Desktop/clip.mov 2
#   speed-up-video.sh ~/Desktop/clip.mov 4 ~/Desktop/clip-fast.mov

set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <input> <speed> [output]" >&2
  exit 1
fi

input="$1"
speed="$2"
output="${3:-}"

if [ ! -f "$input" ]; then
  echo "Input not found: $input" >&2
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found. Install with: brew install ffmpeg" >&2
  exit 1
fi

# Validate speed > 0
if ! awk "BEGIN { exit !($speed > 0) }"; then
  echo "Speed must be > 0 (got: $speed)" >&2
  exit 1
fi

# Default output: <stem>.<speed>x.<ext>
if [ -z "$output" ]; then
  dir=$(dirname "$input")
  base=$(basename "$input")
  stem="${base%.*}"
  ext="${base##*.}"
  output="${dir}/${stem}.${speed}x.${ext}"
fi

# Video PTS multiplier: 1/speed
pts=$(awk "BEGIN { printf \"%.6f\", 1/$speed }")

# atempo filter caps at 2.0 per stage; chain stages for higher speeds (and 0.5 min per stage for slow-down).
# Build atempo chain that multiplies to $speed, each stage in [0.5, 2.0].
atempo_chain=$(awk -v s="$speed" 'BEGIN {
  remaining = s
  out = ""
  if (remaining >= 1) {
    while (remaining > 2.0) { out = out "atempo=2.0,"; remaining /= 2.0 }
    out = out "atempo=" remaining
  } else {
    while (remaining < 0.5) { out = out "atempo=0.5,"; remaining /= 0.5 }
    out = out "atempo=" remaining
  }
  print out
}')

echo "Input:  $input"
echo "Speed:  ${speed}x"
echo "Output: $output"
echo "Filters: video setpts=${pts}*PTS, audio ${atempo_chain}"
echo

ffmpeg -y -i "$input" \
  -filter:v "setpts=${pts}*PTS" \
  -filter:a "$atempo_chain" \
  "$output"

echo
echo "Done: $output"
