#!/usr/bin/env python3
"""
ABA dashboard generator.

Data in, styled HTML out. The brand shell (palette, type scale, table rules,
toggle behaviour) lives here as ONE constant, so a dashboard is a config file
rather than a page of hand-written markup that drifts from the last one.

    python3 aba_dashboard.py config.json out.html

The config is JSON (or a Python dict, if importing `render`):

{
  "title":    "LinkedIn audience",
  "subtitle": "Trailing 7 days ...",
  "footer":   "engagement rate = ... · aibuilder.academy",
  "kpis":     [{"v": "143", "l": "named people"}, ...],

  # Optional. Two modes sharing one table pair, switched by a toggle.
  # Each mode swaps its own KPIs (after the first), tables and prose.
  "toggle": {
    "kpi_prefix": [{"v": "88,820", "l": "impressions"}],   # KPIs kept across modes
    "modes": [
      {"key": "A", "button": "By engagement rate",
       "kpis":   [{"v": "3.36%", "l": "top half avg"}, ...],
       "tables": [{"label": "Top half by engagement rate", "columns": [...], "rows": [...]},
                  {"label": "Bottom half by engagement rate", "columns": [...], "rows": [...]}],
       "prose":  "<strong>What separates them:</strong> ..."}
    ]
  },

  # Rendered in order after the toggle block.
  "sections": [
    {"type": "table",   "heading": "...", "sub": "...", "columns": [...], "rows": [...],
     "note": "<p>...</p>"},
    {"type": "prose",   "heading": "...", "html": "..."},
    {"type": "details", "summary": "...", "columns": [...], "rows": [...]},
    {"type": "defs",    "heading": "...", "rows": [{"term": "...", "html": "..."}]},
    {"type": "divider"}
  ]
}

A column is {"key", "label", "align": "left|right", "mono": bool, "tag": bool,
"emphasis": bool, "sub": "<other key>", "link": "https://…{key}…"}.
Rows are dicts keyed by column key. `sub` renders a second muted line under the
cell — that is how a name carries its headline without a second column.

Everything is escaped except keys ending in `_html`, `note`, `prose`, and the
`defs` bodies, which are trusted markup by design.
"""

import html
import json
import sys

