# tests/infrastructure/sqlite/row_mappers/test_teacher_rows_contract.py

import sqlite3
import pytest

from infrastructure.sqlite.row_mappers.teacher_rows import teacher_row_to_primitives

def _make_row(**columns):
    """
    Helper to create a real sqlite3.Row object.

    This helper intentionally:
    - Uses a real in-memory SQLite database
    - Produces a real sqlite3.Row (no mocks)
    - Closes the connection deterministically
    """
    connection = sqlite3.connect(":memory:")
    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cols = ", ".join(columns.keys())
        placeholders = ", ".join(["?"] * len(columns))
        cursor.execute(f"CREATE TABLE test ({cols})")
        cursor.execute(
            f"INSERT INTO test ({cols}) VALUES ({placeholders})",
            tuple(columns.values()),
        )
        cursor.execute("SELECT * FROM test")
        return cursor.fetchone()
    finally:
        connection.close()


# ----------------------
# teacher_row_to_primitives
# ----------------------

def test_teacher_row_to_primitives_returns_exact_keys():
    # Arrange
    row = _make_row(teacher_id="T01", teacher_name="Dr Smith")

    # Act
    result = teacher_row_to_primitives(row)

    # Assert
    assert result == {
        "teacher_id": "T01",
        "teacher_name": "Dr Smith",
    }


def test_teacher_row_to_primitives_missing_column_raises_key_error():
    # Arrange
    row = _make_row(teacher_id="T01")

    # Act / Assert
    with pytest.raises(KeyError):
        teacher_row_to_primitives(row)