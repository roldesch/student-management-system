# tests/cli/system/test_cli_backend_substitution_parity.py

import sqlite3
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
    result = run_cli("student", "show", "S99", backend=backend, sqlite_path=sqlite_path)

    # Assert
    assert result.returncode == 4, result.stderr


@pytest.mark.parametrize("backend", ["memory", "sqlite"])
def test_cli_duplicate_student_exits_4_state_error(backend: str, tmp_path: Path) -> None:
    # Arrange
    sqlite_path = tmp_path / "sms.db" if backend == "sqlite" else None
    if sqlite_path is not None:
        assert not sqlite_path.exists()

    # Act
    first = run_cli(
        "student", "add", "--id", "S01", "--name", "Alice",
        backend=backend, sqlite_path=sqlite_path
    )
    second = run_cli(
        "student", "add", "--id", "S01", "--name", "Alice",
        backend=backend, sqlite_path=sqlite_path
    )

    # Assert
    assert first.returncode == 0, first.stderr
    assert second.returncode == 4, second.stderr


@pytest.mark.parametrize("backend", ["memory", "sqlite"])
def test_cli_domain_violation_enroll_twice_exits_3_domain_error(backend: str, tmp_path: Path) -> None:
    # Arrange
    sqlite_path = tmp_path / "sms.db" if backend == "sqlite" else None
    if sqlite_path is not None:
        assert not sqlite_path.exists()

    # Act (precondition setup)
    s = run_cli(
        "student", "add", "--id", "S02", "--name", "Bob",
        backend=backend, sqlite_path=sqlite_path
    )
    c = run_cli(
        "course", "add", "--code", "C01", "--name", "Math",
        backend=backend, sqlite_path=sqlite_path
    )
    first_enroll = run_cli(
        "enroll", "--student", "S02", "--course", "C01",
        backend=backend, sqlite_path=sqlite_path
    )

    # Act (operation under test)
    second_enroll = run_cli(
        "enroll", "--student", "S02", "--course", "C01",
        backend=backend, sqlite_path=sqlite_path
    )

    # Assert
    assert s.returncode == 0, s.stderr
    assert c.returncode == 0, c.stderr
    assert first_enroll.returncode == 0, first_enroll.stderr
    assert second_enroll.returncode == 3, second_enroll.stderr



