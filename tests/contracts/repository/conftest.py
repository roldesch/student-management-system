# tests/infrastructure/sqlite/conftest.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Literal, Protocol, runtime_checkable

import pytest

# -------------------------------------------------------------------------
# Domain entities (contract return types)
# -------------------------------------------------------------------------
from domain.models.student import Student
from domain.models.teacher import Teacher
from domain.models.course import Course

# -------------------------------------------------------------------------
# SQLite infrastructure wiring
# -------------------------------------------------------------------------
from infrastructure.sqlite.bootstrap import initialize_sqlite_database
from infrastructure.sqlite.unit_of_work import UnitOfWork

from infrastructure.sqlite.repositories.sqlite_student_repository import SQLiteStudentRepository
from infrastructure.sqlite.repositories.sqlite_teacher_repository import SQLiteTeacherRepository
from infrastructure.sqlite.repositories.sqlite_course_repository import SQLiteCourseRepository

# -----------------------------------------------------------------------------
# In-memory infrastructure wiring
# -----------------------------------------------------------------------------
from infrastructure.in_memory.in_memory_student_repository import InMemoryStudentRepository
from infrastructure.in_memory.in_memory_teacher_repository import InMemoryTeacherRepository
from infrastructure.in_memory.in_memory_course_repository import InMemoryCourseRepository


# -----------------------------------------------------------------------------
# Structural repository contracts (STRICT — domain return types enforced)
# -----------------------------------------------------------------------------
@runtime_checkable
class StudentRepositoryLike(Protocol):
    def add(self, student: Student) -> None: ...
    def get(self, student_id: str) -> Student: ...
    def remove(self, student_id: str) -> None: ...
    def list_all(self) -> Iterable[Student]: ...


@runtime_checkable
class TeacherRepositoryLike(Protocol):
    def add(self, teacher: Teacher) -> None: ...
    def get(self, teacher_id: str) -> Teacher: ...
    def remove(self, teacher_id: str) -> None: ...
    def list_all(self) -> Iterable[Teacher]: ...


@runtime_checkable
class CourseRepositoryLike(Protocol):
    def add(self, course: Course) -> None: ...
    def get(self, course_code: str) -> Course: ...
    def remove(self, course_code: str) -> None: ...
    def list_all(self) -> Iterable[Course]: ...

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


# -------------------------------------------------------------------------
# In-memory scope (no-op lifecycle, same shape as SQLite)
# -------------------------------------------------------------------------

class _MemoryRepositoryScope:
    """
    Explicit scope for in-memory repositories.

    This intentionally mirrors SQLite lifecycle shape,
    even though memory has no real transaction boundary.
    """

    def __init__(
            self,
            *,
            students:InMemoryStudentRepository,
            teachers: InMemoryTeacherRepository,
            courses: InMemoryCourseRepository,
    ) -> None:
        self.students = students
        self.teachers = teachers
        self.courses = courses

    def __enter__(self) -> "RepositoryScope":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        # Explicitly do not suppress exceptions
        return None


# -------------------------------------------------------------------------
# SQLite scope (exactly one UnitOfWork per scope)
# -------------------------------------------------------------------------

class _SqliteRepositoryScope:
    """
    Explicit scope for SQLite repositories.

    Guarantees:
    - Exactly one UnitOfWork
    - Exactly one connection
    - Exactly one transaction per scope
    """

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._uow: UnitOfWork | None = None

        self.students: StudentRepositoryLike | None = None
        self.teachers: TeacherRepositoryLike | None = None
        self.courses: CourseRepositoryLike | None = None

    def __enter__(self) -> "RepositoryScope":
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
# Contract Harness Fixture
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
    Dual-backend repository contract harness.

    Rules:
    - Tests MUST obtain repositories only via:
        with repository_harness.new_scope() as scope:
            scope.students.add(...)
    - No direct instantiation in tests.
    - No backend branching in test bodies.
    """
    kind: RepositoryKind = request.param # type: ignore[assignment]

    if kind == "memory":
        students = InMemoryStudentRepository()
        teachers = InMemoryTeacherRepository()
        courses = InMemoryCourseRepository()

        return RepositoryHarness(
            kind="memory",
            new_scope=lambda : _MemoryRepositoryScope(
                students=students,
                teachers=teachers,
                courses=courses
            ),
        )

    # SQLite branch
    db_path = tmp_path / "sms_contract_test.sqlite3"
    initialize_sqlite_database(db_path)

    return RepositoryHarness(
        kind="sqlite",
        new_scope=lambda : _SqliteRepositoryScope(db_path),
    )