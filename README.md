# Scientific Plotting

`scientific-plotting` is a Codex skill and lightweight plotting toolkit for turning numerical research data into reproducible, manuscript-ready figures.

It is designed for workflows where the figure is not just a visual output, but a traceable scientific artifact: data provenance, plotting script, vector export, raster preview, and final quality checks should travel together.

## What This Repository Provides

- A reusable Codex skill for scientific plotting tasks.
- A publication-style matplotlib template with font fallback and multi-format export.
- A mechanical figure audit utility for generated PNG/PDF/SVG outputs.
- Advanced recipes for multi-panel figures, literature benchmark comparisons, digitized curves, heatmaps, transition matrices, and final figure archive packages.
- A compact project structure that can be copied into research repositories without bringing in a heavy framework.

## Repository Layout

```text
scientific-plotting/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── advanced-recipes.md
└── scripts/
    ├── audit_figure.py
    └── plot_template.py
```

## Core Design Principles

1. **Reproducibility first**

   A serious research figure should be regenerated from code. The expected package is:

   ```text
   data + script + figure + notes
   ```

2. **Publication defaults, not presentation defaults**

   The style is intentionally restrained: white background, black axes, readable serif/math fonts, limited color palette, vector export, and light grid lines only when they improve interpretation.

3. **Traceable benchmark comparisons**

   Literature or digitized data should never become anonymous curves. The workflow requires source notes, DOI/URL, figure/table number, units, digitization method, and any normalization or smoothing.

4. **Small tools over heavy frameworks**

   The included scripts are intentionally simple. They are meant to be adapted inside real research projects, not treated as a closed plotting package.

## Quick Start

Generate a demo publication-style figure:

```bash
python3 scientific-plotting/scripts/plot_template.py \
  --demo \
  --out-dir figures \
  --stem demo_figure
```

This writes:

```text
figures/demo_figure.png
figures/demo_figure.pdf
figures/demo_figure.metadata.json
```

Audit the generated outputs:

```bash
python3 scientific-plotting/scripts/audit_figure.py \
  figures/demo_figure.png \
  figures/demo_figure.pdf
```

Expected output is similar to:

```text
OK raster size: figures/demo_figure.png = 1410x975px
OK vector candidate: figures/demo_figure.pdf
```

## Plotting From CSV

For a CSV with numeric columns such as:

```csv
time_ps,value,benchmark
0.0,1.00,0.94
1.0,0.82,0.79
2.0,0.61,0.66
```

run:

```bash
python3 scientific-plotting/scripts/plot_template.py \
  --input data.csv \
  --x time_ps \
  --y value \
  --benchmark-y benchmark \
  --xlabel "Time (ps)" \
  --ylabel "Signal (a.u.)" \
  --label "This study" \
  --benchmark-label "Benchmark" \
  --out-dir figures \
  --stem signal_vs_time
```

The template writes both PNG and PDF, plus a JSON sidecar describing the input columns and selected font.

## Using The Codex Skill

The skill is defined in:

```text
scientific-plotting/SKILL.md
```

Example prompts:

- `Use $scientific-plotting to create a two-panel manuscript figure from these CSV files.`
- `Use $scientific-plotting to standardize this plot script for publication export.`
- `Use $scientific-plotting to audit whether this figure is ready for submission.`
- `Use $scientific-plotting to compare my curve against a digitized literature benchmark.`

The skill points Codex to the reusable scripts and advanced recipe reference only when needed, keeping normal tasks lightweight while still supporting more complex figure work.

## Advanced Recipes

The reference file:

```text
scientific-plotting/references/advanced-recipes.md
```

covers patterns for:

- multi-panel manuscript figures;
- benchmark and digitized literature comparisons;
- transition matrices and heatmaps;
- composition and fraction figures;
- annotated mechanism figures;
- final figure archive packages.

These are intentionally written as reusable figure-construction rules rather than project-specific instructions.

## Recommended Figure Package

For final manuscript figures, use a stable package layout:

```text
figure_name/
├── data/
├── scripts/
├── figures/
└── figure_notes.md
```

`figure_notes.md` should state:

- what each panel shows;
- exact input files;
- smoothing, filtering, interpolation, normalization, or baseline correction;
- output filenames;
- known limitations.

## Quality Checklist

Before treating a figure as publication-ready:

- Export both raster preview and vector output: `png` plus `pdf` or `svg`.
- Verify axis labels include variables and units.
- Confirm legends do not hide important data.
- Check that the selected font exists or has a fallback.
- Avoid rainbow colormaps and decorative effects that do not encode information.
- Record whether plotted curves are raw, area-normalized, peak-normalized, interpolated, smoothed, or baseline-corrected.
- Open the final figure at likely journal column width and verify that ticks, labels, and panel letters remain readable.

## Dependencies

The scripts are intentionally minimal:

- Python 3
- matplotlib
- numpy
- Pillow, optional, only for raster dimension checks in `audit_figure.py`

`plot_template.py` does not require pandas; it uses the Python standard `csv` module so it can run in lean environments.

## Status

This repository is meant to evolve as a practical research plotting skill. New recipes should be added when they capture reusable plotting judgment, not one-off project details.
