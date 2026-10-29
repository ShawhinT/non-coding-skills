#!/usr/bin/env python3
"""Build a labeled contact sheet from every PNG in a folder.

Usage:
    contact-sheet.py <dir> [--cols 3] [--size 500] [--out <png>]

Defaults: 3 columns, 500px thumbnails, output written to
<dir>/_contact-<dirname>.png. Files starting with "_contact" are skipped so
re-running never nests a sheet inside a sheet.

Why this exists: when several subagents each produce 3–5 mockups, reviewing
them one Read call at a time is slow and loses the side-by-side comparison
that decides which direction wins. One sheet per direction lets Shaw (and the
model) scan the whole set in a single image. See graphic-builder SKILL.md
§ "Ideating from scratch".
"""
import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Pillow is required: pip3 install pillow")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--size", type=int, default=500)
    ap.add_argument("--out")
    args = ap.parse_args()

    d = Path(args.dir).expanduser().resolve()
    files = sorted(
        p for p in d.glob("*.png") if not p.name.startswith("_contact")
    )
    if not files:
        sys.exit(f"no PNGs in {d}")

    s, pad, label_h = args.size, 20, 40
    cols = min(args.cols, len(files))
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new(
        "RGB",
        (cols * s + (cols + 1) * pad, rows * (s + label_h) + (rows + 1) * pad),
        (230, 230, 225),
    )
    draw = ImageDraw.Draw(sheet)

    for i, f in enumerate(files):
        im = Image.open(f).convert("RGB")
        im.thumbnail((s, s))
        x = pad + (i % cols) * (s + pad)
        y = pad + (i // cols) * (s + label_h + pad)
        # center the thumbnail in its cell so non-square renders don't stretch
        sheet.paste(im, (x + (s - im.width) // 2, y + (s - im.height) // 2))
        draw.text((x, y + s + 10), f.name, fill=(0, 0, 0))

    out = Path(args.out) if args.out else d / f"_contact-{d.name}.png"
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()
