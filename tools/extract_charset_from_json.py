#!/usr/bin/env python3
"""
Extrai o conjunto de caracteres usado no JSON da Biblia e imprime:
- lista de caracteres unicos
- lista de caracteres nao-ASCII (com codepoint e byte Latin-1 quando aplicavel)

Uso:
  python3 tools/extract_charset_from_json.py acf_clean.json
"""

from __future__ import annotations

import json
import sys
import unicodedata
from collections import Counter
from pathlib import Path


def _label(ch: str) -> str:
    if ch == " ":
        return "<space>"
    if ch == "\n":
        return "<nl>"
    if ch == "\t":
        return "<tab>"
    cp = ord(ch)
    if cp < 32 or (0x7F <= cp <= 0x9F):
        return f"<ctrl U+{cp:04X}>"
    return ch


def main() -> int:
    if len(sys.argv) < 2:
        print("Uso: extract_charset_from_json.py <arquivo.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8-sig"))

    chars = Counter()
    for book in data:
        chars.update(book.get("name", ""))
        for chap in book.get("chapters", []):
            for verse in chap:
                chars.update(verse)

    all_chars = sorted(chars.keys(), key=ord)
    nonascii = [c for c in all_chars if ord(c) > 127]
    ctrl = [c for c in all_chars if ord(c) < 32 or (0x7F <= ord(c) <= 0x9F)]

    print("unique_chars:", len(all_chars))
    if ctrl:
        print("WARNING: control chars ainda presentes:", len(ctrl))
        for c in ctrl:
            print(f"  U+{ord(c):04X}\t{_label(c)}\tcount={chars[c]}")
        print("")

    print("nonascii:", len(nonascii))
    for c in nonascii:
        cp = ord(c)
        name = unicodedata.name(c, "?")
        try:
            b = c.encode("latin-1")
            hx = f"0x{b[0]:02X}"
        except UnicodeEncodeError:
            hx = "n/a"
        print(f"  U+{cp:04X}\t{_label(c)}\t{name}\tlatin1={hx}\tcount={chars[c]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

