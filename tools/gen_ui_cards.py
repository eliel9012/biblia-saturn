#!/usr/bin/env python3
"""Generate simple UI card textures (TGA) for VDP1 sprites.

We keep these textures tiny and rely on VDP1 scaling/distortion at runtime.
Files generated (by default):
- saturn_app/cd/UI/CARD.TGA      (normal card)
- saturn_app/cd/UI/CARDSEL.TGA   (selected card)
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def lerp(a: int, b: int, t: float) -> int:
    return int(round(a + (b - a) * t))


def lerp_rgb(c0: tuple[int, int, int], c1: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return (lerp(c0[0], c1[0], t), lerp(c0[1], c1[1], t), lerp(c0[2], c1[2], t))


def make_card(
    w: int,
    h: int,
    top: tuple[int, int, int],
    bot: tuple[int, int, int],
    border_light: tuple[int, int, int],
    border_dark: tuple[int, int, int],
    inner_highlight: tuple[int, int, int] | None = None,
) -> Image.Image:
    img = Image.new("RGB", (w, h), bot)
    px = img.load()

    # Vertical gradient fill.
    for y in range(h):
        t = 0.0 if h <= 1 else y / (h - 1)
        c = lerp_rgb(top, bot, t)
        for x in range(w):
            px[x, y] = c

    d = ImageDraw.Draw(img)

    # Beveled border (1px).
    d.line([(0, 0), (w - 1, 0)], fill=border_light)
    d.line([(0, 0), (0, h - 1)], fill=border_light)
    d.line([(0, h - 1), (w - 1, h - 1)], fill=border_dark)
    d.line([(w - 1, 0), (w - 1, h - 1)], fill=border_dark)

    # Thin inner highlight line (top) to give a "card" feel when scaled down.
    if inner_highlight is not None and h >= 4:
        d.line([(1, 2), (w - 2, 2)], fill=inner_highlight)

    return img


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="saturn_app/cd/UI", help="Output directory inside the CD tree.")
    ap.add_argument("--w", type=int, default=64, help="Base card width (pixels).")
    ap.add_argument("--h", type=int, default=16, help="Base card height (pixels).")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Normal card: dark, neutral.
    card = make_card(
        args.w,
        args.h,
        top=(44, 44, 52),
        bot=(18, 18, 22),
        border_light=(160, 160, 175),
        border_dark=(6, 6, 8),
        inner_highlight=(96, 96, 112),
    )

    # Selected card: warmer/brighter.
    card_sel = make_card(
        args.w,
        args.h,
        top=(110, 86, 36),
        bot=(62, 44, 18),
        border_light=(240, 220, 150),
        border_dark=(18, 12, 6),
        inner_highlight=(190, 160, 90),
    )

    out_card = out_dir / "CARD.TGA"
    out_card_sel = out_dir / "CARDSEL.TGA"
    card.save(out_card, format="TGA")
    card_sel.save(out_card_sel, format="TGA")

    print(f"Wrote: {out_card}")
    print(f"Wrote: {out_card_sel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

