#!/usr/bin/env python3
"""
Top/bottom split dashboard: posts in, dashboard out.

    python3 build_split_config.py posts.json prose.json out.html

posts.json  — the rows scrape-feed-api.js leaves on window.__feed, dumped as a
              JSON array. Each row: id, date (YYYY-MM-DD), im, re, co, sh,
              media, preview, and votes for polls. An optional "title" overrides the preview-derived
              one — do that: a 5-word title reads better than a clipped preview.

prose.json  — the words a number can't carry. All keys optional:
  {
    "window":      "Trailing 28 days, Aug 9 to Sep 5, 2026.",
    "separates_A": "<strong>What separates them:</strong> ...",   # by rate
    "separates_B": "<strong>What separates them:</strong> ...",   # by reach
    "crossread":   "<strong>Cross-read:</strong> ...",
    "dual_notes":  "<p class=\\"note\\">...</p>",
    "repurposed":  {"7500171809603010560": "No", "…": "YTC"}     # every post in the window
  }

Everything numeric — engagement rate, halves, medians, averages, max, share of
total, max/median, the dual-median intersection — is computed here. There is
no mean reach anywhere by construction: reach is fat-tailed and its mean is
not a statistic worth printing.
"""
import json, os, statistics, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
URL = "https://www.linkedin.com/feed/update/urn:li:activity:{id}/"
MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


def short_date(iso):
    y, m, d = iso.split("-")
    return f"{MON[int(m)-1]} {int(d)}"


