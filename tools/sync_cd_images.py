#!/usr/bin/env python3
"""
Sync UI + per-book background TGAs into saturn_app/cd with Saturn-friendly names.

Why:
- The original artwork files have long filenames and mixed case.
- Jo Engine + ISO9660 access is more reliable with short, uppercase 8.3 names.

Outputs:
- <out-dir>/UI/MAIN.TGA   (from ui_tela_inicial_320x240.tga)
- <out-dir>/UI/MENU.TGA   (from ui_menu_principal_320x240.tga)
- <out-dir>/BOOKS/B01A.TGA / B01B.TGA ... B66A/B66B.TGA

Note: Some books may be missing a variant (e.g. 66 has only A in the provided set).
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def _copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def _first(globbed: list[Path]) -> Path | None:
    return sorted(globbed)[0] if globbed else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--src-dir",
        default="Saturn_Biblia_Images/tga_format",
        help="Source directory containing the .tga files.",
    )
    ap.add_argument(
        "--out-dir",
        default="saturn_app/cd",
        help="Destination CD directory (the one packed into the ISO).",
    )
    args = ap.parse_args()

    src_dir = Path(args.src_dir)
    out_dir = Path(args.out_dir)

    if not src_dir.exists():
        raise SystemExit(f"Missing src dir: {src_dir}")

    # UI screens (optional, but handy if we use them later).
    ui_main = src_dir / "ui_tela_inicial_320x240.tga"
    ui_menu = src_dir / "ui_menu_principal_320x240.tga"
    if ui_main.exists():
        _copy(ui_main, out_dir / "UI" / "MAIN.TGA")
    if ui_menu.exists():
        _copy(ui_menu, out_dir / "UI" / "MENU.TGA")

    # Per-book artwork. We only rely on numbering (01..66).
    for book_num in range(1, 67):
        prefix = f"{book_num:02d}_"

        src_a = _first(list(src_dir.glob(f"{prefix}*_a_320x240.tga")))
        src_b = _first(list(src_dir.glob(f"{prefix}*_b_320x240.tga")))

        if src_a is not None:
            _copy(src_a, out_dir / "BOOKS" / f"B{book_num:02d}A.TGA")
        if src_b is not None:
            _copy(src_b, out_dir / "BOOKS" / f"B{book_num:02d}B.TGA")

        if src_a is None and src_b is None:
            print(f"WARNING: book {book_num:02d}: missing both A and B")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

