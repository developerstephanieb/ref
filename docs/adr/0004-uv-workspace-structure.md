# ADR-0004: Virtual uv workspace with `package = false` members

- Status: Accepted
- Date: 2026-07-02

## Context

This repo collects several code domains (`python`, `dsa`, `cs_fundamentals`) alongside a prose-only domain (`sdlc`). They share one repository so they can share a CI pipeline, cross-link between concepts, and draw on one central toolchain. But these domains are not installable libraries: forcing them into a build backend would add a build step and a version number for something that is never installed. The domains must be isolated from one another without any of them being published.

## Decision

We structure the repo as a uv workspace.

**Workspace layout**
- **Virtual root:** The root `pyproject.toml` declares `[tool.uv.workspace]` and is marked `package = false`. It builds and installs nothing; it exists to anchor dependency resolution and hold the shared tool config (`ruff`, `mypy`, `pytest`). One `uv sync` installs the shared dev group for every member from a single lockfile.
- **Non-distributable members:** The code domains (`python`, `dsa`, `cs_fundamentals`) are registered as members, each with its own `pyproject.toml` also marked `package = false` (runnable scripts, not installable libraries).
- **Prose stays out of the graph:** Domains with no Python (`sdlc`) are left out of the workspace and live as plain documentation directories alongside it.

## Alternatives considered

- **A separate repo per domain:** Rejected. Loses cross-linking between domains, multiplies toolchain and CI setup per domain, and fragments the single Anki deck.
- **One flat package, no workspace:** Rejected. Simpler, but couples unrelated domains into a single importable namespace and blurs per-member boundaries; the workspace gives member isolation while still sharing one toolchain and lockfile.
- **Real installable packages (`package = true`):** Rejected. Would require build backends and version management for material that is never `pip install`-ed.
- **Including `sdlc` as a member:** Rejected. It contains no Python, so forcing it into the package graph adds an empty package with no operational value.

## Consequences

- **Global reproducibility:** One `uv sync --locked` resolves and installs the whole tree from a single lockfile.
- **Single config source:** The root `pyproject.toml` is the single source of truth for lint, type, and test settings across all members.
- **Adding a member:** A small, documented procedure — create `<member>/pyproject.toml` with `package = false`, add the directory to `members`, and relock (recorded in `CONVENTIONS.md`).
- **Name-collision constraint:** The root project name must not match any member name, or `uv sync` fails on a duplicate (noted in the root `pyproject.toml`).