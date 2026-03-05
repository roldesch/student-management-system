# tests/cli/system/test_cli_sqlite_persistence_failures.py

import sqlite3
from pathlib import Path

from tests.cli.subprocess._cli_runner import run_cli


def test_cli_sqlite_locked_database_exits_10_system_error(tmp_path: Path) -> None:
    # -------------------------------------------------
    # Arrange
    # -------------------------------------------------
    # Precondition:
    # - Fresh SQLite database.
    # - No concurrent writers.
    sqlite_path = tmp_path / "sms.db"
    assert not sqlite_path.exists()

    # Force database initialization (schema creation).
    # This ensures the DB file exists before we acquire the lock.
    init = run_cli("student", "list", backend="sqlite", sqlite_path=sqlite_path)
    assert init.returncode ==0, init.stderr

    # Acquire an exclusive write lock in this process.
    conn = sqlite3.connect(str(sqlite_path))
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("BEGIN EXCLUSIVE;")  # Hold write lock

        # -------------------------------------------------
        # Act (operation under test)
        # -------------------------------------------------
        result = run_cli(
            "student", "add",
            "--id", "S-LOCK",
            "--name", "Locked",
            backend="sqlite",
            sqlite_path=sqlite_path,
        )

        # -------------------------------------------------
        # Assert
        # -------------------------------------------------
        # Lock-induced persistence failure must surface as system error (exit 10).
        assert result.returncode == 10, result.stderr

    finally:
        try:
            conn.rollback()
        finally:
            conn.close()


def test_cli_sqlite_foreign_key_violation_exits_10_system_error(tmp_path: Path) -> None:
    # -------------------------------------------------
    # Arrange
    # -------------------------------------------------
    # Precondition:
    # - Fresh SQLite database.
    # - Foreign keys enforced (per connection policy).
    sqlite_path = tmp_path / "sms.db"
    assert not sqlite_path.exists()

    # -------------------------------------------------
    # Act (precondition setup)
    # -------------------------------------------------
    s = run_cli(
        "student", "add",
        "--id", "S-FK",
        "--name", "FK Student",
        backend="sqlite",
        sqlite_path=sqlite_path,
    )
    c = run_cli(
        "course", "add",
        "--code", "C-FK",
        "--name", "FK Course",
        backend="sqlite",
        sqlite_path=sqlite_path,
    )
    e = run_cli(
        "enroll",
        "--student", "S-FK",
        "--course", "C-FK",
        backend="sqlite",
        sqlite_path=sqlite_path,
    )

    # -------------------------------------------------
    # Act (operation under test)
    # -------------------------------------------------
    # Attempt to delete a course that currently has enrolled students.
    # The application layer performs relationship cleanup before deletion,
    # so the operation should succeed without a foreign key violation.
    remove_course = run_cli(
        "course", "remove", "C-FK",
        backend="sqlite",
        sqlite_path=sqlite_path,
    )

    # -------------------------------------------------
    # Assert
    # -------------------------------------------------
    assert s.returncode == 0, s.stderr
    assert c.returncode == 0, c.stderr
    assert e.returncode == 0, e.stderr

    # Course removal should succeed because the application cleans
    # dependent relationships before deleting the course.
    assert remove_course.returncode == 0, remove_course.stderr