SHELL_CSS = """
:root {
  color-scheme: light;
  --aba-primary: #087CA7;
  --aba-secondary: #B80C09;
  --aba-accent: #7DB72A;
  --aba-warning: #B17A0E;
  --surface: #FAFAF7;
  --surface-card: #FFFFFF;
  --surface-tint: rgba(1, 4, 19, 0.04);
  --fg-1: rgba(1, 4, 19, 1);
  --fg-2: rgba(1, 4, 19, 0.8);
  --fg-3: rgba(1, 4, 19, 0.65);
  --fg-4: rgba(1, 4, 19, 0.5);
  --line: rgba(1, 4, 19, 0.08);
  --line-strong: rgba(1, 4, 19, 0.14);
  --font-display: 'Manrope', system-ui, sans-serif;
  --font-body: 'Libre Franklin', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, monospace;
  --radius-lg: 0.5rem;
  --radius-card: 1rem;
  --radius-field: 2rem;
  --dur-base: 200ms;
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
}
* { box-sizing: border-box; }
html { background: var(--surface); }
body {
  margin: 0 auto; max-width: 900px; padding: 32px 24px 48px;
  background: var(--surface); color: var(--fg-1);
  font-family: var(--font-body); font-size: 16px; line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
h1, h2 { font-family: var(--font-display); font-weight: 800; line-height: 1.1; margin: 0; }
h1 { font-size: 2rem; letter-spacing: -0.02em; margin-bottom: 6px; }
h2 { font-size: 1.375rem; letter-spacing: -0.01em; margin-bottom: 4px; }
.sub { color: var(--fg-3); font-size: 0.9375rem; margin-bottom: 24px; }
.kpis { display: grid; grid-template-columns: repeat(var(--kpi-n, 5), minmax(0, 1fr)); gap: 10px; margin-bottom: 30px; }
.kpi { background: var(--surface-card); border: 1px solid var(--line); border-radius: var(--radius-card); padding: 12px 14px; min-width: 0; }
.kpi .v { font-family: var(--font-display); font-weight: 800; font-size: 1.25rem; letter-spacing: -0.02em; line-height: 1.1; }
.kpi .l { font-family: var(--font-mono); font-size: 0.625rem; color: var(--fg-4); letter-spacing: 0.03em; margin-top: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.toggle { display: inline-flex; gap: 8px; margin-bottom: 16px; }
.toggle button {
  font-family: var(--font-display); font-weight: 700; font-size: 0.875rem;
  padding: 10px 22px; border-radius: var(--radius-field);
  border: 1px solid var(--line-strong); background: transparent; color: var(--fg-2); cursor: pointer;
  transition: background var(--dur-base) var(--ease-standard), color var(--dur-base) var(--ease-standard), border-color var(--dur-base) var(--ease-standard);
}
.toggle button:hover { border-color: var(--aba-primary); color: var(--aba-primary); }
.toggle button[aria-pressed="true"] { background: var(--aba-primary); border-color: var(--aba-primary); color: #fff; }
/* Stacked, never side by side: the title column does the interpretive work and
   two columns compress it into uselessness. */
.halves { display: grid; grid-template-columns: minmax(0, 1fr); gap: 32px; }
.label { font-family: var(--font-display); font-weight: 700; font-size: 1rem; letter-spacing: -0.01em; margin: 0 0 8px; }
table { width: 100%; border-collapse: collapse; font-size: 0.8125rem; }
th {
  font-family: var(--font-mono); font-weight: 500; font-size: 0.6875rem;
  color: var(--fg-4); letter-spacing: 0.04em; text-align: left;
  padding: 7px 6px; border-bottom: 1px solid var(--line-strong); white-space: nowrap;
}
th.r, td.r { text-align: right; }
td { padding: 9px 6px; border-bottom: 1px solid var(--line); color: var(--fg-3); font-size: 0.8125rem; vertical-align: top; }
td.m { font-family: var(--font-mono); font-size: 0.75rem; white-space: nowrap; }
tr:hover td { background: var(--surface-tint); }
.nm { color: var(--fg-1); font-weight: 600; }
.hl { color: var(--fg-4); font-size: 0.75rem; display: block; margin-top: 2px; }
.tag {
  display: inline-block; font-family: var(--font-mono); font-size: 0.625rem;
  color: var(--fg-3); background: var(--surface-tint);
  border-radius: var(--radius-lg); padding: 2px 7px; letter-spacing: 0.02em; white-space: nowrap;
}
.tag.hot { background: rgba(8,124,167,0.12); color: var(--aba-primary); font-weight: 600; }
.tag.warn { background: rgba(184,12,9,0.10); color: var(--aba-secondary); font-weight: 600; }
.tag.muted { background: rgba(1,4,19,0.05); color: var(--fg-4); font-style: italic; white-space: normal; }
.filters {
  display: flex; flex-wrap: wrap; align-items: flex-end; gap: 14px;
  background: var(--surface-card); border: 1px solid var(--line);
  border-radius: var(--radius-card); padding: 14px 16px; margin-bottom: 18px;
}
.filters .fgrp { display: flex; flex-direction: column; gap: 5px; }
.filters .flab { font-family: var(--font-mono); font-size: 0.625rem; color: var(--fg-4); letter-spacing: 0.03em; }
.filters .frow { display: flex; align-items: center; gap: 6px; }
.filters input {
  width: 92px; padding: 6px 9px; font-family: var(--font-mono); font-size: 0.75rem;
  color: var(--fg-1); background: var(--surface); border: 1px solid var(--line-strong);
  border-radius: var(--radius-lg); transition: border-color var(--dur-base) var(--ease-standard);
}
.filters input:focus { outline: none; border-color: var(--aba-primary); }
.filters .dash { color: var(--fg-4); font-family: var(--font-mono); font-size: 0.75rem; }
.filters .fcount {
  margin-left: auto; font-family: var(--font-mono); font-size: 0.6875rem;
  color: var(--fg-3); letter-spacing: 0.02em; white-space: nowrap;
}
.filters .fcount.on { color: var(--aba-primary); font-weight: 600; }
.filters button.reset {
  font-family: var(--font-display); font-weight: 700; font-size: 0.75rem;
  padding: 7px 16px; border-radius: var(--radius-field);
  border: 1px solid var(--line-strong); background: transparent; color: var(--fg-3); cursor: pointer;
  transition: border-color var(--dur-base) var(--ease-standard), color var(--dur-base) var(--ease-standard);
}
.filters button.reset:hover { border-color: var(--aba-secondary); color: var(--aba-secondary); }
tr.hid { display: none; }
.empty { color: var(--fg-4); font-size: 0.875rem; font-style: italic; padding: 10px 6px; }
.divider { height: 1px; background: var(--line); margin: 38px 0 26px; border: 0; }
.note { font-size: 0.9375rem; color: var(--fg-3); margin: 16px 0 0; }
.note strong { color: var(--fg-1); font-weight: 600; }
ul.note { padding-left: 20px; }
ul.note li { margin-bottom: 6px; }
.card { background: var(--surface-card); border: 1px solid var(--line); border-radius: var(--radius-card); padding: 18px 20px; margin-top: 14px; }
.card table td { border-bottom: 1px solid var(--line); }
.card table tr:last-child td { border-bottom: 0; }
details { margin-top: 10px; }
summary { cursor: pointer; font-family: var(--font-mono); font-size: 0.75rem; color: var(--fg-4); letter-spacing: 0.02em; padding: 6px 0; }
summary:hover { color: var(--aba-primary); }
.foot {
  font-family: var(--font-mono); font-size: 0.6875rem; color: var(--fg-4);
  letter-spacing: 0.02em; margin-top: 40px; padding-top: 16px;
  border-top: 1px solid var(--line); text-align: center;
}
"""

