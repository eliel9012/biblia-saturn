#!/usr/bin/env python3
"""
Generate Sega Saturn-friendly Bible assets from acf_clean.json.

Outputs (default):
  saturn_app/cd/BIBLE.BIN  - verse text blob (Latin-1), each verse NUL-terminated
  saturn_app/cd/BIBLE.IDX  - compact index for random access (little-endian)

Index format (little-endian):
  char[4]  magic = "BIB1"
  u16      version = 1
  u16      book_count
  u32      chapter_count_total
  u32      verse_count_total
  u32      text_size_bytes (size of BIBLE.BIN)

  book[book_count]:
    u32  first_chapter_index
    u16  chapter_count
    u16  reserved (0)

  chapter[chapter_count_total]:
    u32  first_verse_index
    u16  verse_count
    u16  reserved (0)

  verse_offsets[verse_count_total]:
    u32  text_offset_bytes
"""

from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path


MAGIC = b"BIB1"
VERSION = 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="acf_clean.json", help="Input JSON (clean UTF-8).")
    ap.add_argument("--out-dir", default="saturn_app/cd", help="Output directory (CD root).")
    ap.add_argument("--out-bin", default="BIBLE.BIN", help="Output text blob filename.")
    ap.add_argument("--out-idx", default="BIBLE.IDX", help="Output index filename.")
    args = ap.parse_args()

    in_json = Path(args.json)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_bin = out_dir / args.out_bin
    out_idx = out_dir / args.out_idx

    data = json.loads(in_json.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise SystemExit("Expected top-level JSON list of books")

    book_entries: list[tuple[int, int]] = []
    chapter_entries: list[tuple[int, int]] = []
    verse_offsets: list[int] = []

    max_verse_len = 0
    total_bytes = 0

    with out_bin.open("wb") as fbin:
        for b, book in enumerate(data):
            chapters = book.get("chapters")
            if not isinstance(chapters, list):
                raise SystemExit(f"Book #{b} has no 'chapters' list")

            first_chapter_index = len(chapter_entries)
            chapter_count = len(chapters)

            for c, chapter in enumerate(chapters):
                if not isinstance(chapter, list):
                    raise SystemExit(f"Book #{b} chapter #{c} is not a list")

                first_verse_index = len(verse_offsets)
                verse_count = len(chapter)

                for v, verse in enumerate(chapter):
                    if not isinstance(verse, str):
                        raise SystemExit(f"Book #{b} chapter #{c} verse #{v} is not a string")

                    # Normalize whitespace/newlines just in case.
                    verse = verse.replace("\r", " ").replace("\n", " ")
                    try:
                        raw = verse.encode("latin-1", errors="strict")
                    except UnicodeEncodeError as e:
                        raise SystemExit(
                            f"Non Latin-1 char in book #{b} chapter #{c} verse #{v}: {e}"
                        ) from e

                    verse_offsets.append(fbin.tell())
                    fbin.write(raw)
                    fbin.write(b"\0")

                    max_verse_len = max(max_verse_len, len(raw) + 1)

                chapter_entries.append((first_verse_index, verse_count))

            book_entries.append((first_chapter_index, chapter_count))

        total_bytes = fbin.tell()

    # Write index
    with out_idx.open("wb") as fidx:
        fidx.write(MAGIC)
        fidx.write(struct.pack("<H", VERSION))
        fidx.write(struct.pack("<H", len(book_entries)))
        fidx.write(struct.pack("<I", len(chapter_entries)))
        fidx.write(struct.pack("<I", len(verse_offsets)))
        fidx.write(struct.pack("<I", total_bytes))

        for first_chapter_index, chapter_count in book_entries:
            fidx.write(struct.pack("<IHH", first_chapter_index, chapter_count, 0))

        for first_verse_index, verse_count in chapter_entries:
            fidx.write(struct.pack("<IHH", first_verse_index, verse_count, 0))

        for off in verse_offsets:
            fidx.write(struct.pack("<I", off))

    idx_size = out_idx.stat().st_size
    bin_size = out_bin.stat().st_size

    # Basic sanity: last offset should be within file and offsets are increasing.
    if verse_offsets:
        assert 0 <= verse_offsets[0] < bin_size
        assert 0 <= verse_offsets[-1] < bin_size
        for i in range(1, len(verse_offsets)):
            if verse_offsets[i] < verse_offsets[i - 1]:
                raise SystemExit("Offsets not monotonically increasing (bug)")

    print(f"Wrote: {out_bin} ({bin_size} bytes)")
    print(f"Wrote: {out_idx} ({idx_size} bytes)")
    print(f"Books: {len(book_entries)}  Chapters: {len(chapter_entries)}  Verses: {len(verse_offsets)}")
    print(f"Max verse bytes (incl NUL): {max_verse_len}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

