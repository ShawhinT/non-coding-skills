"""Seek an HTML animation to chosen times, screenshot each, and print element boxes.

Uses the same pause-and-seek method as render.py, so a snap at t matches the
rendered frame at t. Fonts are awaited first, so layout-dependent helpers
(aim(), placePills()) have already run.

Usage:
  uv run --project ~/.claude/skills/animation-builder python \
    ~/.claude/skills/animation-builder/scripts/snap.py scene.html /tmp/out 1.5,4.2 '#send' '.lbl-cowork'
Writes /tmp/out-1.5.png, /tmp/out-4.2.png and prints [x, y, w, h, cx, cy] per selector.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

html, prefix, times = Path(sys.argv[1]), sys.argv[2], [float(x) for x in sys.argv[3].split(',')]
sels = sys.argv[4:]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(html.resolve().as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
    pg.evaluate("() => { for (const a of document.getAnimations()) a.pause(); }")
    for s in sels:
        r = pg.evaluate("(s)=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return [r.x,r.y,r.width,r.height,r.x+r.width/2,r.y+r.height/2].map(Math.round)}", s)
        print(s, r)
    for t in times:
        pg.evaluate("(t)=>{for(const a of document.getAnimations()) a.currentTime=t}", t * 1000)
        pg.screenshot(path=f"{prefix}-{t}.png")
    b.close()
