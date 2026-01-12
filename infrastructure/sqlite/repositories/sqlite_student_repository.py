# infrastructure/sqlite/repositories/sqlite_student_repository.py

from __future__ import annotations

import sqlite3
from typing import Iterable

from domain.models.student import Student
from domain.repositories.student_repository import StudentRepository


class SQLiteStudentRepository(StudentRepository):
    """
    SQLite Student Repository — Phase 3

    This repository is governed by an authoritative SQL contract:
        SQLite Student Repository — SQL Contract (Phase 3)

    Rules (binding):
    - Interacts with the `students` table only
    - Executes ONLY the SQL statements defined in the contract
    - Column aliases MUST match student_row_to_primitives
    - No joins, no relationship access, no upserts
    - Persistence errors only (no domain or validation logic)

    Any deviation requires explicit architectural review.
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add(self, student: Student) -> None:
        raise NotImplementedError

    def get(self, student_id: str) -> Student:
        raise NotImplementedError

    def remove(self, student_id: str) -> None:
        raise NotImplementedError

    def list_all(self) -> Iterable[Student]:
        raise NotImplementedError
