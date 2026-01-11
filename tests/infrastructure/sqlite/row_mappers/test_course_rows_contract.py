# tests/infrastructure/sqlite/row_mappers/test_course_rows_contract.py

import sqlite3
import pytest

from infrastructure.sqlite.row_mappers.course_rows import (
    course_row_to_primitives,
    course_teacher_join_row_to_primitives,
    course_student_join_row_to_primitives,
)

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
# course_row_to_primitives
# ----------------------

def test_course_row_to_primitives_base_shape():
    # Arrange
    row = _make_row(
        course_code="C01",
        course_name="Math",
        course_teacher_id=None,
    )

    # Act
    result = course_row_to_primitives(row)

    # Assert
    assert result == {
        "course_code": "C01",
        "course_name": "Math",
        "course_teacher_id": None,
    }


def test_course_row_to_primitives_missing_column_raises_key_error():
    # Arrange
    row = _make_row(course_code="C01", course_name="Math")

    # Act / Assert
    with pytest.raises(KeyError):
        course_row_to_primitives(row)


# ----------------------
# course_teacher_join_row_to_primitives
# ----------------------

def test_course_teacher_join_row_to_primitives_shape():
    # Arrange
    row = _make_row(
        course_code="C01",
        teacher_id="T01",
        teacher_name="Dr Smith",
    )

    # Act
    result = course_teacher_join_row_to_primitives(row)

    # Assert
    assert result == {
        "course_code": "C01",
        "teacher": {
            "teacher_id": "T01",
            "teacher_name": "Dr Smith",
        },
    }


def test_course_teacher_join_row_missing_column_raises_key_error():
    # Arrange
    row = _make_row(course_code="C01", teacher_id="T01")

    # Act / Assert
    with pytest.raises(KeyError):
        course_teacher_join_row_to_primitives(row)


# ----------------------
# course_student_join_row_to_primitives
# ----------------------

def test_course_student_join_row_to_primitive_shape():
    # Arrange
    row = _make_row(
        course_code="C01",
        student_id="S01",
        student_name="Alice",
        grade=9.5,
    )

    # Act
    result = course_student_join_row_to_primitives(row)

    # Assert
    assert result == {
        "course_code": "C01",
        "student": {
            "student_id": "S01",
            "student_name": "Alice",
        },
        "grade":9.5,
    }


def test_course_student_join_row_missing_column_raises_key_error():
    # Arrange
    row = _make_row(
        course_code="C01",
        student_id="S01",
        student_name="Alice",
    )

    # Act / Assert
    with pytest.raises(KeyError):
        course_student_join_row_to_primitives(row)
