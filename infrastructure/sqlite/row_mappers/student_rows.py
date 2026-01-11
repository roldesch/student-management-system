# infrastructure/sqlite/row_mappers/student_rows.py

from __future__ import annotations

from typing import Dict, Any
import sqlite3

from ._utils import require_columns


def student_row_to_primitives(row: sqlite3.Row) -> Dict[str, Any]:
    """
    REQUIRED columns (aliased by repository SQL):
        - student_id
        - student_name
    """
    require_columns(row, "student_id", "student_name")

    return {
        "student_id": row["student_id"],
        "student_name": row["student_name"],
    }