---
name: scientific-plotting
description: Use when creating, revising, standardizing, or auditing scientific research plots from tabular or numerical data, including manuscript figures, supplementary figures, multi-panel plots, benchmark comparisons, and reproducible plotting scripts.
---

# Scientific Plotting

## Overview

把科研绘图任务做成可复现的“数据 + 脚本 + 图片 + 简短说明”闭环。默认使用 Python、matplotlib、numpy、pandas；已有项目若使用 R/ggplot2、plotly、seaborn 或专用绘图库，应优先沿用现有技术栈。

## 快速命令

用户可以直接用这些话触发本 skill：

- `根据 data.csv 画一张论文风格折线图，输出 png/pdf 和绘图脚本`
- `把这张图改成 Nature/ACS 风格，字体、线宽、图例统一`
- `做一个 2x2 多面板科研图，每个 panel 标 (a)-(d)`
- `检查这张图是否适合论文投稿，并修改脚本`
- `把多个 CSV 批量画成同一风格的图`
- `重画已有图片：保留科学含义，改善配色、标注和版式`
- `从 digitized CSV 和本研究数据画 benchmark 对比图`

## 工作流

1. 先确认数据含义：列名、单位、分组、误差、归一化方式、是否需要排序或过滤。
2. 选择图型：趋势用 line/scatter，分布用 histogram/violin/box，组成用 stacked/grouped bar，相关性用 scatter + fit，矩阵用 heatmap，多指标用多 panel 而不是硬塞双轴。
3. 写可复现脚本：输入路径、输出路径、样式参数集中放在文件顶部；脚本运行后自动创建输出目录。
4. 同时输出位图和矢量图：默认 `png` 用于预览，`pdf` 或 `svg` 用于论文排版。
5. 写一个短说明：说明数据来源、处理步骤、单位变换、归一化、误差条含义和输出文件。
6. 最后做图像检查：文件是否生成、分辨率是否足够、文字是否重叠、坐标单位是否完整、图例是否遮挡数据。

## Bundled Resources

- `scripts/plot_template.py`: copy or adapt this when starting a new matplotlib figure. It includes font fallback, journal-style axes, multi-format export, metadata sidecar output, and a built-in demo dataset.
- `scripts/audit_figure.py`: run this on generated `png/pdf/svg` files for quick checks on file existence, dimensions, extension, and likely raster resolution issues.
- `references/advanced-recipes.md`: load this when the task involves multi-panel figures, literature/digitized benchmark comparisons, transition matrices, stacked composition bars, or final-archive figure packages.

## 默认画图规范

优先使用白底、黑色坐标轴、浅灰网格和有限配色。不要使用彩虹色、3D 柱状图、过度阴影、无意义渐变背景。

推荐参数：

```python
plt.rcParams.update({
    "font.family": "Times New Roman",  # 不存在时回退到 DejaVu Serif 或 STIXGeneral
    "mathtext.fontset": "stix",
    "axes.linewidth": 1.0,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})
```

常用字号：

- 单栏图：`figsize=(3.4, 2.6)`，轴标题 9-10 pt，刻度 8-9 pt，图例 8-9 pt。
- 双栏图：`figsize=(7.0, 4.5)`，轴标题 10-12 pt，刻度 9-11 pt，图例 9-10 pt。
- 多面板图：panel 标签 11-13 pt，放在左上角，使用 `(a)`, `(b)`。

常用线条：

- 主曲线：`lw=2.0-2.3`，实线。
- 对照/文献曲线：`lw=1.6-2.0`，虚线。
- 散点：`s=20-40`，必要时加透明度 `alpha=0.6-0.8`。
- 网格：只开主轴浅灰网格，`linestyle="--"`, `alpha=0.25-0.4`。

推荐基础色：

```python
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
```

## 脚本模板

新建绘图脚本时优先复制 `scripts/plot_template.py`，再按任务删改。若只需要很小的一次性脚本，也可以采用下面的最小结构：

