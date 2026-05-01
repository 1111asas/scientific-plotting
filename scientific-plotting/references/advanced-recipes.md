# Advanced Scientific Plot Recipes

Load this reference only when a task needs figure patterns beyond a simple single-panel plot.

## Multi-Panel Manuscript Figures

Use multi-panel figures when each panel answers part of one scientific claim. Prefer shared axes when units match.

Patterns:

- Use `fig, axes = plt.subplots(..., dpi=300)` for regular grids.
- Use `GridSpec` only when panels have intentionally unequal sizes.
- Add panel labels with `ax.text(0.03, 0.94, "(a)", transform=ax.transAxes, ...)`.
- Use `fig.subplots_adjust(...)` for final figures when `tight_layout()` makes labels drift.
- Keep legends inside only when they do not hide data; otherwise use one figure-level legend.

## Benchmark And Digitized Literature Comparisons

Keep the visual comparison honest:

- Preserve raw digitized CSV files and never overwrite them with smoothed data.
- Make processed CSV files explicit: `*_normalized.csv`, `*_interpolated.csv`, `*_baseline_corrected.csv`.
- Record DOI/URL, original figure/table number, axis units, and digitization caveats.
- Use separate visual encodings: this-study solid line, literature dashed line or points.
- State whether curves are absolute, area-normalized, peak-normalized, or shape-normalized.

Useful transformations:

```python
def normalize_by_area(x, y):
    area = np.trapezoid(y, x)
    return y / area if area > 0 else y.copy()


def normalize_by_peak(y):
    ymax = float(np.max(y))
    return y / ymax if ymax > 0 else y.copy()
```

## Transition Matrices And Heatmaps

For state transitions, confusion matrices, correlation matrices, and contact maps:

- Keep row/column order explicit in code.
- Use a perceptually simple colormap; avoid rainbow.
- Write nonzero counts or values into cells.
- Add a colorbar with a label.
- If rows are normalized, label them as probability/fraction, not counts.

Core pattern:

```python
im = ax.imshow(matrix, cmap="PuOr", vmin=0)
ax.set_xticks(range(len(labels)), labels, rotation=35, ha="right")
ax.set_yticks(range(len(labels)), labels)
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if matrix[i, j] > 0:
            ax.text(j, i, f"{matrix[i, j]:.2g}", ha="center", va="center")
fig.colorbar(im, ax=ax, label="count")
```

## Composition And Fraction Figures

Use horizontal stacked bars when categories sum to one and labels are short.

Rules:

- Sort categories by scientific meaning, not by color.
- Show the exact fraction if the segment is large enough.
- Put long sample labels outside bars.
- Use `edgecolor="white"` and a small linewidth to separate adjacent segments.

## Annotated Mechanism Figures

Use annotations only for scientific landmarks: peaks, thresholds, region boundaries, transition states, or event windows.

Good annotations:

- `ax.axvline(...)` for thresholds.
- `ax.axvspan(...)` for physically meaningful regions.
- concise labels near the visual feature.

Avoid:

- Decorative labels with no scientific role.
- Arrows crossing dense data.
- More than three callouts per panel unless the figure is explicitly a schematic.

## Figure Archive Package

For final or manuscript-facing figures, keep one stable folder per figure package:

```text
figure_name/
├── data/
├── scripts/
├── figures/
└── figure_notes.md
```

The notes file should state:

- what each panel shows;
- exact input files;
- any smoothing, filtering, interpolation, normalization, or baseline correction;
- output filenames;
- known limitations.
