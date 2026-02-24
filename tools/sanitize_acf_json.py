#!/usr/bin/env python3
"""
Sanitiza o acf.json removendo caracteres "quebrados" (C1/control codes) detectados
no dump da Biblia ACF e gerando um novo arquivo `acf_clean.json`.

Motivacao:
- Alguns versiculos estao com bytes de controle (0x85/0x96/0x97/0x9E) inseridos
  no meio de palavras, provavelmente por conversao de encoding (Win-1252/Latin-1).
- Isso atrapalha renderizacao e vira "glifo inexistente" no Saturn.

Este script faz substituicoes pontuais (baseado nas ocorrencias reais encontradas)
e falha se restar qualquer caractere de controle no resultado.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


IN_PATH = Path("acf.json")
OUT_PATH = Path("acf_clean.json")


@dataclass
class FixStats:
    replaced_i_85: int = 0
    replaced_96: int = 0
    replaced_97: int = 0
    replaced_e_9e_upper: int = 0
    replaced_e_9e_lower: int = 0
    replaced_newline: int = 0
    strings_changed: int = 0


def _count_substring(s: str, sub: str) -> int:
    if not sub:
        return 0
    return s.count(sub)


def sanitize_text(s: str, stats: FixStats) -> str:
    original = s

    # Normaliza newline dentro de versiculo (so ocorre 1x no dump atual).
    n = _count_substring(s, "\n")
    if n:
        s = s.replace("\n", " ")
        stats.replaced_newline += n

    # 0x96: aparece em "ponham\x96se" -> "ponham-se".
    n = _count_substring(s, "\x96")
    if n:
        s = s.replace("\x96", "-")
        stats.replaced_96 += n

    # 0x97: usado como dash "isto\x97ele subiu\x97que" -> "isto - ele subiu - que".
    n = _count_substring(s, "\x97")
    if n:
        s = s.replace("\x97", " - ")
        stats.replaced_97 += n

    # 0x9E: aparece em nomes "E\x9Eutico" / "E\x9Eubulo" -> "Êutico" / "Êubulo".
    n = _count_substring(s, "E\x9E")
    if n:
        s = s.replace("E\x9E", "Ê")
        stats.replaced_e_9e_upper += n

    n = _count_substring(s, "e\x9E")
    if n:
        s = s.replace("e\x9E", "ê")
        stats.replaced_e_9e_lower += n

    # 0x85: ocorre 1x em "pri\x85ncipes" (na pratica vira "príncipes").
    # No dump atual, o byte aparece APOS o 'i', entao colapsamos "i\x85" -> "í".
    n = _count_substring(s, "i\x85")
    if n:
        s = s.replace("i\x85", "í")
        stats.replaced_i_85 += n

    if s != original:
        stats.strings_changed += 1
    return s


def sanitize_obj(obj: Any, stats: FixStats) -> Any:
    if isinstance(obj, str):
        return sanitize_text(obj, stats)
    if isinstance(obj, list):
        return [sanitize_obj(x, stats) for x in obj]
    if isinstance(obj, dict):
        return {k: sanitize_obj(v, stats) for k, v in obj.items()}
    return obj


def find_control_chars(obj: Any, path: str = "$") -> List[str]:
    problems: List[str] = []

    if isinstance(obj, str):
        for i, ch in enumerate(obj):
            cp = ord(ch)
            if cp < 0x20 or (0x7F <= cp <= 0x9F):
                problems.append(f"{path}[{i}]=U+{cp:04X}")
        return problems

    if isinstance(obj, list):
        for idx, item in enumerate(obj):
            problems.extend(find_control_chars(item, f"{path}[{idx}]"))
        return problems

    if isinstance(obj, dict):
        for k, v in obj.items():
            problems.extend(find_control_chars(v, f"{path}.{k}"))
        return problems

    return problems


def main() -> int:
    if not IN_PATH.exists():
        print(f"ERRO: arquivo nao encontrado: {IN_PATH}", file=sys.stderr)
        return 2

    # utf-8-sig remove BOM automaticamente se existir.
    with IN_PATH.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    stats = FixStats()
    cleaned = sanitize_obj(data, stats)

    problems = find_control_chars(cleaned)
    if problems:
        print("ERRO: ainda existem caracteres de controle no resultado:", file=sys.stderr)
        for p in problems[:50]:
            print(" ", p, file=sys.stderr)
        if len(problems) > 50:
            print(f"  ... (+{len(problems) - 50} problemas)", file=sys.stderr)
        return 3

    # Mantem minificado (parecido com o original), preservando acentos.
    OUT_PATH.write_text(
        json.dumps(cleaned, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    print("OK: gerado", OUT_PATH)
    print("Substituicoes:")
    print("  i\\x85  -> í  :", stats.replaced_i_85)
    print("  \\x96   -> -  :", stats.replaced_96)
    print("  \\x97   -> ' - ':", stats.replaced_97)
    print("  E\\x9E  -> Ê  :", stats.replaced_e_9e_upper)
    print("  e\\x9E  -> ê  :", stats.replaced_e_9e_lower)
    print("  \\n     -> ' ':", stats.replaced_newline)
    print("Strings alteradas:", stats.strings_changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