```python
#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "input.csv"
OUT_DIR = ROOT / "figures"


def setup_style() -> None:
    available = {f.name for f in font_manager.fontManager.ttflist}
    family = "Times New Roman" if "Times New Roman" in available else "DejaVu Serif"
    plt.rcParams.update({
        "font.family": family,
        "mathtext.fontset": "stix",
        "axes.linewidth": 1.0,
        "xtick.direction": "in",
        "ytick.direction": "in",
    })


def style_axes(ax) -> None:
    ax.grid(color="#D9D9D9", linestyle="--", alpha=0.35, linewidth=0.8)
    ax.tick_params(labelsize=10, width=1.0, length=4)
    for spine in ax.spines.values():
        spine.set_linewidth(1.0)


def main() -> None:
    setup_style()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)

    fig, ax = plt.subplots(figsize=(4.8, 3.4), dpi=300)
    ax.plot(df["x"], df["y"], color="#4E79A7", lw=2.1, label="Series 1")
    ax.set_xlabel("x label (unit)")
    ax.set_ylabel("y label (unit)")
    style_axes(ax)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()

    fig.savefig(OUT_DIR / "figure.png", dpi=300, bbox_inches="tight")
    fig.savefig(OUT_DIR / "figure.pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
```

## 图型选择规则

- `line plot`：连续变量趋势、时间序列、谱图、RDF/ADF/PMF 等曲线。
- `scatter plot`：相关性、模型预测 vs 实验、降维结果；样本多时用透明度或 hexbin。
- `bar plot`：离散类别均值或组成；必须显示误差条或样本数时，在图注/说明中写清楚。
- `stacked bar`：组成分数相加为 1 的情况；类别过多时改用 heatmap 或 small multiples。
- `box/violin`：样本分布；不要只画均值掩盖离散程度。
- `heatmap`：矩阵、转移概率、相关系数；色条必须有标签和单位。
- `multi-panel`：不同指标服务同一科学问题时使用；共享坐标能减少视觉负担。

复杂图型先查 `references/advanced-recipes.md`，尤其是：

- 多面板图：统一 panel 标签、共享轴、固定 `subplots_adjust`。
- 文献对比图：本研究数据和 digitized benchmark 分开读入，明确归一化和插值。
- 矩阵图：矩阵数值直接写在格子里，色条写单位。
- 组成图：分数和为 1 时优先 horizontal stacked bar，类别标签写在色块内。

避免：

- 除非有强理由，不使用双 y 轴；更推荐上下两个 panel。
- 不用截断 y 轴制造差异；若必须截断，明确画断轴符号并说明。
- 不把统计检验星号当作唯一信息；同时给出效应大小或置信区间。

## 数据与追溯

每张论文级图至少保留：

- 原始或中间数据：`data/`
- 绘图脚本：`scripts/` 或与图同目录的 `plot_*.py`
- 输出图片：`figures/`
- 简短说明：`README.md`、`figure_notes.md` 或自动生成的 summary

文献或手工数字化数据必须记录：

- DOI/URL 或来源文件
- figure/table 编号
- digitization 工具或方式
- 单位变换、插值、平滑、归一化方式
- 不确定性或读图误差风险

## 质量检查

交付前运行脚本，并用 `scripts/audit_figure.py` 做一次机械检查：

```bash
python scientific-plotting/scripts/audit_figure.py path/to/figure.png path/to/figure.pdf
```

然后人工检查：

- `png` 和 `pdf/svg` 均生成成功。
- 坐标轴有变量名和单位。
- 图例不遮挡关键数据。
- 字体在目标系统中可用；缺失时脚本有回退字体。
- panel 标签、注释、误差条、色条没有重叠。
- 输出图在 100% 和缩小到论文栏宽时仍可读。
- 数据处理步骤在脚本或说明中可追溯。

如果图用于投稿，优先保留矢量版本；若图中点数极多导致矢量文件过大，可以把高密度散点栅格化，但坐标轴和文字仍保留矢量。
