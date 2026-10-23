#!/usr/bin/env python3
"""Supplement Figure S1 for the JOI letter.

Draws the screening identity and the transmission-stack diagnostic from the
closed forms in manuscript/joi_letter_supplement.md. This script does not
refit seasonality or transmission, and it does not integrate the ODE.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "outputs" / "figures"
VECTOR_DIR = FIGURE_DIR / "vector"
STEM = "joi_supplement_schematic"

TEXT = "#1B1B1B"
MUTED = "#4B4D4F"
REFERENCE = "#747678"
LIGHT = "#DADCDD"
GRID = "#F7F8F8"
BLUE = "#2A6EBB"
TEAL = "#00B2A9"
ORANGE = "#E37222"
GOLD = "#F0AB00"

BLUE_FILL = "#E7F0F8"
TEAL_FILL = "#E5F6F5"
GOLD_FILL = "#FBF3DC"
WHITE = "#FFFFFF"


def reduction(c0: float, c1: float, ve: float) -> float:
    return 1.0 - (1.0 - c1 * ve) / (1.0 - c0 * ve)


def birth_exposure(uptake: float) -> float:
    return min(0.75, max(0.0, 0.02 + 0.55 * uptake))


def assert_closed_forms() -> dict[str, float]:
    """Stop if a displayed figure drifts from the supplement ledger."""
    phi = 180.0 / 271.25
    legacy_v = 1.0 - (1.0 - 0.75 * 0.55) * (1.0 - 0.75 * 0.92)
    primary = reduction(0.73, 0.90, 0.846)
    band_lo = reduction(0.73, 0.90, 0.769)
    band_hi = reduction(0.73, 0.90, 0.897)
    onset = reduction(0.73, 0.90, 0.862)

    def individual(v: float) -> float:
        return 1.0 - (1.0 - 0.57 * phi * v) / (1.0 - 0.02 * phi * v)

    e0 = birth_exposure(0.73)
    direct_90 = 1.0 - (
        (1.0 - birth_exposure(0.90) * phi * legacy_v) / (1.0 - e0 * phi * legacy_v)
    )
    checks = {
        "primary_90": primary,
        "band_lo": band_lo,
        "band_hi": band_hi,
        "onset_90": onset,
        "phi": phi,
        "legacy_v": legacy_v,
        "individual_legacy": individual(legacy_v),
        "individual_walker": individual(0.846),
        "direct_90": direct_90,
        "icb": reduction(0.544, 0.90, 0.846),
    }
    expected = {
        "primary_90": 0.37607866,
        "band_lo": 0.29804163,
        "band_hi": 0.44175671,
        "onset_90": 0.39526353,
        "phi": 0.66359447,
        "legacy_v": 0.817875,
        "individual_legacy": 0.301781289361592,
        "individual_walker": 0.3122767560860299,
        "direct_90": 0.06579818089527323,
        "icb": 0.5579647853924591,
    }
    for key, target in expected.items():
        if abs(checks[key] - target) > 1e-6:
            raise SystemExit(f"{key} drifted: {checks[key]} vs {target}")
    if abs(birth_exposure(0.73) - 0.4215) > 1e-12:
        raise SystemExit("birth exposure at 73% drifted")
    if abs(birth_exposure(1.0) - 0.57) > 1e-12:
        raise SystemExit("map endpoint at uptake 1 drifted")
    return checks


def add_box(ax, x, y, w, h, face, edge, radius=0.012, lw=0.9):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.003,rounding_size={radius}",
        facecolor=face,
        edgecolor=edge,
        linewidth=lw,
        mutation_aspect=0.6,
        transform=ax.transAxes,
        zorder=2,
    )
    ax.add_patch(patch)
    return patch


def add_text(ax, x, y, text, size=6.2, weight="regular", colour=TEXT, ha="center", va="center"):
    ax.text(
        x,
        y,
        text,
        ha=ha,
        va=va,
        fontsize=size,
        fontweight=weight,
        color=colour,
        transform=ax.transAxes,
        zorder=3,
        linespacing=1.25,
    )


def add_arrow(ax, start, end, colour=MUTED):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=7,
        linewidth=0.8,
        color=colour,
        transform=ax.transAxes,
        zorder=2,
        shrinkA=0,
        shrinkB=0,
        clip_on=False,
    )
    ax.add_patch(arrow)


def draw_screening(ax, values: dict[str, float]) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    add_text(ax, 0.015, 0.955, "A", size=9, weight="bold", ha="left", va="center")
    add_text(
        ax,
        0.055,
        0.955,
        "Screening identity  ·  reported contrast",
        size=8,
        weight="bold",
        ha="left",
        va="center",
    )

    add_box(ax, 0.04, 0.60, 0.40, 0.28, BLUE_FILL, BLUE)
    add_text(ax, 0.24, 0.815, "Vaccinated mothers", size=7.2, weight="bold", colour=BLUE)
    add_text(ax, 0.24, 0.745, "Fraction of infants   c", size=6.4)
    add_text(ax, 0.24, 0.675, r"Risk  $\propto\ 1 - \mathrm{VE}$", size=6.6)

    add_box(ax, 0.56, 0.60, 0.40, 0.28, GRID, MUTED)
    add_text(ax, 0.76, 0.815, "Unvaccinated mothers", size=7.2, weight="bold")
    add_text(ax, 0.76, 0.745, r"Fraction of infants   $1 - c$", size=6.4)
    add_text(ax, 0.76, 0.675, r"Risk  $\propto\ 1$", size=6.6)

    add_arrow(ax, (0.24, 0.60), (0.40, 0.50), BLUE)
    add_arrow(ax, (0.76, 0.60), (0.60, 0.50), MUTED)

    add_box(ax, 0.10, 0.335, 0.80, 0.155, WHITE, BLUE, lw=1.0)
    add_text(
        ax,
        0.50,
        0.435,
        r"Incidence  $\propto\ c(1-\mathrm{VE}) + (1-c)\ =\ 1 - c \cdot \mathrm{VE}$",
        size=7.0,
        weight="bold",
    )
    add_text(
        ax,
        0.50,
        0.368,
        r"Reduction from $c_0$ to $c_1$   $= \ 1 - (1 - c_1\mathrm{VE})\,/\,(1 - c_0\mathrm{VE})$",
        size=6.5,
    )

    add_arrow(ax, (0.50, 0.335), (0.50, 0.285), BLUE)

    primary = 100.0 * values["primary_90"]
    lo = 100.0 * values["band_lo"]
    hi = 100.0 * values["band_hi"]
    onset = 100.0 * values["onset_90"]
    add_box(ax, 0.10, 0.075, 0.80, 0.20, GOLD_FILL, ORANGE, lw=1.0)
    add_text(
        ax,
        0.50,
        0.215,
        f"73.0%  →  90%    at VE 84.6%    reduces incidence by  {primary:.2f}%",
        size=7.0,
        weight="bold",
    )
    add_text(
        ax,
        0.50,
        0.155,
        f"Published VE limits 76.9–89.7% through the same expression:  {lo:.2f}–{hi:.2f}%",
        size=6.2,
    )
    add_text(
        ax,
        0.50,
        0.105,
        f"Onset before 2 months, VE 86.2%, same target to 90%:  {onset:.2f}%",
        size=6.2,
    )

    add_text(
        ax,
        0.50,
        0.028,
        "The vaccination odds ratio equals the disease risk ratio when c is the exposure prevalence.  No slope, duration or transmission level enters.",
        size=5.5,
        colour=MUTED,
    )


def draw_stack(ax, values: dict[str, float]) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    add_text(ax, 0.015, 0.965, "B", size=9, weight="bold", ha="left", va="center")
    add_text(
        ax,
        0.055,
        0.965,
        "Transmission stack inside infant_0_2m  ·  diagnostic, not the reported impact",
        size=8,
        weight="bold",
        ha="left",
        va="center",
    )

    # Births sit over the two entry states. The gap between those states
    # is wide enough for the waning label.
    add_box(ax, 0.16, 0.80, 0.30, 0.11, WHITE, TEXT)
    add_text(ax, 0.31, 0.872, "Births into the bin", size=6.6, weight="bold")
    add_text(ax, 0.31, 0.828, r"Uptake $u$ mapped to entry $e$", size=5.6, colour=MUTED)

    add_box(ax, 0.015, 0.52, 0.25, 0.20, TEAL_FILL, TEAL)
    add_text(ax, 0.14, 0.672, "M protected", size=6.8, weight="bold", colour=TEAL)
    add_text(ax, 0.14, 0.622, r"Entry fraction  $e$", size=5.8)
    add_text(ax, 0.14, 0.578, "Susceptibility  0.5875", size=5.8)
    add_text(ax, 0.14, 0.542, r"Case rate  $\times\ (1-v)$", size=5.8)

    add_box(ax, 0.385, 0.52, 0.22, 0.20, GRID, MUTED)
    add_text(ax, 0.495, 0.655, "S", size=6.8, weight="bold")
    add_text(ax, 0.495, 0.605, r"Entry fraction  $1-e$", size=5.8)
    add_text(ax, 0.495, 0.562, "Susceptibility  1", size=5.8)

    add_arrow(ax, (0.24, 0.80), (0.14, 0.72), TEAL)
    add_arrow(ax, (0.40, 0.80), (0.495, 0.72), MUTED)
    add_text(ax, 0.145, 0.755, "e", size=5.6, colour=TEAL, ha="center")
    add_text(ax, 0.545, 0.755, r"$1-e$", size=5.6, colour=MUTED, ha="left")

    # Waning stays inside the bin: M to S.
    add_arrow(ax, (0.265, 0.60), (0.385, 0.60), ORANGE)
    add_text(ax, 0.325, 0.642, r"waning  $\lambda_w = 1/180$", size=5.2, colour=ORANGE)
    add_text(ax, 0.325, 0.568, "per day", size=5.0, colour=ORANGE)

    add_box(ax, 0.05, 0.30, 0.52, 0.12, WHITE, TEXT)
    add_text(ax, 0.31, 0.378, "Leave the 0–2-month bin", size=6.4, weight="bold")
    add_text(ax, 0.31, 0.332, r"Aging  $\lambda_a = 1/91.25$ per day   from both states", size=5.6)

    add_arrow(ax, (0.14, 0.52), (0.22, 0.42), MUTED)
    add_arrow(ax, (0.495, 0.52), (0.42, 0.42), MUTED)

    # Age strip. The first cell is the diagnostic endpoint.
    labels = ["0–2m", "3–11m", "1–4y", "5–9y", "10–17y", "18–39y", "40–64y", "65+"]
    strip_x, strip_w, strip_y, strip_h = 0.02, 0.57, 0.145, 0.075
    cell = strip_w / len(labels)
    for i, label in enumerate(labels):
        face = TEAL_FILL if i == 0 else WHITE
        edge = TEAL if i == 0 else LIGHT
        add_box(
            ax,
            strip_x + i * cell,
            strip_y,
            cell - 0.004,
            strip_h,
            face,
            edge,
            radius=0.006,
            lw=0.7,
        )
        add_text(
            ax,
            strip_x + i * cell + (cell - 0.004) / 2,
            strip_y + strip_h / 2,
            label,
            size=4.7,
            weight="bold" if i == 0 else "regular",
            colour=TEAL if i == 0 else MUTED,
        )

    add_text(
        ax,
        0.305,
        0.118,
        "Age bins.  The highlighted bin is named 0–2 months and is 0.25 years wide.",
        size=5.0,
        colour=REFERENCE,
    )
    add_text(
        ax,
        0.305,
        0.078,
        "0.57 and 0.02 are the line at uptake 1 and 0, not a measured conditional probability.",
        size=5.0,
        colour=REFERENCE,
    )
    add_text(
        ax,
        0.305,
        0.042,
        "Boundary clearance is off, so protection can age forward.  Within-bin equilibrium uses aging as the exit.",
        size=5.0,
        colour=REFERENCE,
    )

    # Equation card.
    add_box(ax, 0.64, 0.145, 0.34, 0.765, WHITE, BLUE, lw=1.0)
    add_text(ax, 0.81, 0.865, "Closed form", size=7.0, weight="bold", colour=BLUE)
    lines = [
        (0.825, r"$\varphi = 180/271.25 = 0.664$", "6.0", TEXT),
        (0.785, r"Protected person-time  $p = e\,\varphi$", "5.7", TEXT),
        (0.745, r"Cases  $\propto\ 1 - p\,v$", "5.7", TEXT),
        (0.700, "Legacy composite on that state", "5.5", MUTED),
        (0.665, r"$v = 0.818$", "6.0", TEXT),
        (0.620, "Map endpoints  0.57 vs 0.02", "5.5", MUTED),
        (0.580, "Individual effectiveness  30.2%", "6.2", TEXT),
        (0.545, "31.2% if the composite is 0.846", "5.5", MUTED),
        (0.490, "90% target, direct formula", "5.5", MUTED),
        (0.450, "6.58% of bin cases", "6.2", TEXT),
        (0.410, "Integrated reduction  5.92%", "6.0", TEXT),
        (0.365, "0.66 pp left unassigned", "5.6", ORANGE),
        (0.305, "Dose-1 share inside the bin is 0.", "5.3", MUTED),
        (0.260, "Screening contrast at the same", "5.3", MUTED),
        (0.225, "target remains 37.61%.", "5.5", BLUE),
    ]
    for y, text, size, colour in lines:
        weight = "bold" if colour in {TEXT, BLUE, ORANGE} and float(size) >= 6.0 else "regular"
        add_text(ax, 0.81, y, text, size=float(size), weight=weight, colour=colour)

    # Silence an unused-parameter lint if a future edit drops the dict.
    if values["phi"] <= 0:
        raise SystemExit("phi must be positive")


def main() -> None:
    values = assert_closed_forms()
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    width_in = 183 / 25.4
    height_in = 214 / 25.4
    fig, axes = plt.subplots(2, 1, figsize=(width_in, height_in))
    fig.subplots_adjust(left=0.015, right=0.985, top=0.985, bottom=0.012, hspace=0.08)
    draw_screening(axes[0], values)
    draw_stack(axes[1], values)

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    png = FIGURE_DIR / f"{STEM}.png"
    pdf = FIGURE_DIR / f"{STEM}.pdf"
    svg = VECTOR_DIR / f"{STEM}.svg"
    fig.savefig(png, dpi=600, facecolor="white")
    fig.savefig(pdf, facecolor="white")
    fig.savefig(svg, facecolor="white")
    plt.close(fig)
    for path in (png, pdf, svg):
        if not path.is_file() or path.stat().st_size < 1000:
            raise SystemExit(f"missing figure output: {path}")
    print(f"Wrote {png}")
    print(f"Wrote {pdf}")
    print(f"Wrote {svg}")


if __name__ == "__main__":
    main()
