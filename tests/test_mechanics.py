"""Run every topic's ``mechanics.py`` as a regression check.

Each ``mechanics.py`` is the verification source of truth for its topic's
README: it prints labeled results and backs every documented behavior with
``assert``s. Running it here means a failing assert — e.g. a future Python
release changing a behavior the docs rely on — surfaces as a failed test with
the script's stderr attached.

Running each file as a subprocess (rather than importing it) avoids the
module-name collision you'd hit from many files all named ``mechanics.py``, and
exercises each exactly as ``python mechanics.py`` would.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MECHANICS = sorted(p for p in ROOT.rglob("mechanics.py") if ".venv" not in p.parts)


def test_at_least_one_mechanics_found() -> None:
    """Guard against the glob silently discovering nothing (wrong rootdir)."""
    assert MECHANICS, f"no mechanics.py found under {ROOT}"


@pytest.mark.parametrize("script", MECHANICS, ids=lambda p: p.parent.name)
def test_mechanics_asserts_hold(script: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"{script} failed:\n{result.stderr}"
