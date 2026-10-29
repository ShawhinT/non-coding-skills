"""Drive an interactive HTML mock headlessly, then screenshot it and report errors.

Use it to verify a clickable demo (an interactive UI mock) the way a person would use it:
click things, scroll, press keys, then look at one frame. Runs in the skill's own uv project.

Usage:
  uv run --project ~/.claude/skills/animation-builder python \
    ~/.claude/skills/animation-builder/scripts/interact.py page.html /tmp/out.png \
    --viewport 1440x900 --click '#chk-ravi' --click '#next' --wheel '#gridwrap:200' --key ArrowRight \
    --text '#status'

Actions run in the order given. `--viewport 960x600` approximates 150% browser zoom in a
1440x900 window (browser zoom shrinks the CSS viewport; the layout must reflow, not scale).
Prints page errors (uncaught exceptions) and any `--text` selectors' inner text, then saves
the screenshot. Exit code 1 if a page error occurred.
"""
import argparse
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("html"); ap.add_argument("out")
ap.add_argument("--viewport", default="1440x900")
ap.add_argument("--click", action="append", default=[], help="selector to click (repeatable)")
ap.add_argument("--wheel", action="append", default=[], help="'selector:dy' — hover selector, wheel dy px")
ap.add_argument("--key", action="append", default=[], help="key to press (repeatable)")
ap.add_argument("--text", action="append", default=[], help="selector whose inner text to print")
ap.add_argument("--count", action="append", default=[], help="selector whose match count to print")
a = ap.parse_args()
w, h = (int(x) for x in a.viewport.lower().split("x"))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": w, "height": h})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(Path(a.html).resolve().as_uri()); pg.wait_for_load_state("networkidle")
    # replay actions in the order they appear on the command line
    flags = {"--click": "click", "--wheel": "wheel", "--key": "key"}
    actions = [(flags[f], sys.argv[i + 1]) for i, f in enumerate(sys.argv) if f in flags]
    for kind, v in actions:
        if kind == "click": pg.click(v)
        elif kind == "wheel":
            sel, dy = v.rsplit(":", 1); pg.hover(sel); pg.mouse.wheel(0, int(dy))
        elif kind == "key": pg.keyboard.press(v)
        pg.wait_for_timeout(60)
    for s in a.text: print(f"{s}: {pg.inner_text(s).replace(chr(10), ' ')}")
    for s in a.count: print(f"{s}: {pg.locator(s).count()} matches")
    pg.screenshot(path=a.out)
    print("screenshot:", a.out)
    print("errors:", errs or "none")
    b.close()
    sys.exit(1 if errs else 0)
