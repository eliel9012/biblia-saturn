#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Leitor "estilo DOS" (tela cheia, TUI) para a Biblia ACF em JSON.

Formato esperado (acf_clean.json / acf.json neste repo):
[
  {"abbrev":"gn","name":"Gênesis","chapters":[ ["v1","v2",...], ["v1",...], ... ]},
  ...
]

Uso:
  python3 dos_biblia_acf.py
  python3 dos_biblia_acf.py --json acf_clean.json
  python3 dos_biblia_acf.py --selftest
"""

from __future__ import annotations

import argparse
import curses
import json
import os
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional, Tuple


@dataclass(frozen=True)
class Book:
    name: str
    abbrev: str
    chapters: List[List[str]]  # chapters[chap_idx][verse_idx] -> verse text


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def load_bible(path: Path) -> List[Book]:
    data = _load_json(path)
    if not isinstance(data, list):
        raise ValueError("JSON invalido: esperado uma lista de livros.")

    books: List[Book] = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Livro #{i}: esperado objeto.")
        name = str(item.get("name", "")).strip()
        abbrev = str(item.get("abbrev", "")).strip()
        chapters = item.get("chapters")
        if not name or not abbrev:
            raise ValueError(f"Livro #{i}: faltando 'name'/'abbrev'.")
        if not isinstance(chapters, list):
            raise ValueError(f"Livro '{name}': 'chapters' invalido.")
        # Normaliza: garante lista de lista de strings.
        norm_chapters: List[List[str]] = []
        for c, chap in enumerate(chapters):
            if not isinstance(chap, list):
                raise ValueError(f"Livro '{name}' capitulo {c+1}: esperado lista de versos.")
            norm_chapters.append([str(v) for v in chap])
        books.append(Book(name=name, abbrev=abbrev, chapters=norm_chapters))

    return books


def discover_default_json() -> Optional[Path]:
    here = Path(__file__).resolve().parent
    candidates = [
        here / "acf_clean.json",
        here / "acf.json",
        Path.cwd() / "acf_clean.json",
        Path.cwd() / "acf.json",
        Path("/home/pi/acf_clean.json"),
        Path("/home/pi/acf.json"),
    ]
    for p in candidates:
        if p.exists() and p.is_file():
            return p
    return None


def casefold(s: str) -> str:
    # casefold() ja lida melhor com acentos do que lower().
    return s.casefold()


def _clamp(v: int, lo: int, hi: int) -> int:
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v


def _safe_addstr(win: "curses._CursesWindow", y: int, x: int, s: str, attr: int = 0) -> None:
    try:
        win.addstr(y, x, s, attr)
    except curses.error:
        # Terminal pequeno ou escrita fora do viewport.
        pass


def _truncate(s: str, width: int) -> str:
    if width <= 0:
        return ""
    if len(s) <= width:
        return s
    if width == 1:
        return s[:1]
    return s[: width - 1] + ">"


def _draw_bar(stdscr: "curses._CursesWindow", y: int, text: str, attr: int) -> None:
    h, w = stdscr.getmaxyx()
    if y < 0 or y >= h:
        return
    s = _truncate(text.ljust(w), w)
    _safe_addstr(stdscr, y, 0, s, attr)


def _prompt_line(stdscr: "curses._CursesWindow", prompt: str) -> Optional[str]:
    # Prompt simples no rodape. Retorna None se cancelar (ESC).
    try:
        curses.curs_set(1)
    except curses.error:
        pass
    stdscr.nodelay(False)
    h, w = stdscr.getmaxyx()
    y = h - 1
    buf: List[str] = []
    pos = 0
    while True:
        stdscr.move(y, 0)
        stdscr.clrtoeol()
        line = prompt + "".join(buf)
        _safe_addstr(stdscr, y, 0, _truncate(line, w - 1))
        stdscr.move(y, min(len(prompt) + pos, max(0, w - 1)))
        stdscr.refresh()

        ch = stdscr.getch()
        if ch in (27,):  # ESC
            try:
                curses.curs_set(0)
            except curses.error:
                pass
            return None
        if ch in (10, 13, curses.KEY_ENTER):
            try:
                curses.curs_set(0)
            except curses.error:
                pass
            return "".join(buf).strip()
        if ch in (curses.KEY_BACKSPACE, 127, 8):
            if pos > 0:
                del buf[pos - 1]
                pos -= 1
            continue
        if ch == curses.KEY_LEFT:
            pos = max(0, pos - 1)
            continue
        if ch == curses.KEY_RIGHT:
            pos = min(len(buf), pos + 1)
            continue
        if ch == curses.KEY_HOME:
            pos = 0
            continue
        if ch == curses.KEY_END:
            pos = len(buf)
            continue
        if 32 <= ch <= 126 or ch >= 160:
            # Aceita ASCII imprimivel e Latin-1 estendido; terminal UTF-8 deve renderizar.
            buf.insert(pos, chr(ch))
            pos += 1


def _wrap_verse(verse_num: int, text: str, width: int) -> List[str]:
    # Prefixo fixo com numero do verso.
    prefix = f"{verse_num:>3} "
    avail = max(1, width - len(prefix))

    wrapped = textwrap.wrap(
        text,
        width=avail,
        break_long_words=False,
        drop_whitespace=True,
        replace_whitespace=False,
    )
    if not wrapped:
        wrapped = [""]
    lines = [prefix + wrapped[0]]
    indent = " " * len(prefix)
    for part in wrapped[1:]:
        lines.append(indent + part)
    return lines


def build_chapter_lines(book: Book, chap_idx: int, width: int) -> Tuple[List[str], List[int]]:
    # Retorna (linhas, verse_to_line_idx).
    chapter = book.chapters[chap_idx]
    lines: List[str] = []
    verse_to_line: List[int] = [0] * len(chapter)
    for i, verse_text in enumerate(chapter):
        verse_to_line[i] = len(lines)
        lines.extend(_wrap_verse(i + 1, verse_text, width))
    return lines, verse_to_line


def _format_ref(books: List[Book], b: int, c: int, v: Optional[int] = None) -> str:
    book = books[b]
    if v is None:
        return f"{book.name} {c+1}"
    return f"{book.name} {c+1}:{v+1}"


def _draw_help(stdscr: "curses._CursesWindow", attr_title: int, attr_body: int) -> None:
    stdscr.erase()
    h, w = stdscr.getmaxyx()
    title = "Biblia ACF (DOS-like) - Ajuda"
    _safe_addstr(stdscr, 0, 0, _truncate(title.ljust(w), w), attr_title)

    body = [
        "",
        "Navegacao geral:",
        "  Setas / PgUp / PgDn : mover / rolar",
        "  Enter              : selecionar",
        "  b                  : voltar",
        "  q                  : sair",
        "",
        "Leitura:",
        "  Left/Right         : capitulo anterior/proximo",
        "  g                  : ir para verso (numero)",
        "  /                  : buscar (global)",
        "",
        "Busca:",
        "  Enter              : abrir resultado",
        "  ESC/b              : fechar resultados",
        "",
        "Pressione qualquer tecla para voltar.",
    ]

    y = 2
    for line in body:
        if y >= h - 1:
            break
        _safe_addstr(stdscr, y, 2, _truncate(line, max(0, w - 4)), attr_body)
        y += 1
    stdscr.refresh()
    stdscr.getch()


@dataclass
class SearchHit:
    book_i: int
    chap_i: int
    verse_i: int


def _search_all(books: List[Book], query: str) -> List[SearchHit]:
    q = casefold(query)
    hits: List[SearchHit] = []
    for bi, book in enumerate(books):
        for ci, chap in enumerate(book.chapters):
            for vi, verse in enumerate(chap):
                if q in casefold(verse):
                    hits.append(SearchHit(book_i=bi, chap_i=ci, verse_i=vi))
    return hits


def run_tui(stdscr: "curses._CursesWindow", books: List[Book], json_path: Path) -> int:
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    stdscr.keypad(True)
    stdscr.nodelay(False)

    # Cores "DOS": amarelo no azul + selecao ciano.
    has_color = curses.has_colors()
    if has_color:
        curses.start_color()
        try:
            curses.use_default_colors()
        except curses.error:
            pass
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)  # normal
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)   # highlight
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)   # title/body
        attr_norm = curses.color_pair(1)
        attr_hi = curses.color_pair(2)
        attr_title = curses.color_pair(3) | curses.A_BOLD
        attr_body = curses.color_pair(3)
        stdscr.bkgd(" ", attr_norm)
    else:
        attr_norm = curses.A_NORMAL
        attr_hi = curses.A_REVERSE
        attr_title = curses.A_BOLD
        attr_body = curses.A_NORMAL

    state = "books"  # books | chapters | reader | search
    book_sel = 0
    book_top = 0
    chap_sel = 0
    chap_top = 0

    cur_book = 0
    cur_chap = 0
    scroll_line = 0
    chapter_lines: List[str] = []
    verse_to_line: List[int] = []

    search_hits: List[SearchHit] = []
    search_sel = 0
    search_top = 0
    last_query: Optional[str] = None

    def rebuild_reader() -> None:
        nonlocal chapter_lines, verse_to_line, scroll_line
        h, w = stdscr.getmaxyx()
        content_w = max(10, w - 2)
        chapter_lines, verse_to_line = build_chapter_lines(books[cur_book], cur_chap, content_w)
        max_scroll = max(0, len(chapter_lines) - max(1, (h - 3)))
        scroll_line = _clamp(scroll_line, 0, max_scroll)

    rebuild_reader()

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        title = f"Biblia ACF (DOS-like)  |  {json_path.name}  |  F1 Ajuda"
        _draw_bar(stdscr, 0, title, attr_title)

        footer = "q sair | Enter selecionar | b voltar | / buscar | setas navegar"
        _draw_bar(stdscr, h - 1, footer, attr_title)

        if state == "books":
            items = [f"{i+1:>2} {b.name}" for i, b in enumerate(books)]
            content_h = max(1, h - 2)
            book_top = _clamp(book_top, 0, max(0, len(items) - content_h))
            book_sel = _clamp(book_sel, 0, max(0, len(items) - 1))
            if book_sel < book_top:
                book_top = book_sel
            if book_sel >= book_top + content_h:
                book_top = book_sel - content_h + 1

            _safe_addstr(stdscr, 1, 0, _truncate("Selecione o livro:", w), attr_body)
            for row in range(content_h - 1):
                idx = book_top + row
                if idx >= len(items):
                    break
                y = 2 + row
                s = _truncate(items[idx].ljust(w), w)
                attr = attr_hi if idx == book_sel else attr_norm
                _safe_addstr(stdscr, y, 0, s, attr)

        elif state == "chapters":
            book = books[cur_book]
            items = [f"Capitulo {i+1}" for i in range(len(book.chapters))]
            content_h = max(1, h - 2)
            chap_top = _clamp(chap_top, 0, max(0, len(items) - content_h))
            chap_sel = _clamp(chap_sel, 0, max(0, len(items) - 1))
            if chap_sel < chap_top:
                chap_top = chap_sel
            if chap_sel >= chap_top + content_h:
                chap_top = chap_sel - content_h + 1

            _safe_addstr(
                stdscr,
                1,
                0,
                _truncate(f"{book.name}  |  Selecione o capitulo:", w),
                attr_body,
            )
            for row in range(content_h - 1):
                idx = chap_top + row
                if idx >= len(items):
                    break
                y = 2 + row
                s = _truncate(items[idx].ljust(w), w)
                attr = attr_hi if idx == chap_sel else attr_norm
                _safe_addstr(stdscr, y, 0, s, attr)

        elif state == "reader":
            book = books[cur_book]
            chap = cur_chap
            header = f"{book.name}  Capitulo {chap+1}/{len(book.chapters)}"
            _safe_addstr(stdscr, 1, 0, _truncate(header.ljust(w), w), attr_body)

            view_y0 = 2
            view_h = max(1, h - 3)
            max_scroll = max(0, len(chapter_lines) - view_h)
            scroll_line = _clamp(scroll_line, 0, max_scroll)
            for i in range(view_h):
                idx = scroll_line + i
                if idx >= len(chapter_lines):
                    break
                s = _truncate(chapter_lines[idx].ljust(w), w)
                _safe_addstr(stdscr, view_y0 + i, 0, s, attr_norm)

            # Barra de status curta com referencia aproximada (verso no topo).
            top_verse = 0
            if verse_to_line:
                # encontra o maior verso cujo inicio <= scroll_line
                lo, hi = 0, len(verse_to_line) - 1
                while lo <= hi:
                    mid = (lo + hi) // 2
                    if verse_to_line[mid] <= scroll_line:
                        top_verse = mid
                        lo = mid + 1
                    else:
                        hi = mid - 1
            status = f"{_format_ref(books, cur_book, cur_chap, top_verse)}  |  linha {scroll_line+1}/{max(1, len(chapter_lines))}"
            _draw_bar(stdscr, h - 1, status.ljust(w), attr_title)

        elif state == "search":
            query_show = last_query or ""
            _safe_addstr(
                stdscr,
                1,
                0,
                _truncate(f"Resultados da busca: '{query_show}'  (Enter abre, ESC/b volta)", w),
                attr_body,
            )
            content_h = max(1, h - 3)
            search_top = _clamp(search_top, 0, max(0, len(search_hits) - content_h))
            search_sel = _clamp(search_sel, 0, max(0, len(search_hits) - 1))
            if search_sel < search_top:
                search_top = search_sel
            if search_sel >= search_top + content_h:
                search_top = search_sel - content_h + 1

            for row in range(content_h):
                idx = search_top + row
                if idx >= len(search_hits):
                    break
                hit = search_hits[idx]
                verse_text = books[hit.book_i].chapters[hit.chap_i][hit.verse_i]
                line = f"{books[hit.book_i].name} {hit.chap_i+1}:{hit.verse_i+1}  {verse_text}"
                s = _truncate(line.ljust(w), w)
                attr = attr_hi if idx == search_sel else attr_norm
                _safe_addstr(stdscr, 2 + row, 0, s, attr)

            _draw_bar(stdscr, h - 1, f"{len(search_hits)} resultado(s)".ljust(w), attr_title)

        stdscr.refresh()

        ch = stdscr.getch()
        if ch in (ord("q"), ord("Q")):
            return 0
        if ch == curses.KEY_F1:
            _draw_help(stdscr, attr_title, attr_body)
            rebuild_reader()
            continue

        if state == "books":
            if ch in (curses.KEY_UP,):
                book_sel = max(0, book_sel - 1)
            elif ch in (curses.KEY_DOWN,):
                book_sel = min(len(books) - 1, book_sel + 1)
            elif ch in (curses.KEY_PPAGE,):
                book_sel = max(0, book_sel - max(1, h - 3))
            elif ch in (curses.KEY_NPAGE,):
                book_sel = min(len(books) - 1, book_sel + max(1, h - 3))
            elif ch in (10, 13, curses.KEY_ENTER):
                cur_book = book_sel
                chap_sel = 0
                chap_top = 0
                state = "chapters"
            elif ch in (ord("/"),):
                q = _prompt_line(stdscr, "Buscar (global): ")
                if q:
                    last_query = q
                    search_hits = _search_all(books, q)
                    search_sel = 0
                    search_top = 0
                    state = "search"

        elif state == "chapters":
            book = books[cur_book]
            if ch in (curses.KEY_UP,):
                chap_sel = max(0, chap_sel - 1)
            elif ch in (curses.KEY_DOWN,):
                chap_sel = min(len(book.chapters) - 1, chap_sel + 1)
            elif ch in (curses.KEY_PPAGE,):
                chap_sel = max(0, chap_sel - max(1, h - 3))
            elif ch in (curses.KEY_NPAGE,):
                chap_sel = min(len(book.chapters) - 1, chap_sel + max(1, h - 3))
            elif ch in (ord("b"), ord("B"), 27):
                state = "books"
            elif ch in (10, 13, curses.KEY_ENTER):
                cur_chap = chap_sel
                scroll_line = 0
                rebuild_reader()
                state = "reader"
            elif ch in (ord("/"),):
                q = _prompt_line(stdscr, "Buscar (global): ")
                if q:
                    last_query = q
                    search_hits = _search_all(books, q)
                    search_sel = 0
                    search_top = 0
                    state = "search"

        elif state == "reader":
            view_h = max(1, h - 3)
            if ch in (curses.KEY_UP,):
                scroll_line = max(0, scroll_line - 1)
            elif ch in (curses.KEY_DOWN,):
                scroll_line = min(max(0, len(chapter_lines) - view_h), scroll_line + 1)
            elif ch in (curses.KEY_PPAGE,):
                scroll_line = max(0, scroll_line - view_h)
            elif ch in (curses.KEY_NPAGE,):
                scroll_line = min(max(0, len(chapter_lines) - view_h), scroll_line + view_h)
            elif ch in (curses.KEY_HOME,):
                scroll_line = 0
            elif ch in (curses.KEY_END,):
                scroll_line = max(0, len(chapter_lines) - view_h)
            elif ch in (curses.KEY_LEFT,):
                if cur_chap > 0:
                    cur_chap -= 1
                    scroll_line = 0
                    rebuild_reader()
            elif ch in (curses.KEY_RIGHT,):
                if cur_chap + 1 < len(books[cur_book].chapters):
                    cur_chap += 1
                    scroll_line = 0
                    rebuild_reader()
            elif ch in (ord("b"), ord("B"), 27):
                chap_sel = cur_chap
                chap_top = max(0, chap_sel - max(1, h - 3) // 2)
                state = "chapters"
            elif ch in (ord("g"), ord("G")):
                s = _prompt_line(stdscr, "Ir para verso (numero): ")
                if s:
                    try:
                        v = int(s.strip()) - 1
                        if 0 <= v < len(verse_to_line):
                            scroll_line = verse_to_line[v]
                    except ValueError:
                        pass
            elif ch in (ord("/"),):
                q = _prompt_line(stdscr, "Buscar (global): ")
                if q:
                    last_query = q
                    search_hits = _search_all(books, q)
                    search_sel = 0
                    search_top = 0
                    state = "search"

        elif state == "search":
            if ch in (ord("b"), ord("B"), 27):
                # volta para um estado razoavel
                state = "reader"
                rebuild_reader()
            elif ch in (curses.KEY_UP,):
                search_sel = max(0, search_sel - 1)
            elif ch in (curses.KEY_DOWN,):
                search_sel = min(max(0, len(search_hits) - 1), search_sel + 1)
            elif ch in (curses.KEY_PPAGE,):
                search_sel = max(0, search_sel - max(1, h - 4))
            elif ch in (curses.KEY_NPAGE,):
                search_sel = min(max(0, len(search_hits) - 1), search_sel + max(1, h - 4))
            elif ch in (10, 13, curses.KEY_ENTER):
                if 0 <= search_sel < len(search_hits):
                    hit = search_hits[search_sel]
                    cur_book = hit.book_i
                    cur_chap = hit.chap_i
                    rebuild_reader()
                    # posiciona no verso
                    if verse_to_line and 0 <= hit.verse_i < len(verse_to_line):
                        scroll_line = verse_to_line[hit.verse_i]
                    state = "reader"

        # Resize: reconstrua linhas do capitulo para novo width.
        if ch == curses.KEY_RESIZE:
            rebuild_reader()


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--json", dest="json_path", default=None, help="Caminho do JSON ACF (acf_clean.json/acf.json).")
    ap.add_argument("--selftest", action="store_true", help="Carrega o JSON e imprime um resumo (sem curses).")
    args = ap.parse_args(argv)

    json_path: Optional[Path]
    if args.json_path:
        json_path = Path(args.json_path).expanduser()
    else:
        json_path = discover_default_json()

    if not json_path or not json_path.exists():
        print("ERRO: nao achei o JSON da Biblia ACF.")
        print("Passe explicitamente: --json /caminho/para/acf_clean.json")
        return 2

    books = load_bible(json_path)
    if args.selftest:
        total_verses = sum(len(ch) for b in books for ch in b.chapters)
        print("OK")
        print("JSON:", json_path)
        print("Livros:", len(books))
        print("Versos:", total_verses)
        print("Primeiro livro:", books[0].name, f"({len(books[0].chapters)} capitulos)")
        print("Ultimo livro:", books[-1].name, f"({len(books[-1].chapters)} capitulos)")
        return 0

    # curses.wrapper garante reset do terminal em excecoes.
    return curses.wrapper(lambda stdscr: run_tui(stdscr, books, json_path))


if __name__ == "__main__":
    raise SystemExit(main())
