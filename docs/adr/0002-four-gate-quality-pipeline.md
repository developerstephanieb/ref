# ADR-0002: Four-gate quality pipeline (ruff, mypy, pytest)

- Status: Accepted
- Date: 2026-07-02

## Context

This repo holds reference material where correctness and consistency are verified by assert-backed proof: each topic's `mechanics.py` proves its empirical claims with `assert`, and a root test harness runs those files to catch future regressions. Enforcement must be automated and give fast local feedback, so that a red CI is the exception, not how problems normally surface.

## Decision

Run four gates, in order, both locally and in CI: `ruff check` (lint) → `ruff format` (formatting) → `mypy` (strict types) → `pytest` (tests).

**Pipeline topology & execution**
- **Sequential CI job:** The four gates run as ordered steps in a single CI job, cheapest gate first, and the job stops at the first failing step. This is fail-fast in the useful sense (a lint error fails in seconds without waiting for the test suite) while keeping one job, one `uv sync`, and one required status check.
- **Lint before format:** Lint (with `--fix` locally) runs before the formatter: a lint autofix (e.g., import sorting under `I`) rewrites code that the formatter then lays out, so running lint first lets everything settle in one pass. 
- **Fix locally, verify in CI:** pre-commit fixes (`ruff check --fix`, `ruff format`); CI verifies (`ruff check`, `ruff format --check`). mypy has no fix mode and is identical in both. pytest runs in CI only.
- **Hook style:** pre-commit hooks are local and call `uv run <tool>`, not the upstream ruff/mypy mirror hooks.

**Rule scope**
- **ruff:** Selects exactly `["E", "F", "I", "B", "UP"]` — pycodestyle errors, pyflakes, import sorting, flake8-bugbear, pyupgrade.
- **mypy:** Runs with `strict = true`.

## Alternatives considered

**ruff rule selection**
- **`S` (flake8-bandit):** Rejected. `S101` flags every `assert`, but assertions are the load-bearing proof mechanism here, so `S` would fire on exactly what the methodology does on purpose. `S603`/`S607` would also flag the harness running `mechanics.py` via subprocess, which also intentional. bandit's assumptions are wrong for reference code: a deliberate omission, not a security gap.
- **`ANN` (flake8-annotations):** Rejected as redundant. mypy `strict` already enforces annotation coverage; `ANN` would repeat the signal with noisier messages.
- **`D` (pydocstyle):** Rejected. Docstrings-everywhere is disproportionate for short teaching snippets; noise without matching value.
- **`RUF` (Ruff-native) and `PT` (flake8-pytest-style):** Deferred. Both are low-noise and on-theme (`RUF100` catches a stale `# noqa` that suppresses nothing; `PT018` splits a composite `assert a and b` so a failure names which half broke). But their value is contingent: `RUF100` pays off only once suppressions exist, and `PT` scales with pytest machinery (fixtures, `parametrize`, `raises`) not yet used much. Kept out of the starting set to avoid complexity without present payoff; revisit when the first `# noqa` lands or the test suite grows richer.
- **`SIM` (flake8-simplify):** Rejected. Like `D`, this is a fit problem: `SIM` rewrites for brevity (`SIM108` ternary, `SIM110` `all(...)`), but reference material is read to be learned from, and an explicit `if/else` or accumulator loop is often the clearer teacher.
- **`ALL`:** Rejected. Pulls in the above plus churny, mutually conflicting rules, needing a long ignore-list to stay usable. A small explicit select states intent clearly.

**Pipeline structure**
- **Parallel jobs (separate concurrent `lint` / `type` / `test`):** Deferred on cost, not capability. Separate top-level jobs would run to completion and surface all failures in one run, so that benefit is real. But for a pipeline that finishes in seconds the wall-clock saving is negligible, while each job repeats checkout, cache restore, and `uv sync` (roughly tripling setup) and turns one required status check into three. Revisit when `pytest` scales into minutes. (This applies to *separate jobs*; if the three checks were a `matrix` instead, `fail-fast` defaults to true and would cancel siblings on first failure; a reason to prefer separate jobs over a matrix whenever we do parallelize.)

**Pre-commit hook style**
- **Upstream mirror hooks** (`astral-sh/ruff-pre-commit`, `mirrors-mypy`): Rejected. Each pins its own tool version via `rev:`, independent of `uv.lock`, so pre-commit's ruff/mypy can drift from CI's `uv run` versions and give a false green locally. The mypy mirror hook also runs in an isolated environment that can't see project types. Rejected for local `uv run` hooks, so local and CI run the same tool from the same locked environment.

## Consequences

- **Single source of truth:** A single pipeline definition governs the workspace; the concrete settings live in `CONVENTIONS.md`.
- **Local/CI parity:** They agree by construction — same tools, same environment, same order.
- **Fast commits:** Leaving pytest out of pre-commit keeps commits quick; CI is the test backstop.
- **Whole-tree typing:** The mypy hook uses `pass_filenames: false` and runs `mypy .` rather than on staged files (see ADR-0003 for the resolution constraint that forces this).
- **Single required check:** One sequential job means branch protection needs one required check (`check`), not one per gate. Splitting into parallel jobs later means re-wiring that ruleset.