#!/usr/bin/env python3
"""
anki_gen.py -- build one Anki-importable TSV from every cards.md in the workspace.

Each card's deck is derived from its top-level member directory, so cards file
themselves into per-domain subdecks under a shared base deck:

    python/...          -> Interview Prep::Python
    dsa/...             -> Interview Prep::DSA
    sdlc/...            -> Interview Prep::SDLC
    cs_fundamentals/... -> Interview Prep::CS Fundamentals

Card format (blocks separated by a line containing only `---`):

    Q: front of the card (single line)
    A: back of the card; may span
       multiple lines and contain ```code fences```
    TAGS: space separated tags
    ---

Usage:
    python tools/anki_gen.py                      # scan workspace, write build/anki.tsv
    python tools/anki_gen.py --deck "Prep"        # change the base deck name
    python tools/anki_gen.py --out cards.tsv

Import into Anki: File > Import. The file's header lines set the Tab separator,
enable HTML, and map the Tags and Deck columns automatically; the first time, map
the first two columns to Front / Back. Re-running regenerates the file; keeping the
first field (the question) stable lets Anki update existing notes instead of
duplicating them.

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

# Pretty display names for known members; unknown dirs fall back to a title-cased
# version of the directory name (underscores -> spaces).
DECK_DISPLAY = {
    "python": "Python",
    "dsa": "DSA",
    "sdlc": "SDLC",
    "cs_fundamentals": "CS Fundamentals",
}


@dataclass(frozen=True)
class Card:
    front: str
    back: str
    tags: str
    deck: str
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


def deck_for(cards_file: Path, root: Path, base: str) -> str:
    """Map a cards.md path to a base::Domain deck name from its member directory."""
    rel = cards_file.relative_to(root)
    if len(rel.parts) < 2:  # cards.md sitting at the root, no member dir
        return base
    member = rel.parts[0]
    display = DECK_DISPLAY.get(member, member.replace("_", " ").title())
    return f"{base}::{display}"


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
    return Card(front, "\n".join(back).strip(), tags, "", "")


def parse_file(path: Path, deck: str) -> list[Card]:
    cards: list[Card] = []
    for raw in CARD_SEP.split(path.read_text(encoding="utf-8")):
        if not raw.strip():
            continue
        card = parse_block(raw.strip())
        if card is not None:
            cards.append(Card(card.front, card.back, card.tags, deck, str(path.parent)))
    return cards


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path("."), type=Path)
    parser.add_argument("--out", default=Path("build/anki.tsv"), type=Path)
    parser.add_argument(
        "--deck",
        default="Interview Prep",
        type=str,
        help="base deck name; the member dir becomes a ::subdeck",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    cards: list[Card] = []
    for cards_file in sorted(root.rglob("cards.md")):
        deck = deck_for(cards_file, root, args.deck)
        cards.extend(parse_file(cards_file, deck))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        # Header lines let Anki import without manual separator/HTML/column setup.
        # Columns: 1=Front, 2=Back, 3=Tags, 4=Deck.
        f.write("#separator:tab\n")
        f.write("#html:true\n")
        f.write("#tags column:3\n")
        f.write("#deck column:4\n")
        for card in cards:
            f.write(
                f"{to_html(card.front)}\t{to_html(card.back)}\t"
                f"{card.tags}\t{card.deck}\n"
            )

    by_deck: dict[str, int] = {}
    for card in cards:
        by_deck[card.deck] = by_deck.get(card.deck, 0) + 1
    print(f"wrote {len(cards)} cards to {args.out}")
    for deck in sorted(by_deck):
        print(f"  {by_deck[deck]:>4}  {deck}")


if __name__ == "__main__":
    main()