FONTS = ("https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800"
         "&family=Libre+Franklin:ital,wght@0,400;0,500;0,600;1,400"
         "&family=JetBrains+Mono:wght@400;500;600&display=swap")


def esc(v):
    return html.escape("" if v is None else str(v), quote=True)


def _cell(row, col):
    key = col["key"]
    raw = row.get(key, "")
    val = esc(raw)

    if col.get("link"):
        href = esc(col["link"].format(**{k: str(v) for k, v in row.items()}))
        val = f'<a href="{href}" target="_blank" rel="noopener">{val}</a>'
    if col.get("tag"):
        variant = row.get(col.get("tag_variant_key", ""), col.get("tag_variant", ""))
        cls = f"tag {variant}".strip()
        val = f'<span class="{esc(cls)}">{val}</span>'
    elif col.get("emphasis"):
        val = f'<span class="nm">{val}</span>'

    if col.get("sub"):
        subv = row.get(col["sub"], "")
        if subv:
            val += f'<span class="hl">{esc(subv)}</span>'

    if raw in ("", None) and not col.get("tag"):
        val = "&mdash;"

    classes = []
    if col.get("align") == "right":
        classes.append("r")
    if col.get("mono"):
        classes.append("m")
    cls = f' class="{" ".join(classes)}"' if classes else ""
    return f"<td{cls}>{val}</td>"


def table_html(columns, rows):
    head = "".join(
        f'<th class="{"r" if c.get("align") == "right" else ""}">{esc(c.get("label", c["key"]))}</th>'
        for c in columns
    )
    parts = []
    for r in rows:
        # Raw numerics for the client-side filter. Cells carry formatted text
        # ("3.62%", "1,091"), so the unformatted values ride along separately
        # rather than being parsed back out of the markup.
        f = r.get("_f")
        attr = f" data-f='{json.dumps(f)}'" if f else ""
        parts.append(f"<tr{attr}>" + "".join(_cell(r, c) for c in columns) + "</tr>")
    body = "".join(parts)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def kpis_html(kpis):
    return "".join(
        f'<div class="kpi"><div class="v">{esc(k["v"])}</div>'
        f'<div class="l">{esc(k["l"])}</div></div>'
        for k in kpis
    )