def build(posts, prose):
    rows = []
    for p in posts:
        eng = (p.get("re") or 0) + (p.get("co") or 0) + (p.get("sh") or 0)
        im = p["im"]
        rows.append({
            "id": p["id"], "date": short_date(p["date"]), "iso": p["date"],
            "im": im, "re": p.get("re") or 0, "co": p.get("co") or 0, "sh": p.get("sh") or 0,
            "media": p.get("media", "text"), "votes": p.get("votes"), "eng": eng,
            "er": round(eng / im * 100, 2) if im else 0.0,
            "title": p.get("title") or (p.get("preview") or "")[:60].rstrip(" ,.;:") ,
        })

    n = len(rows); half = n // 2
    tot_im = sum(r["im"] for r in rows)
    med_er = statistics.median(r["er"] for r in rows)
    med_im = statistics.median(r["im"] for r in rows)
    by_rate = sorted(rows, key=lambda r: -r["er"])
    by_reach = sorted(rows, key=lambda r: -r["im"])
    top_rate, bot_rate = by_rate[:half], by_rate[half:]
    top_reach, bot_reach = by_reach[:half], by_reach[half:]
    avg = lambda rs: round(sum(r["er"] for r in rs) / len(rs), 2)
    top3 = sum(r["im"] for r in by_reach[:3])

    # by-format rollup: the one "what separates them" dimension that's free
    by_media = {}
    for r in rows:
        by_media.setdefault(r["media"], []).append(r["er"])
    media_line = ", ".join(f"{k} {round(sum(v)/len(v),2)}% across {len(v)}"
                           for k, v in sorted(by_media.items(), key=lambda kv: -len(kv[1])))

    top_rate_ids = {r["id"] for r in top_rate}
    dual = [r for r in top_reach if r["id"] in top_rate_ids]
    dual.sort(key=lambda r: -r["er"])
    switchers = sum(1 for r in top_rate if r["id"] not in {x["id"] for x in top_reach})

    COLS_A = [
      {"key": "er",    "label": "eng %",  "align": "right", "mono": True, "emphasis": True},
      {"key": "date",  "label": "date",   "align": "right", "mono": True},
      {"key": "im",    "label": "impr",   "align": "right", "mono": True},
      {"key": "re",    "label": "re",     "align": "right", "mono": True},
      {"key": "co",    "label": "co",     "align": "right", "mono": True},
      {"key": "sh",    "label": "sh",     "align": "right", "mono": True},
      {"key": "media", "label": "format", "mono": True, "tag": True},
      {"key": "rep",   "label": "repurposed", "mono": True, "tag": True, "tag_variant_key": "rep_variant"},
      {"key": "title", "label": "post",   "link": URL},
    ]
    COLS_B = [dict(c) for c in [COLS_A[2], COLS_A[1], COLS_A[0]] + COLS_A[3:]]
    COLS_B[0]["emphasis"], COLS_B[2]["emphasis"] = True, False
    COLS_D = [dict(c) for c in COLS_A]

    rep = prose.get("repurposed", {})

    def fmt(rs):
        out = []
        for r in rs:
            v = rep.get(r["id"], "?")
            # `_f` carries the unformatted values the filter compares against;
            # the visible cells stay formatted ("3.62%", "1,091").
            # A poll's votes aren't in its rate, so they ride in the format cell.
            media = f'{r["media"]} · {r["votes"]} votes' if r.get("votes") else r["media"]
            out.append({**r, "media": media, "er": f'{r["er"]:.2f}%', "im": f'{r["im"]:,}',
                        "_f": {"er": r["er"], "im": r["im"]},
                        "rep": v, "rep_variant": "warn" if v == "No" else "hot"})
        return out

    dual_rows = fmt(dual)

    reach_prose = prose.get("separates_B") or (
        f"<strong>What separates them:</strong> whether the post escaped the immediate network. "
        f'Read {by_reach[0]["date"]} in absolute terms: {by_reach[0]["eng"]} interactions against '
        f'{sum(r["eng"] for r in top_rate)} across the entire top-rate half. Its {by_reach[0]["er"]:.2f}% '
        f"is measuring audience fit with a cold crowd, not post quality.")
    rate_prose = prose.get("separates_A") or (
        f"<strong>What separates them:</strong> by format, {media_line}. "
        f"Top half averages {avg(top_rate)}%, bottom half {avg(bot_rate)}%.")
    crossread = prose.get("crossread") or (
        f"<strong>Cross-read:</strong> {switchers} of {half} posts change halves when the sort flips. "
        f"{len(dual)} post{'s' if len(dual) != 1 else ''} clear{'s' if len(dual) == 1 else ''} the median on both.")

    cfg = {
      "title": "LinkedIn top/bottom split",
      "subtitle": f"{prose.get('window', '')} {n} original posts, pulled from the Voyager feed API.".strip(),
      "footer": "engagement rate = (reactions + comments + shares) / impressions · excludes clicks and saves · aibuilder.academy",
      # Both splits sort on these two metrics, so they are the two worth
      # filtering. Hides rows only — see filters_html in the renderer.
      "filters": [
        {"key": "er", "label": "eng rate", "suffix": " %", "step": "0.01"},
        {"key": "im", "label": "impressions", "step": "1"},
      ],
      "toggle": {
        "kpi_prefix": [{"v": f"{tot_im:,}", "l": "impressions"}],
        "modes": [
          {"key": "A", "button": "By engagement rate",
           "kpis": [{"v": f"{avg(top_rate)}%", "l": "top half avg"},
                    {"v": f"{avg(bot_rate)}%", "l": "bottom half avg"},
                    {"v": f"{round(med_er, 2)}%", "l": "median rate"},
                    {"v": f"{round(avg(top_rate)/avg(bot_rate),1)}x", "l": "spread"}],
           "tables": [{"label": "Top half by engagement rate", "columns": COLS_A, "rows": fmt(top_rate)},
                      {"label": "Bottom half by engagement rate", "columns": COLS_A, "rows": fmt(bot_rate)}],
           "prose": rate_prose},
          {"key": "B", "button": "By reach",
           "kpis": [{"v": f"{int(med_im):,}", "l": "median reach"},
                    {"v": f'{by_reach[0]["im"]:,}', "l": "max reach"},
                    {"v": f'{round(by_reach[0]["im"]/tot_im*100,1)}%', "l": "top post share"},
                    {"v": f'{round(by_reach[0]["im"]/med_im,1)}x', "l": "max / median"}],
           "tables": [{"label": "Top half by reach", "columns": COLS_B, "rows": fmt(top_reach)},
                      {"label": "Bottom half by reach", "columns": COLS_B, "rows": fmt(bot_reach)}],
           "prose": reach_prose},
        ],
      },
      "sections": [
        {"type": "prose", "html": crossread},
        {"type": "divider"},
        {"type": "table",
         "heading": "Top half of both splits",
         "sub": f"Cleared the median on reach and on engagement rate. {len(dual)} of {n}.",
         "columns": COLS_D, "rows": dual_rows,
         "note": prose.get("dual_notes", "")},
      ],
      "_stats": {"n": n, "tot_im": tot_im, "med_er": round(med_er, 2), "med_im": med_im,
                 "top1_share": round(by_reach[0]["im"]/tot_im*100, 1),
                 "top3_share": round(top3/tot_im*100, 1),
                 "by_media": media_line, "dual": [r["id"] for r in dual], "switchers": switchers},
    }
    return cfg


def main():
    if len(sys.argv) != 4:
        sys.exit("usage: build_split_config.py posts.json prose.json out.html")
    posts = json.load(open(sys.argv[1]))
    prose = json.load(open(sys.argv[2])) if os.path.exists(sys.argv[2]) else {}
    cfg = build(posts, prose)
    cfg_path = os.path.splitext(sys.argv[3])[0] + ".config.json"
    json.dump(cfg, open(cfg_path, "w"), indent=1)
    subprocess.run([sys.executable, os.path.join(HERE, "aba_dashboard.py"), cfg_path, sys.argv[3]], check=True)
    print(json.dumps(cfg["_stats"], indent=1))


if __name__ == "__main__":
    main()
