# tests/cli/subprocess/test_cli_enroll_and_errors.py
from tests.cli.subprocess._cli_runner import run_cli


def test_student_add_validation_error():
    result = run_cli(
        "student", "add",
        "--id", "",
        "--name", "Alice"
    )

    assert result.returncode == 2

    combined = (result.stdout + result.stderr).lower()
    assert "invalid input" in combined


def test_enroll_fails_when_entities_do_not_exist():
    result = run_cli(
        "enroll",
        "--student", "S01",
        "--course", "C01",
    )

    assert result.returncode == 4

    combined = (result.stdout + result.stderr).lower()
    assert "state" in combined or "not found" in combined
