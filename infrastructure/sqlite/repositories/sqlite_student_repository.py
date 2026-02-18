# infrastructure/sqlite/repositories/sqlite_student_repository.py

from __future__ import annotations

import sqlite3
from typing import Iterable

from domain.models.student import Student
from domain.repositories.student_repository import StudentRepository

from domain.exceptions.domain_exceptions import (
    EntityNotFoundError,
    DuplicateEntityError,
)
from infrastructure.sqlite.errors import (
    PersistenceError,
    ForeignKeyViolationError,
)

from infrastructure.sqlite.row_mappers.student_rows import student_row_to_primitives


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

    # ------------------------------------------------------------------
    # add(student_id)
    # ------------------------------------------------------------------
    def add(self, student: Student) -> None:
        try:
            self._connection.execute(
                """
                INSERT INTO students (student_id, name)
                VALUES (?, ?)
                """,
                (student.id, student.name),
            )
        except sqlite3.IntegrityError as exc:
            msg = str(exc).lower()

            # Duplicate student identity → state semantics
            if "unique constraint failed: students.student_id" in msg:
                raise DuplicateEntityError(str(msg)) from exc

            # FK violation (if schema evolves) → persistence semantics
            elif "foreign key constraint failed" in msg:
                raise ForeignKeyViolationError(str(msg)) from exc

            else:
                raise PersistenceError(str(msg)) from exc

        except sqlite3.Error as exc:
            raise PersistenceError(str(exc)) from exc

    # ------------------------------------------------------------------
    # get(student_id)
    # ------------------------------------------------------------------
    def get(self, student_id: str) -> Student:
        try:
            cursor = self._connection.execute(
                """
                SELECT
                   s.student_id AS student_id,
                   s.name As student_name
                FROM students s
                WHERE s.student_id = ?
                """,
                (student_id,),
            )
            row = cursor.fetchone()
        except sqlite3.Error as exc:
            raise PersistenceError(str(exc)) from exc

        if row is None:
            raise EntityNotFoundError(f"Student not found: {student_id}")

        primitives = student_row_to_primitives(row)

        return Student(
            student_id=primitives["student_id"],
            name=primitives["student_name"],
        )

    # ------------------------------------------------------------------
    # remove(student_id)
    # ------------------------------------------------------------------
    def remove(self, student_id: str) -> None:
        try:
            cursor = self._connection.execute(
                """
                DELETE FROM students
                WHERE student_id = ?
                """,
                (student_id,),
            )
        except sqlite3.Error as exc:
            raise PersistenceError(str(exc)) from exc

        if cursor.rowcount == 0:
            raise EntityNotFoundError(f"Student not found: {student_id}")

    # ------------------------------------------------------------------
    # list_all()
    # ------------------------------------------------------------------

    def list_all(self) -> Iterable[Student]:
        try:
            cursor = self._connection.execute(
                """
                SELECT
                    s.student_id AS student_id,
                    s.name AS student_name
                FROM students s
                ORDER BY s.student_id
                """,
            )
            rows = cursor.fetchall()
        except sqlite3.Error as exc:
            raise PersistenceError(str(exc)) from exc

        for row in rows:
            primitives = student_row_to_primitives(row)
            yield Student(
                student_id=primitives["student_id"],
                name=primitives["student_name"],
            )

