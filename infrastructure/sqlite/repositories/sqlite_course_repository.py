# infrastructure/sqlite/repositories/sqlite_course_repository.py

from __future__ import annotations

import sqlite3
from typing import Iterable

from domain.models.course import Course
from domain.repositories.course_repository import CourseRepository


class SQLiteCourseRepository(CourseRepository):
    """
    SQLite Course Repository — Phase 3

    This repository is governed by an authoritative SQL contract:
        SQLite Course Repository — SQL Contract (Phase 3)

    Rules (binding):
    - Interacts only with the tables defined in the contract
    - Executes ONLY the SQL statements defined in the contract
    - Aggregate reconstruction uses domain methods only
    - No validation, no business logic, no workflow orchestration
    - Persistence errors only (no domain or validation logic)

    Any deviation requires explicit architectural review.
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add(self, course: Course) -> None:
        raise NotImplementedError

    def get(self, course_code: str) -> Course:
        raise NotImplementedError

    def remove(self, course_code: str) -> None:
        raise NotImplementedError

    def list_all(self) -> Iterable[Course]:
        raise NotImplementedError
