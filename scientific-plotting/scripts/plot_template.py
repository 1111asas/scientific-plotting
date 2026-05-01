#!/usr/bin/env python3
"""Reusable matplotlib template for publication-style scientific figures.

Use directly for a quick demo:
    python plot_template.py --demo --out-dir figures

Use with tabular data:
    python plot_template.py --input data.csv --x time_ps --y value --label "This study"
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager


COLORS = {
    "blue": "#4E79A7",
    "orange": "#F28E2B",
    "green": "#76C7A5",
    "red": "#D65F5F",
    "purple": "#8E63CE",
    "gray": "#666666",
    "grid": "#D9D9D9",
    "text": "#333333",
}


def setup_style() -> str:
    available = {f.name for f in font_manager.fontManager.ttflist}
    family = "Times New Roman" if "Times New Roman" in available else "DejaVu Serif"
    plt.rcParams.update({
        "font.family": family,
        "mathtext.fontset": "stix",
        "axes.linewidth": 1.0,
        "axes.edgecolor": "black",
        "axes.labelcolor": COLORS["text"],
        "xtick.direction": "in",
        "ytick.direction": "in",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
    })
    return family


def style_axes(ax, *, grid_axis: str = "both", ticksize: float = 9.5) -> None:
    ax.grid(axis=grid_axis, color=COLORS["grid"], linestyle="--", alpha=0.35, linewidth=0.8)
    ax.tick_params(labelsize=ticksize, width=1.0, length=4, top=False, right=False)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1.0)


def read_data(args: argparse.Namespace) -> dict[str, np.ndarray]:
    if args.demo:
        x = np.linspace(0.0, 10.0, 121)
        return {
            args.x: x,
            args.y: np.exp(-0.18 * x) * np.cos(1.4 * x),
            "benchmark": np.exp(-0.16 * x) * np.cos(1.4 * x + 0.18),
        }
    if args.input is None:
        raise SystemExit("Provide --input or use --demo.")
    rows = list(csv.DictReader(args.input.open(encoding="utf-8-sig")))
    if not rows:
        raise SystemExit(f"No rows found in {args.input}")
    data: dict[str, np.ndarray] = {}
    for key in rows[0]:
        try:
            data[key] = np.array([float(row[key]) for row in rows], dtype=float)
        except ValueError:
            continue
    return data


def export_figure(fig, out_dir: Path, stem: str, metadata: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / f"{stem}.png"
    pdf = out_dir / f"{stem}.pdf"
    fig.savefig(png, dpi=300, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    (out_dir / f"{stem}.metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, help="CSV file with plotting columns.")
    parser.add_argument("--x", default="x", help="Column for x values.")
    parser.add_argument("--y", default="y", help="Column for y values.")
    parser.add_argument("--benchmark-y", help="Optional benchmark/comparison y column.")
    parser.add_argument("--xlabel", default="x label (unit)")
    parser.add_argument("--ylabel", default="y label (unit)")
    parser.add_argument("--label", default="This study")
    parser.add_argument("--benchmark-label", default="Benchmark")
    parser.add_argument("--title", default="")
    parser.add_argument("--stem", default="scientific_figure")
    parser.add_argument("--out-dir", type=Path, default=Path("figures"))
    parser.add_argument("--demo", action="store_true", help="Generate a demo figure without input data.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    font_family = setup_style()
    df = read_data(args)
    if args.x not in df or args.y not in df:
        raise SystemExit(f"Required numeric columns not found: {args.x}, {args.y}")
    benchmark_col = args.benchmark_y or ("benchmark" if "benchmark" in df else None)

    fig, ax = plt.subplots(figsize=(4.8, 3.35), dpi=300)
    ax.plot(df[args.x], df[args.y], color=COLORS["blue"], lw=2.1, label=args.label)
    if benchmark_col:
        ax.plot(
            df[args.x],
            df[benchmark_col],
            color=COLORS["orange"],
            lw=1.8,
            ls="--",
            dash_capstyle="butt",
            label=args.benchmark_label,
        )

    ax.set_xlabel(args.xlabel, fontsize=10.5)
    ax.set_ylabel(args.ylabel, fontsize=10.5)
    if args.title:
        ax.set_title(args.title, fontsize=11.5, pad=8)
    style_axes(ax)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()

    export_figure(
        fig,
        args.out_dir,
        args.stem,
        {
            "input": str(args.input) if args.input else "demo",
            "x": args.x,
            "y": args.y,
            "benchmark_y": benchmark_col,
            "font_family": font_family,
            "outputs": [f"{args.stem}.png", f"{args.stem}.pdf"],
        },
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
