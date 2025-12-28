# tests/cli/subprocess/test_cli_validation_error.py

import subprocess
import sys


def test_cli_validation_error_student_add_invalid_input():
    """
    GIVEN a CLI command that passes argparse
    BUT fails application-level validation
    WHEN executed as a subprocess
    THEN it exits with EXIT_VALIDATION_ERROR (2)
    AND prints a validation error message
    """

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "cli.main",
            "student",
            "add",
            "--id",
            "",                 # invalid: empty identifier
            "--name",
            "John",
        ],
        capture_output=True,
        text=True,
    )

    # Exit code defined by CLI validation contract
    assert result.returncode == 2

    # Validation error should produce user-facing output
    combined_output = (result.stdout + result.stderr).lower()
    assert "invalid input" in combined_output
