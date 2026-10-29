#!/bin/zsh
# Joins assets/N-*.mp4 (in playback order) into one video with 0.4s crossfades.
# Offsets come from each clip's real duration, so re-rendering a scene at a new length just works.
# Usage: ./assemble.sh [out.mp4] [N=path/to/replacement.mp4 ...]   e.g. 7=assets/alt/7-animation-next_client_auto.mp4
set -e
cd "${ASSEMBLE_DIR:-$PWD}"   # run from the video folder (the one holding assets/)
XF=0.4
OUT=${1:-video.mp4}; (( $# )) && shift
clips=(${(f)"$(ls assets/*.mp4 | sort -t/ -k2 -n)"})
for r in "$@"; do clips[${r%%=*}]=${r#*=}; done
inputs=(); filter=""; prev="0"; t=0
for i in {1..$#clips}; do
  inputs+=(-i $clips[$i])
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $clips[$i])
  if (( i > 1 )); then
    out="v$i"; (( i == $#clips )) && out="vout"
    filter+="[${prev}][$((i-1))]xfade=transition=fade:duration=$XF:offset=$(printf %.3f $t)[${out}];"
    prev=$out
  fi
  t=$(( t + d - XF ))
done
ffmpeg -y -loglevel error $inputs -filter_complex "${filter}[vout]format=yuv420p[v]" -map "[v]" \
  -c:v libx264 -crf 18 -r 30 -movflags +faststart $OUT
printf "%s: %ss from %d clips\n" $OUT "$(ffprobe -v error -show_entries format=duration -of csv=p=0 $OUT)" $#clips
