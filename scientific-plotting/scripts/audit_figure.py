#!/usr/bin/env python3
"""Quick mechanical audit for generated scientific figure files."""

from __future__ import annotations

import argparse
from pathlib import Path


RASTER_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}
VECTOR_EXTS = {".pdf", ".svg", ".eps"}


def image_size(path: Path) -> tuple[int | None, int | None]:
    try:
        from PIL import Image
    except Exception:
        return None, None
    if path.suffix.lower() not in RASTER_EXTS:
        return None, None
    with Image.open(path) as img:
        return img.size


def audit(path: Path, *, min_width: int, min_height: int) -> list[str]:
    messages = []
    if not path.exists():
        return [f"FAIL missing: {path}"]
    if path.stat().st_size == 0:
        return [f"FAIL empty: {path}"]

    suffix = path.suffix.lower()
    if suffix not in RASTER_EXTS | VECTOR_EXTS:
        messages.append(f"WARN uncommon extension: {path}")

    width, height = image_size(path)
    if width is not None and height is not None:
        messages.append(f"OK raster size: {path} = {width}x{height}px")
        if width < min_width or height < min_height:
            messages.append(
                f"WARN small raster: {path} below {min_width}x{min_height}px; "
                "export a larger PNG or use PDF/SVG for publication."
            )
    elif suffix in VECTOR_EXTS:
        messages.append(f"OK vector candidate: {path}")
    else:
        messages.append(f"OK exists: {path}")

    return messages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("figures", nargs="+", type=Path)
    parser.add_argument("--min-width", type=int, default=1200)
    parser.add_argument("--min-height", type=int, default=900)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    any_fail = False
    for figure in args.figures:
        for message in audit(figure, min_width=args.min_width, min_height=args.min_height):
            print(message)
            any_fail = any_fail or message.startswith("FAIL")
    raise SystemExit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
