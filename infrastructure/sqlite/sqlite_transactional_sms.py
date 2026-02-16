# infrastructure/sqlite/sqlite_transactional_sms.py

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from collections.abc import Callable
from typing import TypeVar

from application.services.student_management_system import StudentManagementSystem
from application.responses.student_response import StudentResponse
from application.responses.teacher_response import TeacherResponse
from application.responses.course_response import CourseResponse

from infrastructure.sqlite.bootstrap import initialize_sqlite_database
from infrastructure.sqlite.unit_of_work import UnitOfWork
from infrastructure.sqlite.repositories.sqlite_student_repository import SQLiteStudentRepository
from infrastructure.sqlite.repositories.sqlite_teacher_repository import SQLiteTeacherRepository
from infrastructure.sqlite.repositories.sqlite_course_repository import SQLiteCourseRepository

R = TypeVar("R")


@dataclass(frozen=True, slots=True)
class SqliteTransactionalStudentManagementSystem:
    """
    Infrastructure-owned transactional proxy.

    Implements the same public API as StudentManagementSystem
    without importing the CLI Protocol.

    Guarantees:
    - One UnitOfWork per use-case call
    - Fresh repositories per call
    - Fresh StudentManagementSystem per call
    - Correct transaction mode (read vs write)
    - No state retention
    - No error translation or wrapping

    Architectural Note — Constructor Coupling

    This proxy constructs StudentManagementSystem per use-case call to
    guarantee strict transactional isolation (one UnitOfWork per call).

    This introduces intentional constructor coupling between infrastructure
    and the application service. Any change to the StudentManagementSystem
    must be mirrored here.

    This coupling is inward-only and does not violate dependency direction.

    This trade-off is accepted to preserve:
    - Transaction correctness
    - Repository scoping integrity
    - Absence of cross-call state leakage

    Isolation is prioritized over constructor decoupling.
    """

    sqlite_path: str | Path
    _db_path: Path = field(init=False, repr=False)

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def __post_init__(self) -> None:
        # Normalize path exactly once at construction time.
        # Store strict internal Path invariant in _db_path.
        normalized = Path(self.sqlite_path)
        object.__setattr__(self, "_db_path", normalized)

        # Phase-1 Guarantee:
        # Ensure database schema and required pragmas exist
        # before any UnitOfWork begins.
        initialize_sqlite_database(self._db_path)

    # ---------------------------------------------------------
    # Internal execution wrapper
    # ---------------------------------------------------------

    def _execute_in_transaction(
        self,
        *,
        write: bool,
        fn: Callable[[StudentManagementSystem], R],
    ) -> R:
        with UnitOfWork(self._db_path, write=write) as uow:
            conn = uow.connection

            sms = StudentManagementSystem(
                student_repo=SQLiteStudentRepository(conn),
                teacher_repo=SQLiteTeacherRepository(conn),
                course_repo=SQLiteCourseRepository(conn),
            )

            return fn(sms)

    # ---------------------------------------------------------
    # Student use cases
    # ---------------------------------------------------------

    def add_student(self, student_id: str, name: str) -> StudentResponse:
        return self._execute_in_transaction(
            write=True,
            fn=lambda sms: sms.add_student(student_id, name),
        )

    def get_student(self, student_id: str) -> StudentResponse:
        return self._execute_in_transaction(
            write=False,
            fn=lambda sms: sms.get_student(student_id),
        )

    # ---------------------------------------------------------
    # Teacher use cases
    # ---------------------------------------------------------

    def add_teacher(self, teacher_id: str, name: str) -> TeacherResponse:
        return self._execute_in_transaction(
            write=True,
            fn=lambda sms: sms.add_teacher(teacher_id, name),
        )

    def get_teacher(self, teacher_id: str) -> TeacherResponse:
        return self._execute_in_transaction(
            write=False,
            fn=lambda sms: sms.get_teacher(teacher_id),
        )

    # ---------------------------------------------------------
    # Course use cases
    # ---------------------------------------------------------

    def add_course(self, code: str, name: str) -> CourseResponse:
        return self._execute_in_transaction(
            write=True,
            fn=lambda sms: sms.add_course(code, name),
        )

    def get_course(self, code: str) -> CourseResponse:
        return self._execute_in_transaction(
            write=False,
            fn=lambda sms: sms.get_course(code),
        )

    def enroll_student_in_course(self, student_id: str, course_code: str) -> None:
        return self._execute_in_transaction(
            write=True,
            fn=lambda sms: sms.enroll_student_in_course(student_id, course_code),
        )

