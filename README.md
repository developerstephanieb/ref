# ref

> A verification-first reference workspace — Python internals, data structures &
> algorithms, CS fundamentals, and the software lifecycle — where every claim is proven by
> runnable, assert-backed code or a written derivation.

[![CI](https://github.com/developerstephanieb/ref/actions/workflows/ci.yml/badge.svg)](https://github.com/developerstephanieb/ref/actions/workflows/ci.yml)

## Members

| Member            | Scope                                                 | Form    |
| ----------------- | ----------------------------------------------------- | ------- |
| `python`          | Python language behavior & CPython internals.         | package |
| `dsa`             | Data structures, algorithms, and complexity analysis. | package |
| `cs_fundamentals` | Hardware/theory below the algorithm layer.            | package |
| `sdlc`            | Software lifecycle, system design, and operations.    | docs    |

## How it's organized

Each member holds topics under numbered category folders (e.g. `c01_complexity_analysis`,
`c02_builtin_types`). A code topic is three files:

| File           | Role                                                                                          |
| -------------- | --------------------------------------------------------------------------------------------- |
| `README.md`    | Technical reference (always visible) + collapsible deep dives.                                |
| `mechanics.py` | Runnable, assert-backed proof of every *empirical* claim.                                     |
| `cards.md`     | Spaced-repetition flashcards (`Q:` / `A:` / `TAGS:`) compiled into a per-domain Anki subdeck. |

## Quickstart

```bash
uv sync                          # create the shared .venv + install the dev group
uv run ruff check --fix .        # lint (E, F, I, B, UP) + autofix
uv run ruff format .             # format in place   (CI verifies with --check)
uv run mypy .                    # strict type check
uv run pytest                    # discover + run every test across all members
uv run tools/anki_gen.py         # build build/anki.tsv from every cards.md

# run one topic's proofs and read the labeled output:
uv run python python/c02_builtin_types/float/mechanics.py
```

Once per clone, install the git hooks so the fast gates run automatically on every commit:

```bash
uv run pre-commit install
```

## Quality gates

Every push to `main` and every pull request runs four gates in CI: lint, format, type-check,
and tests (`ruff check`, `ruff format --check`, `mypy`, `pytest`). The lint, format, and type
gates also run locally on commit via `pre-commit`. The rules behind these gates live in
[`docs/CONVENTIONS.md`](docs/CONVENTIONS.md); the reasoning is recorded in
[`docs/adr/`](docs/adr/).
