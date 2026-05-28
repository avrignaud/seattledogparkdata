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
OUT_HERO = ROOT / "docs" / "images" / "enforcement-hero.png"   # 4:3, email attachment
OUT_CARD = ROOT / "docs" / "images" / "enforcement-card.png"   # 1200x630, social card

# Brand palette (CLAUDE.md).
BG = "#F6F2E9"
INK = "#121820"
INK_SOFT = "#5A5046"
ORANGE = "#C04A1E"
SAGE = "#4C6B54"
NAVY = "#2C4A6E"
DANGER = "#8B2518"

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
    cost = [int(r["annual_cost"]) for r in rows]
    return years, dlp, cpc, cost


def avg_cost_per_citation(years, dlp, cost) -> int:
    """Aggregate average = total program cost / total citations over the
    displayed 2016–2025 window (excludes imputed pre-2016 cost and the partial
    2026 year, matching the cost-per-citation line on the chart)."""
    idx = [i for i, y in enumerate(years) if 2016 <= int(y) <= 2025]
    return round(sum(cost[i] for i in idx) / sum(dlp[i] for i in idx))


# The three headline points, shared by both layouts. The big numbers render in
# DejaVu Sans (it has the → and \$ glyphs Helvetica Neue lacks).
POINTS = [
    (SAGE,   "FALLING OUTPUT", "1,276 → 447",
     "Peak citations (2018) vs. the\nbest year since (2024) — about a third."),
    (ORANGE, "RISING COST",    r"\$229 → \$654",
     "Cost per citation, 2018 vs. 2024.\nFees cover ~11% of the \\$3.3M program."),
    (NAVY,   "NO DETERRENCE",  "84–96%",
     "First-time offenders, every year.\nThe offense mix never shifted."),
]

# COVID band: 2020–2021 (bar indices 6–7), matching the shading on the page.
COVID_SPAN = (5.5, 7.5)


def draw_chart(fig, rect, years, dlp, cpc, *, compact: bool, avg: int) -> None:
    """Citation bars + cost-per-citation line + COVID band + average line."""
    fs_tick = 7 if compact else 10
    fs_lbl = 8.5 if compact else 11
    fs_ann = 8 if compact else 11
    ax = fig.add_axes(rect)
    ax.set_facecolor(BG)
    x = list(range(len(years)))
    bar_colors = [ORANGE if y != "2026" else "#E79B7C" for y in years]
    ax.bar(x, dlp, color=bar_colors, width=0.72, zorder=2)
    ax.set_ylim(0, 1450)

    # COVID band behind the bars, with a label at the top.
    ax.axvspan(*COVID_SPAN, color=DANGER, alpha=0.11, zorder=0, lw=0)
    ax.text(sum(COVID_SPAN) / 2, 1450 * 0.96, "COVID", ha="center", va="top",
            color=DANGER, alpha=0.85, fontsize=fs_tick, fontweight="bold",
            family="monospace", zorder=4)

    i2018, i2024 = years.index("2018"), years.index("2024")
    ax.annotate(f"{dlp[i2018]:,}", (i2018, dlp[i2018]), textcoords="offset points",
                xytext=(0, 5), ha="center", fontsize=fs_ann, fontweight="bold", color=INK)
    ax.annotate(f"{dlp[i2024]}", (i2024, dlp[i2024]), textcoords="offset points",
                xytext=(0, 5), ha="center", fontsize=fs_ann, fontweight="bold", color=INK)

    if not compact:
        ax.set_ylabel("DLP citations / year", fontsize=fs_lbl, color=INK_SOFT)
    ax.set_xticks(x)
    labels = [("'" + y[2:]) if compact else y for y in years]
    ax.set_xticklabels(labels, fontsize=fs_tick, color=INK_SOFT)
    ax.tick_params(axis="y", labelsize=fs_tick, colors=INK_SOFT)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#D8D0C0")

    # cost-per-citation line on twin axis (2016+, documented-cost era)
    ax2 = ax.twinx()
    xs = [i for i, c in enumerate(cpc) if c is not None]
    ax2.plot(xs, [cpc[i] for i in xs], color=NAVY, linewidth=2.4,
             marker="o", markersize=4 if compact else 5, zorder=3)
    if not compact:
        ax2.set_ylabel(r"\$ per citation", fontsize=fs_lbl, color=NAVY)
    ax2.tick_params(axis="y", labelsize=fs_tick, colors=NAVY)
    ax2.set_ylim(0, 1900)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_color(NAVY)

    # average cost-per-citation reference line (2016–2025 aggregate)
    ax2.axhline(avg, color=NAVY, linestyle=(0, (5, 3)), linewidth=1.1, alpha=0.55, zorder=1)
    ax2.text(len(years) - 0.5, avg + 30, f"avg \\${avg}", ha="right", va="bottom",
             color=NAVY, fontsize=fs_tick, family="DejaVu Sans")

    ax.bar(0, 0, color=ORANGE, label="Citations issued" + ("" if compact else " (left)"))
    ax.plot([], [], color=NAVY, linewidth=2.4, marker="o",
            label="Cost / citation" + ("" if compact else ", 2016+ (right)"))
    ax.legend(loc="upper left" if compact else "upper right",
              fontsize=fs_tick, frameon=False)


