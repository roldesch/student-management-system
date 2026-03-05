# infrastructure/sqlite/row_mappers/_utils.py

from __future__ import annotations

import sqlite3


def require_columns(row: sqlite3.Row, *cols: str) -> None:
    """
    Enforce that all required column are present in the sqlite3.Row.

    This function is intentionally:
    - strict
    - non-validating
    - non-coercing

    Missing columns raise immediately.
    """
    missing = [c for c in cols if c not in row.keys()]
    if missing:
        raise KeyError(
            f"Row missing required columns: {missing}."
            f"Available columns: {row.keys()}"
        )

