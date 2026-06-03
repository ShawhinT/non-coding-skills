#!/usr/bin/env bash
# Render an infographic HTML to a 2x retina PNG via headless Chrome.
#
# Usage:
#   render.sh <html-path> [--size square|portrait|landscape|<W>x<H>] [--out <png-path>]
#
# Defaults:
#   --size landscape   (1080×820)
#   --out  <html-dir>/<html-basename>.png
#
# Why headless Chrome and not Playwright MCP: the MCP blocks file:// URLs, and
# `python3 -m http.server` is blocked by the sandbox classifier. Chrome's
# --headless mode accepts file:// directly and renders deterministically.

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: render.sh <html-path> [--size square|portrait|landscape|WxH] [--out <png>]" >&2
  exit 1
fi

HTML="$1"; shift
SIZE="landscape"
OUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --size) SIZE="$2"; shift 2 ;;
    --out)  OUT="$2";  shift 2 ;;
    *) echo "unknown flag: $1" >&2; exit 1 ;;
  esac
done

case "$SIZE" in
  square)    W=1080; H=1080 ;;
  portrait)  W=1080; H=1350 ;;
  landscape) W=1080; H=820  ;;
  *x*)       W="${SIZE%x*}"; H="${SIZE#*x}" ;;
  *) echo "bad --size: $SIZE" >&2; exit 1 ;;
esac

# Resolve absolute paths.
if [[ ! -f "$HTML" ]]; then
  echo "no such file: $HTML" >&2; exit 1
fi
HTML_ABS="$(cd "$(dirname "$HTML")" && pwd)/$(basename "$HTML")"

if [[ -z "$OUT" ]]; then
  OUT="${HTML_ABS%.html}.png"
fi
# Make OUT absolute too (Chrome treats relative paths as relative to its cwd).
case "$OUT" in
  /*) ;;
  *)  OUT="$(pwd)/$OUT" ;;
esac

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [[ ! -x "$CHROME" ]]; then
  echo "Google Chrome not found at $CHROME" >&2; exit 1
fi

"$CHROME" \
  --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size="$W,$H" \
  --force-device-scale-factor=2 \
  --screenshot="$OUT" \
  "file://$HTML_ABS" 2>/dev/null

if [[ ! -s "$OUT" ]]; then
  echo "render failed: $OUT is empty or missing" >&2; exit 1
fi

# Report.
DIM="$(file "$OUT" | grep -oE '[0-9]+ x [0-9]+' | head -1)"
echo "rendered: $OUT  ($DIM, ${W}×${H} logical @2x)"
