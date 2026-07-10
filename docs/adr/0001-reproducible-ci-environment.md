# ADR-0001: Reproducible CI environment (uv lockfile + SHA-pinned actions)

- Status: Accepted
- Date: 2026-07-02

## Context

This repo is a uv-managed Python workspace. For continuous integration (CI) to serve as a trustworthy quality gate, the pipeline must run identically every time (reproducibility) so that tests evaluate the exact committed code (validity). This requires eliminating two sources of silent environmental drift:

1. **Dependency resolution:** Dynamic package resolution during CI risks running tests against a dependency graph that differs from the one committed. The invariant that matters is not the developer's local machine (which may be dirty or unsynced) but the committed lockfile: if CI resolves anything other than what `uv.lock` pins, the pipeline validates a dependency set that was never committed, making the quality gate meaningless.
2. **CI harness mutability:** The GitHub Actions that run the pipeline (repository checkout, uv installation) are third-party code pulled in by version reference. How that reference is written — a moving major tag (`@v7`), a full version tag (`@v7.0.0`), or an exact SHA — determines whether the action's maintainers can change what the pipeline runs without a commit to this repository. If the upstream code changes silently, a previously green pipeline can break or falsely pass with no commit here, and the CI signal can no longer be trusted.

## Decision

We require the dependency graph to be locked and the CI harness to be immutable.

**Dependency resolution**
- **Strict synchronization:** Install dependencies in CI with `uv sync --locked`. The `--locked` flag fails the job if `uv.lock` is out of sync with `pyproject.toml`.
- **Unified resolution:** A single root lockfile resolves all workspace members (see ADR-0004).

**CI harness immutability**
- **Cryptographic pinning:** Pin all actions to a full 40-character commit SHA (the only inherently immutable reference).
- **Legibility requirement:** Each pin carries a trailing comment with the human-readable version.

```yaml
- uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7.0.0
- uses: astral-sh/setup-uv@fac544c07dec837d0ccb6301d7b5580bf5edae39 # v8.2.0
```

**Automated upgrades**
- **Dependabot lifecycle:** Configure Dependabot (`.github/dependabot.yml`) for the github-actions ecosystem to propose SHA bumps, updating both the pin and the comment on reviewable pull requests, so pins stay current without moving silently.

*Note:* If an action is ever reverted from a SHA back to a tag, `astral-sh/setup-uv` needs a full version tag. setup-uv publishes only full-version tags from v8.0.0 (March 2026) onward, so `@v8` does not exist and fails to resolve.

## Alternatives considered

**Dependency management**
- **`uv pip install -r requirements.txt`:** Rejected. Abandons uv's lockfile and resolver model and reintroduces the "works on my machine" gap.
- **`uv sync` without `--locked`:** Rejected. Does not guarantee dependency reproducibility; silently masks lockfile drift.

**CI infrastructure**
- **Moving major tags (`@v7`):** Rejected. The maintainer can repoint the tag on any minor or patch release, changing the harness with no commit here.
- **Full version tags (`@v7.0.0`):** Rejected. Not inherently immutable — tag stability depends on the action's repository opting into immutable releases, not on a platform-wide guarantee. Better than moving tags, but still trust-dependent.
- **SHA-pinning without Dependabot:** Rejected. Freezes the harness entirely, so security patches and bug fixes never land.

## Consequences

- **Reproducible end to end:** A green check means both the resolved environment and the CI harness match the exact committed state.
- **Fail-fast lockfiles:** A stale lockfile fails CI loudly, by design, forcing `pyproject.toml` and `uv.lock` to be committed together.
- **Auditable upgrades:** Action upgrades become explicit, reviewable commits via Dependabot PRs instead of silent tag moves.
- **Legibility trade-off:** A 40-character SHA reduces immediate readability in the workflow file; the trailing version comment exists to keep the version readable at a glance.
- **Maintenance overhead:** Someone must periodically review and merge those PRs, which is the accepted cost of harness immutability.