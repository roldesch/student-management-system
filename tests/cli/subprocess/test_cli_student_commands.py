# tests/cli/subprocess/test_cli_student_commands.py

import subprocess
import sys


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "cli.main", *args],
        capture_output=True,
        text=True,
    )


def test_student_add_success():
    result = run_cli(
        "student", "add",
        "--id", "S01",
        "--name", "Alice",
    )

    assert result.returncode == 0
    assert "success" in (result.stdout + result.stderr).lower()


def test_student_show_not_found():
    result = run_cli("student", "show", "S01")

    assert result.returncode == 4

    combined = (result.stdout + result.stderr).lower()
    assert "state" in combined or "not found" in combined