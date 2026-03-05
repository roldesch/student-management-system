# tests/cli/subprocess/test_cli_usage_error.py

from tests.cli.subprocess._cli_runner import run_cli


def test_cli_usage_error_missing_required_arguments(tmp_path):
    """
    GIVEN an incomplete command that violates argparse requirements
    WHEN the CLI is executed as a subprocess
    THEN it exits with EXIT_USAGE_ERROR (1)
    AND prints usage/help text
    """
    db_path = tmp_path / "sms.db"

    result = run_cli(
        "student",
        "add",
        backend="sqlite",
        sqlite_path=db_path,
    )

    # Exit code defined by CLI contract
    assert result.returncode == 1

    # argparse should emit usage/help text
    combined_output = (result.stdout + result.stderr).lower()
    assert "usage" in combined_output or "required" in combined_output

def test_student_add_missing_arguments(tmp_path):
    db_path = tmp_path / "sms.db"

    result = run_cli(
        "student",
        "add",
        backend="sqlite",
        sqlite_path=db_path,
    )

    assert result.returncode == 1

    combined = (result.stdout + result.stderr).lower()
    assert "usage" in combined or "required" in combined
    