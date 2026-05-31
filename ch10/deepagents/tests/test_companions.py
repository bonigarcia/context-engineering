from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_script(*parts: str, args: list[str] | None = None) -> str:
    script = ROOT.joinpath(*parts)
    result = subprocess.run(
        [sys.executable, str(script), *(args or [])],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_file_context_trims_notes() -> None:
    output = run_script("file_context", "file_context.py")

    assert "# File context" in output
    assert "trimmed" in output.lower()
    assert "bounded note buffer" in output.lower()


def test_subagent_delegation_shows_split_steps() -> None:
    output = run_script("subagent_delegation", "subagent_delegation.py")

    assert "# Subagent delegation" in output
    assert "select files" in output.lower()
    assert "merge" in output.lower()


def test_planning_loop_shows_multiple_passes() -> None:
    output = run_script("planning_loop", "planning_loop.py")

    assert "# Planning loop" in output
    assert output.lower().count("pass") >= 2
    assert "reduced context" in output.lower()


def test_human_approval_can_resume_without_interaction() -> None:
    output = run_script("human_approval", "human_approval.py", args=["--auto-approve"])

    assert "# Human approval" in output
    assert "awaiting approval" in output.lower()
    assert "approved" in output.lower()
