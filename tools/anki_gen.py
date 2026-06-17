#!/usr/bin/env python3
"""
anki_gen.py -- build one Anki-importable TSV from every cards.md in the repo.

Card format (blocks separated by a line containing only `---`):

    Q: front of the card (single line)
    A: back of the card; may span
       multiple lines and contain ```code fences```
    TAGS: space separated tags
    ---

Usage:
    python tools/anki_gen.py                 # scan repo, write build/anki.tsv
    python tools/anki_gen.py --out cards.tsv

Import into Anki: File > Import, set field separator to Tab, turn ON
"Allow HTML in fields", and map the columns to Front / Back / Tags. Re-running
regenerates the file; if you keep the first field (the question) stable, Anki
updates existing notes instead of duplicating them.

Convention: keep questions to a single `Q:` line, and don't put a bare `---`
line inside an answer (it is the card separator).
"""

from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from pathlib import Path

CARD_SEP = re.compile(r"^---\s*$", re.MULTILINE)
FENCE = re.compile(r"```[a-zA-Z]*\n?(.*?)```", re.DOTALL)
INLINE_CODE = re.compile(r"`([^`\n]+)`")


@dataclass(frozen=True)
class Card:
    front: str
    back: str
    tags: str
    source: str


def to_html(text: str) -> str:
    """Escape HTML, render ```fences``` as <pre>, and newlines as <br>."""
    stashed: list[str] = []

    def stash(match: re.Match[str]) -> str:
        code = html.escape(match.group(1).strip("\n"))
        stashed.append(f"<pre>{code}</pre>")
        return f"\x00{len(stashed) - 1}\x00"

    text = FENCE.sub(stash, text)
    text = html.escape(text).replace("\n", "<br>")
    text = INLINE_CODE.sub(r"<code>\1</code>", text)
    for i, block in enumerate(stashed):
        text = text.replace(f"\x00{i}\x00", block)
    return text.replace("\t", "    ").strip()


def parse_block(block: str) -> Card | None:
    front, tags = "", ""
    back: list[str] = []
    mode: str | None = None
    for line in block.splitlines():
        if line.startswith("Q:"):
            front, mode = line[2:].strip(), "q"
        elif line.startswith("A:"):
            back, mode = [line[2:].strip()], "a"
        elif line.startswith("TAGS:"):
            tags, mode = line[5:].strip(), None
        elif mode == "a":
            back.append(line)
    if not front or not back:
        return None
    return Card(front, "\n".join(back).strip(), tags, "")


def parse_file(path: Path) -> list[Card]:
    cards: list[Card] = []
    for raw in CARD_SEP.split(path.read_text(encoding="utf-8")):
        if not raw.strip():
            continue
        card = parse_block(raw.strip())
        if card is not None:
            cards.append(Card(card.front, card.back,
                         card.tags, str(path.parent)))
    return cards


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path("."), type=Path)
    parser.add_argument("--out", default=Path("build/anki.tsv"), type=Path)
    args = parser.parse_args()

    cards: list[Card] = []
    for cards_file in sorted(args.root.rglob("cards.md")):
        cards.extend(parse_file(cards_file))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        for card in cards:
            f.write(f"{to_html(card.front)}\t{to_html(card.back)}\t{card.tags}\n")

    print(f"wrote {len(cards)} cards to {args.out}")


if __name__ == "__main__":
    main()
