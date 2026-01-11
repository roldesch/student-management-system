# infrastructure/sqlite/row_mappers/teacher_rows.py

from __future__ import annotations

from typing import Dict, Any
import sqlite3

from ._utils import require_columns


def teacher_row_to_primitives(row: sqlite3.Row) -> Dict[str, Any]:
    """
    REQUIRED columns (aliased by repository SQL):
        - teacher_id
        - teacher_name
    """
    require_columns(row, "teacher_id", "teacher_name")

    return {
        "teacher_id": row["teacher_id"],
        "teacher_name": row["teacher_name"],
    }

