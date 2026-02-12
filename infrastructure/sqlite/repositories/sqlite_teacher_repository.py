# infrastructure/sqlite/repositories/sqlite_teacher_repository.py

from __future__ import annotations

import sqlite3
from typing import Iterable

from domain.models.teacher import Teacher
from domain.repositories.teacher_repository import TeacherRepository

from domain.exceptions.domain_exceptions import (
    EntityNotFoundError,
    DuplicateEntityError,
)
from infrastructure.sqlite.errors import (PersistenceError)

from infrastructure.sqlite.row_mappers.teacher_rows import teacher_row_to_primitives


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


    # ------------------------------------------------------------------
    # add(teacher_id)
    # ------------------------------------------------------------------
    def add(self, teacher: Teacher) -> None:
        try:
            self._connection.execute(
                """
                INSERT INTO teachers (teacher_id, name)
                VALUES (?, ?)
                """,
                (teacher.id, teacher.name),    # domain id -> persistence teacher_id
            )
        except sqlite3.IntegrityError as exc:
            # Currently safe: only PK constraint exists on teachers.teacher_id
            raise DuplicateEntityError(str(exc)) from exc
        except sqlite3.Error as exc:
            raise PersistenceError(str(exc)) from exc

    # ------------------------------------------------------------------
    # get(teacher_id)
    # ------------------------------------------------------------------
    def get(self, teacher_id: str) -> Teacher:
        try:
            cursor = self._connection.execute(
                """
                SELECT
                    t.teacher_id AS teacher_id,
                    t.name AS teacher_name
                FROM teachers t
                WHERE t.teacher_id = ?
                """,
                (teacher_id,),
            )
            row = cursor.fetchone()
        except sqlite3.Error as exc:
            raise PersistenceError(str(exc)) from exc

        if row is None:
            raise EntityNotFoundError(f"Teacher not found: {teacher_id}")

        primitives = teacher_row_to_primitives(row)

        # Reconstruction only - no mutators, no relationships
        return Teacher(
            teacher_id=primitives["teacher_id"],
            name=primitives["teacher_name"],
        )

    # ------------------------------------------------------------------
    # remove(teacher_id)
    # ------------------------------------------------------------------
    def remove(self, teacher_id: str) -> None:
        try:
            cursor = self._connection.execute(
                """
                DELETE FROM teachers
                WHERE teacher_id = ?
                """,
                (teacher_id,),
            )
        except sqlite3.Error as exc:
            raise PersistenceError(str(exc)) from exc

        if cursor.rowcount == 0:
            raise EntityNotFoundError(f"Teacher not found: {teacher_id}")


    # ------------------------------------------------------------------
    # list_all()
    # ------------------------------------------------------------------
    def list_all(self) -> Iterable[Teacher]:
        try:
            cursor = self._connection.execute(
                """
                SELECT
                    t.teacher_id AS teacher_id,
                    t.name AS teacher_name
                FROM teachers t
                ORDER BY t.teacher_id
                """
            )
            rows = cursor.fetchall()
        except sqlite3.Error as exc:
            raise PersistenceError(str(exc)) from exc

        for row in rows:
            primitives = teacher_row_to_primitives(row)
            yield Teacher(
                teacher_id=primitives["teacher_id"],
                name=primitives["teacher_name"],
            )
