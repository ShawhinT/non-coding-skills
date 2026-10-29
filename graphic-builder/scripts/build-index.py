#!/usr/bin/env python3
"""Build a local index.html that shows every rendered pair in a scratch folder side by side.

Usage:
    build-index.py <root> [--dirs a/b c/d ...] [--sides bad good] [--column 680] [--title "..."]

Scans each direction folder for PNGs named `NN-<concept>-<side>.png` (suffixed variants like
`NN-<concept>-<side>-5p.png` are picked up too and grouped under the same concept), pairs the
two sides, and writes `<root>/index.html` with a sidebar nav, one section per direction, each
pair shown left/right with links to the full PNG and its HTML source, and a toggle that stacks
the pair at the host column width (Medium is 680px) so the user sees it as the reader will.

Descriptions for each direction come from a `README.md` or `DESCRIPTION` file in that folder
(first line), or fall back to the folder name. Run it again after every round; it overwrites
index.html and nothing else.
"""
import argparse
import html
import re
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--dirs", nargs="*", help="direction subfolders, in display order (default: every subfolder with PNGs)")
    ap.add_argument("--sides", nargs=2, default=["bad", "good"], metavar=("LEFT", "RIGHT"))
    ap.add_argument("--column", type=int, default=680, help="host column width for the stacked toggle")
    ap.add_argument("--title", default=None)
    a = ap.parse_args()

    root = Path(a.root).resolve()
    left, right = a.sides
    pat = re.compile(rf"^(\d+)-(.+?)-({left}|{right})(-[\w-]+)?\.png$")

    if a.dirs:
        dirs = [root / d for d in a.dirs]
    else:
        dirs = sorted(p.parent for p in root.rglob("*.png") if pat.match(p.name) and not p.name.startswith("_"))
        dirs = sorted(set(dirs))

    sections = []
    for d in dirs:
        groups = {}
        for p in sorted(d.glob("*.png")):
            m = pat.match(p.name)
            if not m:
                continue
            num, concept, side, suffix = m.groups()
            key = f"{num}-{concept}{suffix or ''}"
            groups.setdefault(key, {})[side] = p
        pairs = sorted(((k, g) for k, g in groups.items() if left in g and right in g),
                       key=lambda kg: (kg[0].split("-")[0], kg[0].count("-"), kg[0]))  # base before its suffixed variants
        if not pairs:
            continue
        desc = ""
        for name in ("README.md", "DESCRIPTION"):
            f = d / name
            if f.exists():
                desc = f.read_text().strip().splitlines()[0]
                break
        sections.append((d, desc, pairs))

    title = a.title or f"{root.name}: {sum(len(s[2]) for s in sections)} pairs"
    rel = lambda p: html.escape(str(p.relative_to(root)))
    src = lambda p: rel(p.with_suffix(".html")) if p.with_suffix(".html").exists() else None

    nav, body = [], []
    for d, desc, pairs in sections:
        sid = rel(d).replace("/", "-")
        nav.append(f'<a href="#{sid}">{html.escape(d.name)} <small>{len(pairs)}</small></a>')
        cards = []
        for key, g in pairs:
            cells = []
            for side in (left, right):
                p = g[side]
                s = src(p)
                links = f'<a href="{rel(p)}" target="_blank">png</a>' + (f' · <a href="{s}" target="_blank">html</a>' if s else "")
                cells.append(f'<figure><img src="{rel(p)}" loading="lazy"><figcaption>{side} · {links}</figcaption></figure>')
            cards.append(f'<div class="pair"><h3>{html.escape(key)}</h3><div class="cells">{"".join(cells)}</div></div>')
        body.append(f'<section id="{sid}"><h2>{html.escape(d.name)}</h2><p>{html.escape(desc)}</p>{"".join(cards)}</section>')

    page = f"""<!doctype html><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>
:root{{--col:{a.column}px}}
body{{margin:0;font:15px/1.4 system-ui,sans-serif;color:#222;background:#fff;display:grid;grid-template-columns:220px 1fr}}
nav{{position:sticky;top:0;height:100vh;overflow:auto;padding:20px;border-right:1px solid #eee}}
nav a{{display:block;padding:6px 0;color:#222;text-decoration:none}} nav small{{color:#888}}
main{{padding:24px 32px;max-width:1400px}}
label{{display:block;margin:0 0 20px;color:#555}}
section{{margin-bottom:48px}} h2{{margin:0 0 4px}} p{{margin:0 0 16px;color:#666}}
.pair{{margin-bottom:28px}} h3{{font-weight:500;margin:0 0 8px;color:#444}}
.cells{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
figure{{margin:0;min-width:0}} img{{width:100%;height:auto;border:1px solid #eee;display:block}}
figcaption{{font-size:13px;color:#777;margin-top:4px}}
body.stack .cells{{grid-template-columns:1fr;max-width:var(--col)}}
</style>
<nav><strong>{html.escape(title)}</strong>{"".join(nav)}</nav>
<main>
<label><input type="checkbox" onchange="document.body.classList.toggle('stack',this.checked)"> stacked at column width ({a.column}px), as the reader sees it</label>
{"".join(body)}
</main>"""
    (root / "index.html").write_text(page)
    print(f"wrote {root / 'index.html'} with {sum(len(s[2]) for s in sections)} pairs in {len(sections)} directions")


if __name__ == "__main__":
    main()
