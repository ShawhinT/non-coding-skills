#!/usr/bin/env python3
"""Revenue-over-time line chart in the Medium/TDE style.

Usage as a module:
    from cohort_chart import plot_series
    plot_series([("Cohort 1", 10798, "2024-11-08"), ...], "out.png",
                title="AI Builders Bootcamp revenue by cohort",
                subtitle="8 cohorts · $87,667 lifetime · Nov 2024 – Feb 2026",
                ylabel="Revenue per cohort (USD)", below={"Cohort 2"})

Usage from the shell (JSON list of [label, value, iso_date]):
    python cohort_chart.py data.json out.png --title "..." --subtitle "..." --below "Cohort 2,Cohort 7"

Styling encodes what Shaw has asked for: white background, Medium green series, bold title with a
gray subtitle placed via fig.text (ax.set_title collides with a subtitle), $Nk ticks on 5k steps,
dashed average line at 80% opacity labeled past the right edge, value+label on every point, and an
x-axis that starts a few weeks before the first tick so its label clears the y-axis.
`below` names points whose labels go under the dot (use when a label would sit on the average line
or on a steep neighboring segment).
"""
import argparse, datetime as dt, json, sys
import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator

GREEN, INK, GRAY, RULE = "#1a8917", "#242424", "#6b6b6b", "#cfcfcf"


def plot_series(points, out, title, subtitle="", ylabel="Revenue (USD)", below=(),
                show_avg=True, tick_step=5000, ymax=None):
    labels = [p[0] for p in points]
    vals = [p[1] for p in points]
    dates = [dt.date.fromisoformat(p[2]) for p in points]
    below = set(below)
    avg = sum(vals) / len(vals)
    ymax = ymax or (max(vals) * 1.28 // tick_step + 1) * tick_step

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 14})
    fig, ax = plt.subplots(figsize=(14, 6.2), dpi=200)
    x0 = dates[0] - dt.timedelta(days=60)
    x1 = dates[-1] + dt.timedelta(days=45)
    if show_avg:
        ax.axhline(avg, color=INK, lw=2, ls="--", alpha=0.8, zorder=2)
        ax.text(x1, avg, f"  Avg ${avg:,.0f}", va="center", ha="left", fontsize=12, color=INK,
                alpha=0.8, clip_on=False)
    ax.plot(dates, vals, color=GREEN, lw=3, marker="o", ms=11, mfc="white", mew=3, zorder=3)
    for lab, v, d in zip(labels, vals, dates):
        up = lab not in below
        ax.annotate(f"${v:,.0f}", (d, v), textcoords="offset points", xytext=(0, 16 if up else -30),
                    ha="center", fontsize=13, color=INK, fontweight="bold")
        ax.annotate(lab, (d, v), textcoords="offset points", xytext=(0, 33 if up else -46),
                    ha="center", fontsize=11, color=GRAY)
    ax.set_ylim(0, ymax)
    ax.yaxis.set_major_locator(MultipleLocator(tick_step))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v/1000:.0f}k"))
    ax.set_ylabel(ylabel, color=GRAY, labelpad=12)
    ax.set_xlim(x0, x1)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(RULE)
    ax.tick_params(colors=GRAY)
    ax.grid(axis="y", color="#ececec", lw=1, zorder=0)
    fig.text(0.075, 0.95, title, fontsize=20, fontweight="bold", color=INK)
    if subtitle:
        fig.text(0.075, 0.905, subtitle, fontsize=13, color=GRAY)
    fig.tight_layout(rect=(0, 0, 0.94, 0.88))
    fig.savefig(out, facecolor="white")
    return avg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data"); ap.add_argument("out")
    ap.add_argument("--title", required=True); ap.add_argument("--subtitle", default="")
    ap.add_argument("--ylabel", default="Revenue (USD)")
    ap.add_argument("--below", default="", help="comma-separated labels whose text goes under the dot")
    a = ap.parse_args()
    pts = json.load(open(a.data))
    below = [s.strip() for s in a.below.split(",") if s.strip()]
    avg = plot_series(pts, a.out, a.title, a.subtitle, a.ylabel, below)
    print(a.out, f"avg={avg:,.0f}")


if __name__ == "__main__":
    sys.exit(main())
