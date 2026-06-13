#!/usr/bin/env python3
"""Generate a 320x240 Saturn-safe Bible reading bitmap preview.

The ROM renders verses at runtime, but this preview is useful for art direction:
dark matte text panel, safe margins, and low-noise sacred background detail.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W = 320
H = 240


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf",
    )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def quantize_saturn_safe(img: Image.Image) -> Image.Image:
    return img.convert("P", palette=Image.Palette.ADAPTIVE, colors=32).convert("RGB")


def draw_preview() -> Image.Image:
    img = Image.new("RGB", (W, H), (17, 15, 20))
    draw = ImageDraw.Draw(img)

    # Quiet parchment/gold edge detail outside the reading panel.
    for y in range(H):
        for x in range(W):
            edge = max(0, 38 - min(x, W - 1 - x, y, H - 1 - y))
            if edge:
                r = 18 + edge * 2
                g = 15 + edge
                b = 18
                img.putpixel((x, y), (min(r, 96), min(g, 70), b))

    for x in range(0, W, 16):
        draw.line((x, 10, x + 46, 62), fill=(92, 68, 30))
        draw.line((x, H - 20, x + 38, H - 70), fill=(78, 58, 28))
    for y in range(24, H, 32):
        draw.line((8, y, 70, y + 22), fill=(62, 47, 28))
        draw.line((W - 74, y + 22, W - 8, y), fill=(62, 47, 28))

    panel = (12, 14, 308, 204)
    hud = (12, 211, 308, 234)
    draw.rectangle(panel, fill=(18, 19, 25), outline=(178, 170, 142))
    draw.rectangle((panel[0] + 2, panel[1] + 2, panel[2] - 2, panel[3] - 2), outline=(50, 52, 62))
    draw.rectangle(hud, fill=(20, 21, 28), outline=(178, 170, 142))

    font = load_font(10)
    hud_font = load_font(9)
    text = [
        "1 No principio criou Deus o ceu e a",
        "  terra.",
        "2 E a terra era sem forma e vazia;",
        "  e havia trevas sobre a face do",
        "  abismo; e o Espirito de Deus se",
        "  movia sobre a face das aguas.",
        "3 E disse Deus: Haja luz; e houve",
        "  luz.",
        "4 E viu Deus que era boa a luz; e",
        "  fez Deus separacao entre a luz e",
        "  as trevas.",
    ]

    y = 23
    for line in text:
        draw.text((18, y + 1), line, font=font, fill=(0, 0, 0))
        draw.text((18, y), line, font=font, fill=(238, 236, 216))
        y += 15

    draw.rectangle((16, 208, 304, 210), fill=(96, 94, 108))
    draw.text((18, 214), "Genesis  Cap 1/50", font=hud_font, fill=(238, 236, 216))
    draw.text((18, 225), "B: caps   L/R: cap   X/Y: pagina", font=hud_font, fill=(238, 236, 216))

    return quantize_saturn_safe(img)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("outputs", nargs="+", help="PNG output path(s).")
    args = parser.parse_args()

    img = draw_preview()
    for output in args.outputs:
        out = Path(output)
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out)
        print(f"Wrote: {out} ({W}x{H})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
