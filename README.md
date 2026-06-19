# ref-python

> A verification-first reference for Python's behavior and internals — where every claim is proven by runnable, assert-backed code.

[![CI](https://github.com/developerstephanieb/ref-python/actions/workflows/ci.yml/badge.svg)](https://github.com/developerstephanieb/ref-python/actions/workflows/ci.yml)

Each topic is a quick technical reference, a set of collapsible deep dives that build the "why", an executable proof of every claim, and spaced-repetition cards for retention.

## How it's organized

Topics live under category folders. Each topic is three files:

| File           | Role                                                                                                                                        |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `README.md`    | **Technical reference** (always visible) + **collapsible deep dives**.                                                                      |
| `mechanics.py` | Runnable, **assert-backed proof** of every claim in the README. The source of truth — the doc's numbers and outputs come from running this. |
| `cards.md`     | **Spaced-repetition flashcards** (`Q:` / `A:` / `TAGS:`) compiled into an Anki deck.                                                        |

## Quickstart

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync                                                 # set up the environment
uv run pytest                                           # run every topic's mechanics.py as a regression check
uv run python 02_builtin_types/float/mechanics.py       # run one topic's proofs and read the labeled output
```

## Build the Anki deck

```bash
uv run python tools/anki_gen.py                      # writes build/anki.tsv from every cards.md
```

Import into Anki: **File → Import**, set the field separator to **Tab**, turn on
**"Allow HTML in fields"**, and map the columns to **Front / Back / Tags**. Keeping the
first field (the question) stable lets re-imports update notes instead of duplicating them.

## Quality gates

`ruff` (lint + format) and `pytest` run in CI on every push to `main` and every pull
request. To reproduce the checks locally:

```bash
uv run ruff format .          # normalize formatting (run before committing)
uv run ruff check .           # lint
uv run pytest                 # tests
```

## Topics

- `builtin_types/float` — Float behavior: representation and imprecision, comparison,
  exactness (`Decimal`/`Fraction`), special values (`nan`/`inf`), integers as floats, and
  floor division.

## Adding a topic

Copy the per-topic profile from [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) (Part B), fill
it in, and build the three files to the conventions. The pytest harness and CI pick up the
new `mechanics.py` automatically — no test or CI wiring required.