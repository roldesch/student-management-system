# tests/infrastructure/sqlite/conftest.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Literal, Protocol, runtime_checkable

import pytest

from infrastructure.sqlite.bootstrap import initialize_sqlite_database
from infrastructure.sqlite.unit_of_work import UnitOfWork

from infrastructure.sqlite.repositories.sqlite_student_repository import SQLiteStudentRepository
from infrastructure.sqlite.repositories.sqlite_teacher_repository import SQLiteTeacherRepository
from infrastructure.sqlite.repositories.sqlite_course_repository import SQLiteCourseRepository

# -----------------------------------------------------------------------------
# In-memory repositories (contract counterparts)
# -----------------------------------------------------------------------------
from infrastructure.in_memory.in_memory_student_repository import InMemoryStudentRepository
from infrastructure.in_memory.in_memory_teacher_repository import InMemoryTeacherRepository
from infrastructure.in_memory.in_memory_course_repository import InMemoryCourseRepository


# -----------------------------------------------------------------------------
# Structural typing only (no inheritance assumptions)
# -----------------------------------------------------------------------------
@runtime_checkable
class StudentRepositoryLike(Protocol):
    def add(self, student) -> None: ...
    def get(self, student_id: str): ...
    def remove(self, student_id: str) -> None: ...
    def list_all(self) -> Iterable[object]: ...


@runtime_checkable
class TeacherRepositoryLike(Protocol):
    def add(self, teacher) -> None: ...
    def get(self, teacher_id: str): ...
    def remove(self, teacher_id: str) -> None: ...
    def list_all(self) -> Iterable[object]: ...


@runtime_checkable
class CourseRepositoryLike(Protocol):
    def add(self, course) -> None: ...
    def get(self, course_code: str): ...
    def remove(self, course_code: str) -> None: ...
    def list_all(self) -> Iterable[object]: ...

RepositoryKind = Literal["memory", "sqlite"]


# -----------------------------------------------------------------------------
# Scopes (explicit BEGIN / COMMIT / ROLLBACK visibility in tests)
# -----------------------------------------------------------------------------
class RepositoryScope(Protocol):
    students: StudentRepositoryLike
    teachers: TeacherRepositoryLike
    courses: CourseRepositoryLike

    def __enter__(self) -> "RepositoryScope": ...
    def __exit__(self, exc_type, exc, tb) -> None: ...


class _MemoryRepositoryScope:
    """
    Explicit scope for in-memory repositories.

    This is intentionally a no-op context manager, but it enforces the same
    lifecycle shape as SQLite: tests always operate within an explicit scope.
    """

    def __init__(self) -> None:
        self.students = InMemoryStudentRepository()
        self.teachers = InMemoryTeacherRepository()
        self.courses = InMemoryCourseRepository(
            students=self.students,
            teachers=self.teachers,
        )

    def __enter__(self) -> "_MemoryRepositoryScope":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        # Explicitly do not suppress exceptions
        return None


class _SqliteRepositoryScope:
    """
    Explicit scope for SQLite repositories.

    Owns exactly one UnitOfWork, therefore:
    - exactly one connection
    - exactly one transaction per scope
    """

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._uow: UnitOfWork | None = None

        self.students: SQLiteStudentRepository | None = None
        self.teachers: SQLiteTeacherRepository | None = None
        self.courses: SQLiteCourseRepository | None = None

    def __enter__(self) -> "_SqliteRepositoryScope":
        self._uow = UnitOfWork(self._db_path, write=True)
        self._uow.__enter__()

        conn = self._uow.connection
        self.students = SQLiteStudentRepository(conn)
        self.teachers = SQLiteTeacherRepository(conn)
        self.courses = SQLiteCourseRepository(conn)

        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        assert self._uow is not None
        self._uow.__exit__(exc_type, exc, tb)

        # Help catch accidental post-scope use in tests
        self.students = None
        self.teachers = None
        self.courses = None


# -----------------------------------------------------------------------------
# Harness fixture (contract entry point)
# -----------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class RepositoryHarness:
    kind: RepositoryKind
    new_scope: Callable[[], RepositoryScope]

@pytest.fixture(params=["memory", "sqlite"])
def repository_harness(
        request:pytest.FixtureRequest,
        tmp_path: Path,
) -> RepositoryHarness:
    """
    Contract harness used by all SQLite repositories contract tests.

    Rule:
    - Tests MUST acquire repositories only via an explicit scope:
        with repository_harness.new_scope() as scope:
            scope.students.add(...)
    """
    kind: RepositoryKind = request.param # type: ignore[assignment]

    if kind == "memory":
        return RepositoryHarness(
            kind="memory",
            new_scope=lambda : _MemoryRepositoryScope(),
        )

    db_path = tmp_path / "sms_contract_test.sqlite3"
    initialize_sqlite_database(db_path)

    return RepositoryHarness(
        kind="sqlite",
        new_scope=lambda : _SqliteRepositoryScope(db_path),
    )