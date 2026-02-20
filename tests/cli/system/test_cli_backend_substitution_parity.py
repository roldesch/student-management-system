# tests/cli/system/test_cli_backend_substitution_parity.py

from pathlib import Path

import pytest

from tests.cli.subprocess._cli_runner import run_cli

@pytest.mark.parametrize("backend", ["memory", "sqlite"])
def test_cli_missing_student_exits_4_state_error(backend: str, tmp_path: Path) -> None:
    # Arrange
    # Precondition: system contains no student with id "S99"
    sqlite_path = tmp_path / "sms.db" if backend == "sqlite" else None
    if sqlite_path is not None:
        assert not sqlite_path.exists()

    # Act
    result = run_cli(
        "student",
        "show",
        "S99",
        backend=backend,
        sqlite_path=sqlite_path,
    )

    # Assert
    assert result.returncode == 4, result.stderr


def test_cli_duplicate_student_exits_4_state_error_sqlite_only(tmp_path: Path) -> None:
    # Arrange
    sqlite_path = tmp_path / "sms.db"
    assert not sqlite_path.exists()

    # Arrange (precondition setup)
    first = run_cli(
        "student",
        "add",
        "--id",
        "S01",
        "--name",
        "Alice",
        backend="sqlite",
        sqlite_path=sqlite_path,
    )
    assert first.returncode == 0, first.stderr

    # Act
    second = run_cli(
        "student",
        "add",
        "--id",
        "S01",
        "--name",
        "Alice",
        backend="sqlite",
        sqlite_path=sqlite_path,
    )

    # Assert
    assert second.returncode == 4, second.stderr


def test_cli_domain_violation_enroll_twice_exits_3_domain_error_sqlite_only(tmp_path: Path) -> None:
    # Arrange
    sqlite_path = tmp_path / "sms.db"
    assert not sqlite_path.exists()

    # Arrange (precondition setup)
    s = run_cli(
        "student",
        "add",
        "--id",
        "S02",
        "--name",
        "Bob",
        backend="sqlite",
        sqlite_path=sqlite_path,
    )
    assert s.returncode == 0, s.stderr

    c = run_cli(
        "course",
        "add",
        "--code",
        "C01",
        "--name",
        "Math",
        backend="sqlite",
        sqlite_path=sqlite_path,
    )
    assert c.returncode == 0, c.stderr

    first_enroll = run_cli(
        "enroll",
        "--student",
        "S02",
        "--course",
        "C01",
        backend="sqlite",
        sqlite_path=sqlite_path,
    )
    assert first_enroll.returncode == 0, first_enroll.stderr


    # Act (operation under test)
    second_enroll = run_cli(
        "enroll",
        "--student",
        "S02",
        "--course",
        "C01",
        backend="sqlite",
        sqlite_path=sqlite_path,
    )

    # Assert
    assert second_enroll.returncode == 3, second_enroll.stderr



