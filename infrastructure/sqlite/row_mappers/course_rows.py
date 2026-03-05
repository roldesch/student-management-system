# infrastructure/sqlite/row_mappers/course_rows.py

from __future__ import annotations

from typing import Dict, Any
import sqlite3

from ._utils import require_columns

def course_row_to_primitives(row: sqlite3.Row) -> Dict[str, Any]:
    """
    Base Course row.

    REQUIRED columns:
        - course_code
        - course_name
        - course_teacher_id  (nullable allowed)
    """
    require_columns(
        row,
        "course_code",
        "course_name",
        "course_teacher_id",
    )

    return {
        "course_code": row["course_code"],
        "course_name": row["course_name"],
        "course_teacher_id": row["course_teacher_id"],
    }


def course_teacher_join_row_to_primitives(row: sqlite3.Row) -> Dict[str, Any]:
    """
    Course ↔ Teacher join row.

    REQUIRED columns:
        - course_code
        - teacher_id
        - teacher_name
    """
    require_columns(
        row,
        "course_code",
        "teacher_id",
        "teacher_name",
    )

    return {
        "course_code": row["course_code"],
        "teacher": {
            "teacher_id": row["teacher_id"],
            "teacher_name": row["teacher_name"],
        },
    }


def course_student_join_row_to_primitives(row: sqlite3.Row) -> Dict[str, Any]:
    """
    Course ↔ Enrollment ↔ Student join row.

    REQUIRED columns:
        - course_code
        - student_id
        - student_name
        - grade   (nullable allowed)
    """
    require_columns(
        row,
        "course_code",
        "student_id",
        "student_name",
        "grade",
    )

    return {
        "course_code": row["course_code"],
        "student": {
            "student_id": row["student_id"],
            "student_name": row["student_name"],
        },
        "grade": row["grade"],
    }
