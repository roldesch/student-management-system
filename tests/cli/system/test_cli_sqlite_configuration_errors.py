#

from pathlib import Path

from tests.cli.subprocess._cli_runner import run_cli


def test_cli_sqlite_missing_path_exits_2_configuration_error() -> None:
    """
    When SMS_BACKEND=sqlite and SMS_SQLITE_PATH is missing,
    CLI must exit deterministically with exit code 2 and
    a stable configuration error message.
    """

    result = run_cli(
        "student", "list",
        backend="sqlite",
        sqlite_path=None,  # Explicitly omitted
    )

    assert result.returncode == 2
    assert "Invalid configuration:" in result.stdout


def test_cli_sqlite_relative_path_exits_2_configuration_error(tmp_path: Path) -> None:
    """
    When SMS_BACKEND=sqlite and SMS_SQLITE_PATH is relative,
    CLI must reject it deterministically.
    """

    relative_path = Path("relative.db")

    result = run_cli(
        "student", "list",
        backend="sqlite",
        sqlite_path=relative_path,
    )

    assert result.returncode == 2
    assert "Invalid configuration:" in result.stdout