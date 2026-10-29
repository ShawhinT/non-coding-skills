#!/usr/bin/env python3
"""Render a self-contained HTML file to a PNG with headless Chromium (Playwright).

Usage:
    python render_png.py page.html out.png [--width 2000] [--height 820] [--scale 2]

The HTML's <body> should set its own width/height to match --width/--height so nothing
overflows; relative asset paths (e.g. ../assets/avatar.png) resolve against the HTML file.
Exports at --scale device pixels per CSS pixel (2 = retina-crisp on Medium).
"""
import argparse, os, sys
from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=2000)
    ap.add_argument("--height", type=int, default=820)
    ap.add_argument("--scale", type=float, default=2)
    ap.add_argument("--wait", type=int, default=1800, help="ms to wait for web fonts")
    a = ap.parse_args()
    path = os.path.abspath(a.html)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": a.width, "height": a.height}, device_scale_factor=a.scale)
        pg.goto("file://" + path)
        pg.wait_for_timeout(a.wait)
        pg.screenshot(path=a.out)
        b.close()
    print(a.out, f"{int(a.width*a.scale)}x{int(a.height*a.scale)}")


if __name__ == "__main__":
    sys.exit(main())
