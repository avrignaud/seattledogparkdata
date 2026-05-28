#!/usr/bin/env python3
"""
Build docs/images/enforcement-hero.png — a single shareable "hero" graphic for
the enforcement story, for use in email / social. It encodes the three headline
points: falling output, rising cost per citation, and the unchanged first-offense
mix. Data is read from data/enforcement-year-metrics.csv so the image stays in
sync with the page.

Run from repo root:  .venv/bin/python scripts/build_hero_image.py
"""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
METRICS = ROOT / "data" / "enforcement-year-metrics.csv"
OUT = ROOT / "docs" / "images" / "enforcement-hero.png"

# Brand palette (CLAUDE.md).
BG = "#F6F2E9"
INK = "#121820"
INK_SOFT = "#5A5046"
ORANGE = "#C04A1E"
SAGE = "#4C6B54"
NAVY = "#2C4A6E"

# Prefer a clean system sans; fall back to matplotlib default.
for cand in ("Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"):
    if any(f.name == cand for f in fm.fontManager.ttflist):
        plt.rcParams["font.family"] = cand
        break


def load():
    rows = list(csv.DictReader(METRICS.open()))
    years = [r["year"] for r in rows]
    dlp = [int(r["dlp_citations"]) for r in rows]
    cpc = [int(r["cost_per_citation"]) if r["cost_per_citation"] else None for r in rows]
    return years, dlp, cpc


def main() -> None:
    years, dlp, cpc = load()
    OUT.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(11, 8.5), dpi=140)
    fig.patch.set_facecolor(BG)

    # ---- title block ----
    fig.text(0.065, 0.945, "13 years of Seattle off-leash enforcement",
             fontsize=24, fontweight="bold", color=INK, ha="left")
    fig.text(0.065, 0.905, "Rising cost, falling output.",
             fontsize=19, fontstyle="italic", color=ORANGE, ha="left")

    # ---- main chart: citation bars + cost-per-citation line ----
    ax = fig.add_axes([0.075, 0.345, 0.85, 0.46])
    ax.set_facecolor(BG)
    x = range(len(years))
    bar_colors = [ORANGE if y != "2026" else "#E79B7C" for y in years]
    ax.bar(x, dlp, color=bar_colors, width=0.72, zorder=2)
    # peak + recovery annotations
    i2018 = years.index("2018")
    i2024 = years.index("2024")
    ax.annotate(f"{dlp[i2018]:,}", (i2018, dlp[i2018]), textcoords="offset points",
                xytext=(0, 6), ha="center", fontsize=11, fontweight="bold", color=INK)
    ax.annotate(f"{dlp[i2024]}", (i2024, dlp[i2024]), textcoords="offset points",
                xytext=(0, 6), ha="center", fontsize=11, fontweight="bold", color=INK)
    ax.set_ylabel("DLP citations / year", fontsize=11, color=INK_SOFT)
    ax.set_ylim(0, 1450)
    ax.set_xticks(list(x))
    ax.set_xticklabels(years, fontsize=10, color=INK_SOFT)
    ax.tick_params(axis="y", labelsize=10, colors=INK_SOFT)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#D8D0C0")

    # cost-per-citation line on twin axis (2016+, documented-cost era)
    ax2 = ax.twinx()
    xs = [i for i, c in enumerate(cpc) if c is not None]
    ys = [cpc[i] for i in xs]
    ax2.plot(xs, ys, color=NAVY, linewidth=2.6, marker="o", markersize=5, zorder=3)
    ax2.set_ylabel(r"\$ per citation", fontsize=11, color=NAVY)
    ax2.tick_params(axis="y", labelsize=10, colors=NAVY)
    ax2.set_ylim(0, 1900)
    for s in ("top",):
        ax2.spines[s].set_visible(False)
    ax2.spines["right"].set_color(NAVY)

    # legend
    ax.bar(0, 0, color=ORANGE, label="Citations issued (left)")
    ax.plot([], [], color=NAVY, linewidth=2.6, marker="o", label="Cost per citation, 2016+ (right)")
    ax.legend(loc="upper right", fontsize=10, frameon=False)

    # ---- three callout points ----
    cols = [
        (SAGE,   "FALLING OUTPUT",   "1,276 → 447",
         "Peak citations (2018) vs. the\nbest year since (2024) — about a third."),
        (ORANGE, "RISING COST",      r"\$229 → \$654",
         "Cost per citation, 2018 vs. 2024.\nFees cover ~11% of the \\$3.3M program."),
        (NAVY,   "NO DETERRENCE",    "84–96%",
         "First-time offenders, every year.\nThe offense mix never shifted."),
    ]
    xpos = [0.075, 0.395, 0.715]
    for (color, kicker, big, sub), xp in zip(cols, xpos):
        fig.text(xp, 0.215, kicker, fontsize=11, fontweight="bold", color=color,
                 ha="left", family="monospace")
        # DejaVu Sans for the big numbers: it has the → and \$ glyphs that
        # Helvetica Neue lacks, and stays consistent across all three.
        fig.text(xp, 0.150, big, fontsize=27, fontweight="bold", color=INK, ha="left",
                 family="DejaVu Sans")
        fig.text(xp, 0.095, sub, fontsize=10.5, color=INK_SOFT, ha="left", va="top")

    fig.text(0.075, 0.035,
             "Source: Seattle Animal Control PRRs C049204 + C263949 (2014–2026)  ·  "
             "seattledogparkdata.com/enforcement",
             fontsize=9, color=INK_SOFT, ha="left", family="monospace")

    fig.savefig(OUT, facecolor=BG, dpi=140)
    print(f"Wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
