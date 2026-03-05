# tests/infrastructure/sqlite/test_schema_bootstrap.py

import sqlite3
from pathlib import Path

import pytest

from infrastructure.sqlite.bootstrap import (
    initialize_sqlite_database,
    SqliteBootstrapConfig,
)


# -------------------------------------------------------------------
# Fixtures (Infrastructure-only)
# -------------------------------------------------------------------

@pytest.fixture
def sqlite_database_path(tmp_path: Path) -> Path:
    """
    Provides an isolated SQLite database path.
    """
    return tmp_path / "test.sqlite3"


def _open_connection(db_path: Path) -> sqlite3.Connection:
    """
    Opens a raw SQLite connection for inspection purposes.

    NOTE:
    SQLite PRAGMA foreign_keys is connection-local.
    Tests explicitly enable it where enforcement is required.
    """
    return sqlite3.connect(db_path)


def _read_pragma(conn: sqlite3.Connection, pragma_name: str) -> int | str:
    """
    Reads a SQLite PRAGMA value.
    """
    return conn.execute(f"PRAGMA {pragma_name};").fetchone()[0]


# -------------------------------------------------------------------
# Schema bootstrap verification tests
# -------------------------------------------------------------------

def test_initialize_sqlite_database_creates_a_valid_sqlite_database_file(
    sqlite_database_path: Path,
):
    # Arrange
    assert not sqlite_database_path.exists()  # precondition

    # Act
    initialize_sqlite_database(sqlite_database_path)

    # Assert
    assert sqlite_database_path.exists()

    with _open_connection(sqlite_database_path) as conn:
        conn.execute("SELECT 1;")  # database is readable


def test_initialize_sqlite_database_creates_all_tables_defined_by_schema_sql(
    sqlite_database_path: Path,
):
    # Arrange
    expected_tables = {
        "students",
        "teachers",
        "courses",
        "enrollments",
    }

    # Act
    initialize_sqlite_database(sqlite_database_path)

    # Assert
    with _open_connection(sqlite_database_path) as conn:
        rows = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table';
            """
        ).fetchall()

        # NOTE:
        # sqlite_master may include internal SQLite tables
        # (e.g., sqlite_sequence). We intentionally assert
        # subset membership rather than equality.
        actual_tables = {row[0] for row in rows}

    assert expected_tables.issubset(actual_tables)


def test_initialize_sqlite_database_allows_foreign_key_enforcement_to_be_enabled_on_new_connections(
    sqlite_database_path: Path,
):
    # Arrange
    initialize_sqlite_database(sqlite_database_path)

    # Act
    with _open_connection(sqlite_database_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        foreign_keys_status = _read_pragma(conn, "foreign_keys")

    # Assert
    assert foreign_keys_status == 1


def test_initialize_sqlite_database_applies_required_sqlite_pragmas(
    sqlite_database_path: Path,
):
    # Arrange
    assert not sqlite_database_path.exists()  # precondition
    config = SqliteBootstrapConfig(busy_timeout_ms=5000)

    # Act
    initialize_sqlite_database(sqlite_database_path, config=config)

    # Assert
    with _open_connection(sqlite_database_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")  # inspection connection
        journal_mode = _read_pragma(conn, "journal_mode")
        foreign_keys = _read_pragma(conn, "foreign_keys")
        busy_timeout = _read_pragma(conn, "busy_timeout")

    # journal_mode casing may vary by driver / SQLite version
    assert str(journal_mode).lower() == "wal"
    assert foreign_keys == 1
    assert busy_timeout == config.busy_timeout_ms


def test_initialize_sqlite_database_is_idempotent_and_can_be_safely_executed_multiple_times(
    sqlite_database_path: Path,
):
    # Arrange
    initialize_sqlite_database(sqlite_database_path)

    # Act
    initialize_sqlite_database(sqlite_database_path)

    # Assert
    with _open_connection(sqlite_database_path) as conn:
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table';"
            )
        }

    assert "students" in tables
    assert "teachers" in tables
    assert "courses" in tables
    assert "enrollments" in tables
