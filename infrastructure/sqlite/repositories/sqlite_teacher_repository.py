# infrastructure/sqlite/repositories/sqlite_teacher_repository.py

from __future__ import annotations

import sqlite3
from typing import Iterable

from domain.models.teacher import Teacher
from domain.repositories.teacher_repository import TeacherRepository


class SQLiteTeacherRepository(TeacherRepository):
    """
    SQLite Teacher Repository — Phase 3

    This repository is governed by an authoritative SQL contract:
        SQLite Teacher Repository — SQL Contract (Phase 3)

    Rules (binding):
    - Interacts with the `teachers` table only
    - Executes ONLY the SQL statements defined in the contract
    - Column aliases MUST match teacher_row_to_primitives
    - No joins, no relationship access, no upserts
    - Persistence errors only (no domain or validation logic)

    Any deviation requires explicit architectural review.
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add(self, teacher: Teacher) -> None:
       raise NotImplementedError


    def get(self, teacher_id: str) -> Teacher:
        raise NotImplementedError


    def remove(self, teacher_id: str) -> None:
        raise NotImplementedError

    def list_all(self) -> Iterable[Teacher]:
        raise NotImplementedError