def section_html(s):
    t = s.get("type", "table")
    if t == "divider":
        return '<hr class="divider">'
    out = []
    if s.get("heading"):
        out.append(f'<h2>{esc(s["heading"])}</h2>')
    if s.get("sub"):
        out.append(f'<div class="sub" style="margin-bottom:14px">{esc(s["sub"])}</div>')

    if t == "table":
        out.append(table_html(s["columns"], s["rows"]))
    elif t == "prose":
        out.append(f'<p class="note">{s["html"]}</p>')
    elif t == "details":
        out.append(
            f'<details><summary>{esc(s["summary"])}</summary>'
            f'<div style="margin-top:8px">{table_html(s["columns"], s["rows"])}</div></details>'
        )
    elif t == "defs":
        body = "".join(
            f'<tr><td style="width:150px"><span class="nm">{esc(d["term"])}</span></td>'
            f'<td>{d["html"]}</td></tr>'
            for d in s["rows"]
        )
        out.append(f'<div class="card"><table><tbody>{body}</tbody></table></div>')

    if s.get("note"):
        out.append(f'<p class="note">{s["note"]}</p>')
    return "\n".join(out)


FILTER_JS = """
// Row-level filter. Hides rows only — every summary number on the page is
// computed over the full window by the builder and deliberately does not move,
// so the halves keep meaning what their labels say.
function fBounds() {
  const b = {};
  document.querySelectorAll('#filters input').forEach(i => {
    const v = i.value.trim();
    if (v === '') return;
    const n = Number(v);
    if (!isFinite(n)) return;
    (b[i.dataset.fkey] = b[i.dataset.fkey] || {})[i.dataset.fbound] = n;
  });
  return b;
}
function applyFilters() {
  const b = fBounds();
  const active = Object.keys(b).length > 0;
  document.querySelectorAll('table').forEach(tbl => {
    const body = tbl.tBodies[0];
    if (!body) return;
    let shown = 0, total = 0;
    body.querySelectorAll('tr[data-f]').forEach(tr => {
      total++;
      let ok = true;
      let d = {};
      try { d = JSON.parse(tr.dataset.f); } catch (e) {}
      for (const k in b) {
        const v = d[k];
        if (typeof v !== 'number') { ok = false; break; }
        if (b[k].min !== undefined && v < b[k].min) { ok = false; break; }
        if (b[k].max !== undefined && v > b[k].max) { ok = false; break; }
      }
      tr.classList.toggle('hid', !ok);
      if (ok) shown++;
    });
    // A table emptied by the filter should say so rather than look broken.
    let ph = body.querySelector('tr.phRow');
    if (total > 0 && shown === 0) {
      if (!ph) {
        ph = document.createElement('tr');
        ph.className = 'phRow';
        ph.innerHTML = '<td class="empty" colspan="' +
          (tbl.tHead ? tbl.tHead.rows[0].cells.length : 9) + '">No posts match this filter.</td>';
        body.appendChild(ph);
      }
    } else if (ph) { ph.remove(); }
  });
  const scope = document.getElementById('halves') || document;
  const rows = scope.querySelectorAll('tr[data-f]');
  let vis = 0;
  rows.forEach(tr => { if (!tr.classList.contains('hid')) vis++; });
  const c = document.getElementById('fCount');
  if (c) {
    c.textContent = active ? ('showing ' + vis + ' of ' + rows.length + ' posts')
                           : (rows.length + ' posts');
    c.classList.toggle('on', active);
  }
}
function wireFilters() {
  document.querySelectorAll('#filters input').forEach(i => {
    i.addEventListener('input', applyFilters);
  });
  const r = document.getElementById('fReset');
  if (r) r.onclick = () => {
    document.querySelectorAll('#filters input').forEach(i => { i.value = ''; });
    applyFilters();
  };
}
"""


def filters_html(filters):
    """Min/max number boxes per declared metric.

    Bounds stay empty by default and an empty box means 'no bound', so the page
    opens showing everything. The filter only ever hides rows: medians, halves
    and averages are computed over the full window by the builder and do NOT
    re-derive here, because a post belongs to the top half by beating the real
    median, not by beating whatever survived a filter. The counter states the
    visible subset so that distinction is never ambiguous on screen.
    """
    groups = []
    for f in filters:
        step = f.get("step", "any")
        suf = f.get("suffix", "")
        groups.append(
            f'<div class="fgrp"><span class="flab">{esc(f["label"])}{esc(suf)}</span>'
            f'<div class="frow">'
            f'<input type="number" step="{esc(step)}" placeholder="min" '
            f'data-fkey="{esc(f["key"])}" data-fbound="min" aria-label="{esc(f["label"])} minimum">'
            f'<span class="dash">&ndash;</span>'
            f'<input type="number" step="{esc(step)}" placeholder="max" '
            f'data-fkey="{esc(f["key"])}" data-fbound="max" aria-label="{esc(f["label"])} maximum">'
            f'</div></div>'
        )
    return (
        '<div class="filters" id="filters">' + "".join(groups) +
        '<button class="reset" id="fReset" type="button">Reset</button>'
        '<span class="fcount" id="fCount"></span></div>'
    )


