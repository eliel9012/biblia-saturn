#!/usr/bin/env python3
"""Generate a Jo Engine compatible 8x8 NBG2 font strip (8-bit paletted TGA).

This generates a vertical strip image:
- width: 8
- height: 8 * glyph_count

Important: Jo Engine expects each 8x8 glyph to be rotated 90 degrees clockwise
in the source image (see jo_vdp2_set_nbg2_8bits_font documentation).

Output files (defaults):
- saturn_app/cd/FONT.TGA
- saturn_app/font_mapping.h  (ASCII-only mapping string for C)
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ASCII_PRINTABLE = list(range(0x20, 0x7F))

# Non-ASCII bytes seen in acf_clean.json (ISO-8859-1 / Latin-1)
EXTRA_LATIN1 = [
    0xAB,  # <<
    0xB3,  # 3 (superscript)
    0xC0,  # A grave
    0xC1,  # A acute
    0xC3,  # A tilde
    0xC7,  # C cedilla
    0xC9,  # E acute
    0xCA,  # E circumflex
    0xD3,  # O acute
    0xD4,  # O circumflex
    0xDA,  # U acute
    0xE0,  # a grave
    0xE1,  # a acute
    0xE2,  # a circumflex
    0xE3,  # a tilde
    0xE7,  # c cedilla
    0xE9,  # e acute
    0xEA,  # e circumflex
    0xED,  # i acute
    0xF2,  # o grave
    0xF3,  # o acute
    0xF4,  # o circumflex
    0xF5,  # o tilde
    0xFA,  # u acute
    0xFC,  # u umlaut
]


def build_mapping_bytes() -> list[int]:
    mapping = list(ASCII_PRINTABLE)
    for b in EXTRA_LATIN1:
        if b not in mapping:
            mapping.append(b)
    return mapping


def mapping_bytes_to_c_string(mapping: list[int]) -> str:
    """Return an ASCII-only C string expression (concatenated literals)."""

    def esc_ascii(byte: int) -> str:
        ch = chr(byte)
        if ch == "\\":
            return "\\\\"
        if ch == '"':
            return "\\\""
        return ch

    # Emit as multiple literals to avoid "\\xNN" + hex-digit merge issues.
    parts: list[str] = []
    cur: list[str] = []

    def flush() -> None:
        nonlocal cur
        if cur:
            parts.append('"' + "".join(cur) + '"')
            cur = []

    for b in mapping:
        if 0x20 <= b <= 0x7E:
            cur.append(esc_ascii(b))
        else:
            flush()
            parts.append(f"\"\\x{b:02X}\"")
    flush()

    return " ".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--font",
        default="/usr/share/fonts/X11/misc/5x8-ISO8859-1.pcf.gz",
        help="Source bitmap font (PCF/TTF). Default: 5x8 ISO8859-1 PCF.",
    )
    ap.add_argument(
        "--out-tga",
        default="saturn_app/cd/FONT.TGA",
        help="Output Jo Engine font TGA.",
    )
    ap.add_argument(
        "--out-header",
        default="saturn_app/font_mapping.h",
        help="Output C header for the mapping string.",
    )
    ap.add_argument(
        "--preview-png",
        default="saturn_app/FONT_PREVIEW.png",
        help="Output preview PNG (rotated glyphs, same layout as TGA).",
    )
    ap.add_argument("--xoff", type=int, default=0, help="X offset inside the 8x8 cell.")
    ap.add_argument("--yoff", type=int, default=0, help="Y offset inside the 8x8 cell.")
    ap.add_argument(
        "--bold",
        type=int,
        default=1,
        help="Apply N rounds of dilation to thicken glyphs (0 disables).",
    )
    ap.add_argument(
        "--bold-mode",
        choices=("right", "4n"),
        default="right",
        help="Dilation mode. 'right' is a mild embolden. '4n' is heavier.",
    )
    ap.add_argument(
        "--shadow",
        choices=("none", "drop"),
        default="drop",
        help="Add a baked-in shadow using palette index 2. Default: drop.",
    )
    ap.add_argument(
        "--shadow-dx",
        type=int,
        default=1,
        help="Shadow X offset (pixels) for --shadow=drop.",
    )
    ap.add_argument(
        "--shadow-dy",
        type=int,
        default=0,
        help="Shadow Y offset (pixels) for --shadow=drop.",
    )
    args = ap.parse_args()

    mapping = build_mapping_bytes()
    if mapping[0] != 0x20:
        raise SystemExit("Mapping must start with space (0x20)")

    out_tga = Path(args.out_tga)
    out_header = Path(args.out_header)
    out_preview = Path(args.preview_png) if args.preview_png else None
    out_tga.parent.mkdir(parents=True, exist_ok=True)
    out_header.parent.mkdir(parents=True, exist_ok=True)
    if out_preview is not None:
        out_preview.parent.mkdir(parents=True, exist_ok=True)

    font = ImageFont.truetype(args.font, 8)

    # Paletted image:
    # - index 0 = glyph (white)
    # - index 1 = background (transparent on Saturn)
    # - index 2 = shadow (dark gray)
    palette = [255, 255, 255, 0, 0, 0, 64, 64, 64] + [0, 0, 0] * 253

    strip_h = 8 * len(mapping)
    strip = Image.new("P", (8, strip_h), color=1)
    strip.putpalette(palette)

    def dilate(cell_img: Image.Image) -> None:
        # In our palette: 0 = glyph pixel, 1 = background.
        pix = cell_img.load()
        w, h = cell_img.size
        orig = [[pix[x, y] for x in range(w)] for y in range(h)]
        out = [row[:] for row in orig]
        for y in range(h):
            for x in range(w):
                if orig[y][x] != 0:
                    continue
                if args.bold_mode == "right":
                    dirs = ((1, 0),)
                else:
                    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
                for dx, dy in dirs:
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        out[ny][nx] = 0
        for y in range(h):
            for x in range(w):
                pix[x, y] = out[y][x]

    def apply_drop_shadow(cell_img: Image.Image) -> None:
        if args.shadow == "none":
            return
        if args.shadow != "drop":
            raise SystemExit(f"Unsupported shadow mode: {args.shadow}")

        pix = cell_img.load()
        w, h = cell_img.size
        orig = [[pix[x, y] for x in range(w)] for y in range(h)]
        out = [row[:] for row in orig]

        dx = args.shadow_dx
        dy = args.shadow_dy

        for y in range(h):
            for x in range(w):
                if orig[y][x] != 0:
                    continue
                nx = x + dx
                ny = y + dy
                if not (0 <= nx < w and 0 <= ny < h):
                    continue
                if orig[ny][nx] == 0:
                    continue
                if out[ny][nx] == 1:
                    out[ny][nx] = 2

        for y in range(h):
            for x in range(w):
                pix[x, y] = out[y][x]

    for i, b in enumerate(mapping):
        ch = bytes([b]).decode("latin1")
        cell = Image.new("P", (8, 8), color=1)
        cell.putpalette(palette)
        d = ImageDraw.Draw(cell)
        d.text((args.xoff, args.yoff), ch, font=font, fill=0)
        for _ in range(max(0, args.bold)):
            dilate(cell)
        apply_drop_shadow(cell)
        # Rotate 90 degrees clockwise for Jo Engine.
        cell = cell.transpose(Image.Transpose.ROTATE_270)
        strip.paste(cell, (0, i * 8))

    if out_preview is not None:
        strip.save(out_preview, format="PNG")
    strip.save(out_tga, format="TGA")

    mapping_c = mapping_bytes_to_c_string(mapping)
    header = f"""// Auto-generated by tools/gen_font_tga_template.py
// Encoding: ISO-8859-1 (Latin-1) single-byte characters.
// IMPORTANT: The first character must be a space.

#pragma once

// Palette index 1 in the TGA file is used as the background and becomes transparent.
// Jo Engine adds +1 to palette indices, so pass 2 to jo_tga_8bits_loader().
#define SATURN_FONT_TGA_TRANSPARENT_COLOR_INDEX_IN_PALETTE 2

#define SATURN_FONT_MAPPING_STR {mapping_c}
"""
    out_header.write_text(header, encoding="ascii")

    print(f"Wrote: {out_tga} ({strip.size[0]}x{strip.size[1]})")
    if out_preview is not None:
        print(f"Wrote: {out_preview}")
    print(f"Wrote: {out_header}")
    print(f"Glyphs: {len(mapping)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
