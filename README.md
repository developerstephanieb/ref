# ref

> A verification-first, reference workspace — Python internals, data
> structures & algorithms, CS fundamentals, and the software lifecycle — where every claim
> is proven by runnable, assert-backed code or a written derivation.

[![CI](https://github.com/developerstephanieb/ref/actions/workflows/ci.yml/badge.svg)](https://github.com/developerstephanieb/ref/actions/workflows/ci.yml)

A uv workspace that collects several domain references under one roof. Each member is a
self-contained reference; topics cross-link across members, share one toolchain, and compile
into a single spaced-repetition deck.

## Members

| Member            | Scope                                                                           | Form    |
| ----------------- | ------------------------------------------------------------------------------- | ------- |
| `python`          | Python language behavior & CPython internals.                                   | package |
| `dsa`             | Data structures, algorithms, and complexity analysis (incl. interview process). | package |
| `cs_fundamentals` | Hardware/theory below the algorithm layer — number representation, and more.    | package |
| `sdlc`            | Software lifecycle, system design, and operations.                              | docs    |

`python` is the established member; the others are being built out. `sdlc` is prose and
diagrams rather than code, so it isn't a workspace package.

## How it's organized

Each member holds topics under category folders. A code topic is three files:

| File           | Role                                                                                                                                                                                                      |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `README.md`    | **Technical reference** (always visible) + **collapsible deep dives**.                                                                                                                                    |
| `mechanics.py` | Runnable, **assert-backed proof** of every *empirical* claim — the source of truth for the doc's numbers and outputs. (Bounds and correctness are proved in the README; `sdlc` topics usually have none.) |
| `cards.md`     | **Spaced-repetition flashcards** (`Q:` / `A:` / `TAGS:`) compiled into a per-domain Anki subdeck.                                                                                                         |

What "proven" means is scoped per member — run the code, derive it, or cite a source. See
[`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) §A2.

## Quickstart

Requires [uv](https://docs.astral.sh/uv/). Run from the workspace root; uv manages the
shared `.venv` — no need to activate anything.

```bash
uv sync                                                       # build the shared workspace environment
uv run pytest                                                 # run every member's mechanics.py as a regression check
uv run python python/02_builtin_types/float/mechanics.py      # run one topic's proofs and read the labeled output
```

## Build the Anki deck

```bash
uv run python tools/anki_gen.py     # writes build/anki.tsv from every cards.md
```

Each card files into a `::domain` subdeck derived from its member directory. 
Import into Anki: **File → Import**. The file's header lines
set the Tab separator, enable HTML, and map the Tags and Deck columns automatically; the first
time, map the first two columns to **Front / Back**. Keeping the question stable lets re-imports
update notes instead of duplicating them. (Header lines need Anki 2.1.54+; on older versions,
set the separator/HTML and map columns by hand.)

## Quality gates

`ruff` (lint + format) and `pytest` run in CI on every push to `main` and every pull request.
The root test harness discovers every `mechanics.py` across all members and runs each as a
subprocess, so a future Python that changes a documented behavior fails the suite. Reproduce
the checks locally:

```bash
uv run ruff format .          # normalize formatting (run before committing)
uv run ruff check .           # lint
uv run pytest                 # tests
```

## Conventions

One shared spec governs every member: [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md). Part A is
the universal quality bar, verification discipline, and structure; Part B is the per-topic
profile you fill in for each new topic.

## Adding a topic

Copy the per-topic profile from [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) (Part B), fill it
in, and build the files to the conventions. The pytest harness and CI pick up the new
`mechanics.py` automatically — no test or CI wiring required.

## Adding a member

Create `<member>/pyproject.toml` (with `package = false`), then add the directory to
`[tool.uv.workspace] members` in the root `pyproject.toml`. Run `uv sync` to relock.