def render(cfg):
    kpi_static = cfg.get("kpis", [])
    tog = cfg.get("toggle")

    n_kpi = len(kpi_static)
    if tog:
        n_kpi = len(tog.get("kpi_prefix", [])) + len(tog["modes"][0].get("kpis", []))

    head = [
        f'<h1>{esc(cfg["title"])}</h1>',
        f'<div class="sub">{cfg.get("subtitle_html") or esc(cfg.get("subtitle", ""))}</div>',
        f'<div class="kpis" style="--kpi-n:{n_kpi}">{kpis_html(kpi_static) if not tog else ""}</div>',
    ]

    body, script = [], ""
    if tog:
        buttons = "".join(
            f'<button data-mode="{esc(m["key"])}" aria-pressed="{"true" if i == 0 else "false"}">'
            f'{esc(m["button"])}</button>'
            for i, m in enumerate(tog["modes"])
        )
        body.append(
            f'<div class="toggle" role="group" aria-label="View selector">{buttons}</div>'
            + (filters_html(cfg["filters"]) if cfg.get("filters") else "")
            + '<div class="halves" id="halves" style="margin-top:22px"></div>'
            '<p class="note" id="modeProse"></p>'
        )
        modes = {}
        for m in tog["modes"]:
            modes[m["key"]] = {
                "kpis": kpis_html(tog.get("kpi_prefix", [])) + kpis_html(m.get("kpis", [])),
                "tables": "".join(
                    f'<div><p class="label">{esc(t["label"])}</p>{table_html(t["columns"], t["rows"])}</div>'
                    for t in m.get("tables", [])
                ),
                "prose": m.get("prose", ""),
            }
        script = (
            "<script>\nconst MODES = " + json.dumps(modes) + ";\n"
            "const KEYS = " + json.dumps([m["key"] for m in tog["modes"]]) + ";\n"
            "const SKEY = " + json.dumps("abadash_" + cfg["title"].lower().replace(" ", "_")) + ";\n"
            """function render(k) {
  if (!MODES[k]) k = KEYS[0];
  document.querySelector(".kpis").innerHTML = MODES[k].kpis;
  document.getElementById("halves").innerHTML = MODES[k].tables;
  document.getElementById("modeProse").innerHTML = MODES[k].prose;
  document.querySelectorAll(".toggle button").forEach(b =>
    b.setAttribute("aria-pressed", b.dataset.mode === k));
  if (typeof applyFilters === "function") applyFilters();
  try { localStorage.setItem(SKEY, k); } catch (e) {}
}
document.querySelectorAll(".toggle button").forEach(b =>
  b.onclick = () => render(b.dataset.mode));
let saved = KEYS[0];
try { saved = localStorage.getItem(SKEY) || KEYS[0]; } catch (e) {}
"""
            + (FILTER_JS + "wireFilters();\n" if cfg.get("filters") else "")
            + """render(saved);
</script>"""
        )

    if cfg.get("filters") and not tog:
        body.insert(0, filters_html(cfg["filters"]))
        script = "<script>\n" + FILTER_JS + "wireFilters();\napplyFilters();\n</script>"

    for s in cfg.get("sections", []):
        body.append(section_html(s))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(cfg["title"])}</title>
<link href="{FONTS}" rel="stylesheet">
<style>{SHELL_CSS}</style>
</head>
<body>

{chr(10).join(head)}

{chr(10).join(body)}

<p class="foot">{esc(cfg.get("footer", "aibuilder.academy"))}</p>
{script}
</body>
</html>
"""


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: aba_dashboard.py <config.json> <out.html>")
    with open(sys.argv[1]) as f:
        cfg = json.load(f)
    with open(sys.argv[2], "w") as f:
        f.write(render(cfg))
    print(f"wrote {sys.argv[2]}")


if __name__ == "__main__":
    main()
