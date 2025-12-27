# tests/cli/subprocess/test_cli_usage_error.py

import subprocess
import sys


def test_cli_usage_error_missing_required_arguments():
    """
    GIVEN an incomplete command that violates argparse requirements
    WHEN the CLI is executed as a subprocess
    THEN it exits with EXIT_USAGE_ERROR (1)
    AND prints usage/help text
    """

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "cli.main",
            "student",
            "add",
        ],
        capture_output=True,
        text=True,
    )

    # Exit code defined by CLI contract
    assert result.returncode == 1

    # argparse should emit usage/help text
    combined_output = (result.stdout + result.stderr).lower()
    assert "usage" in combined_output or "required" in combined_output