SOURCE = ("Source: Seattle Animal Control PRRs C049204 + C263949 (2014–2026)  ·  "
          "seattledogparkdata.com/enforcement")


def build_hero(years, dlp, cpc, avg) -> None:
    """4:3 image for the email attachment: title, full chart, three callouts."""
    fig = plt.figure(figsize=(11, 8.5), dpi=140)
    fig.patch.set_facecolor(BG)
    fig.text(0.065, 0.945, "13 years of Seattle off-leash enforcement",
             fontsize=24, fontweight="bold", color=INK)
    fig.text(0.065, 0.905, "Rising cost, falling output.",
             fontsize=19, fontstyle="italic", color=ORANGE)
    draw_chart(fig, [0.075, 0.345, 0.85, 0.46], years, dlp, cpc, compact=False, avg=avg)
    for (color, kicker, big, sub), xp in zip(POINTS, (0.075, 0.395, 0.715)):
        fig.text(xp, 0.215, kicker, fontsize=11, fontweight="bold", color=color,
                 family="monospace")
        fig.text(xp, 0.150, big, fontsize=27, fontweight="bold", color=INK,
                 family="DejaVu Sans")
        fig.text(xp, 0.095, sub, fontsize=10.5, color=INK_SOFT, va="top")
    fig.text(0.075, 0.035, SOURCE, fontsize=9, color=INK_SOFT, family="monospace")
    fig.savefig(OUT_HERO, facecolor=BG, dpi=140)
    print(f"Wrote {OUT_HERO.relative_to(ROOT)} ({OUT_HERO.stat().st_size:,} bytes)")


# One-line glosses for the social card (the hero uses the 2-line versions).
CARD_SUBS = [
    "Peak (2018) vs. best year since (2024).",
    "Cost per citation, 2018 vs. 2024.",
    "First-time offenders, every year.",
]


def build_card(years, dlp, cpc, avg) -> None:
    """1200x630 social card: title + three stacked callouts (left), chart (right)."""
    fig = plt.figure(figsize=(12, 6.3), dpi=100)
    fig.patch.set_facecolor(BG)
    fig.text(0.045, 0.90, "13 years of Seattle off-leash enforcement",
             fontsize=20, fontweight="bold", color=INK)
    fig.text(0.045, 0.81, "Rising cost, falling output.",
             fontsize=16, fontstyle="italic", color=ORANGE)
    for (color, kicker, big, _), sub, yc in zip(POINTS, CARD_SUBS, (0.60, 0.40, 0.20)):
        fig.text(0.045, yc + 0.085, kicker, fontsize=9.5, fontweight="bold",
                 color=color, family="monospace")
        fig.text(0.045, yc, big, fontsize=22, fontweight="bold", color=INK,
                 family="DejaVu Sans", va="center")
        fig.text(0.045, yc - 0.075, sub, fontsize=9, color=INK_SOFT, va="top")
    draw_chart(fig, [0.55, 0.20, 0.42, 0.58], years, dlp, cpc, compact=True, avg=avg)
    fig.text(0.045, 0.045, SOURCE, fontsize=7.5, color=INK_SOFT, family="monospace")
    fig.savefig(OUT_CARD, facecolor=BG, dpi=100)
    print(f"Wrote {OUT_CARD.relative_to(ROOT)} ({OUT_CARD.stat().st_size:,} bytes)")


def main() -> None:
    OUT_HERO.parent.mkdir(parents=True, exist_ok=True)
    years, dlp, cpc, cost = load()
    avg = avg_cost_per_citation(years, dlp, cost)
    print(f"Average cost per citation (2016–2025): ${avg}")
    build_hero(years, dlp, cpc, avg)
    build_card(years, dlp, cpc, avg)


if __name__ == "__main__":
    main()
