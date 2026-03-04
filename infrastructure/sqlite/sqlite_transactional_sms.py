# infrastructure/sqlite/sqlite_transactional_sms.py

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from collections.abc import Callable
from typing import TypeVar, ClassVar

from application.services.student_management_system import StudentManagementSystem
from application.responses.student_response import StudentResponse
from application.responses.teacher_response import TeacherResponse
from application.responses.course_response import CourseResponse

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
    # Write method classification
    # ---------------------------------------------------------
    # Authoritative classification of mutating operations.
    # Any new command method added to StudentManagementSystem
    # must be explicitly listed here.

    _WRITE_METHODS: ClassVar[frozenset[str]] = frozenset({
        "add_student",
        "add_teacher",
        "add_course",
        "remove_student",
        "remove_teacher",
        "remove_course",
        "assign_teacher_to_course",
        "unassign_teacher_from_course",
        "enroll_student_in_course",
        "drop_student_from_course",
        "assign_grade_to_student",
        "remove_grade_from_student",
    })


    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def __post_init__(self) -> None:
        # Normalize path exactly once at construction time.
        # Store strict internal Path invariant in _db_path.
        normalized = Path(self.sqlite_path).expanduser().resolve()
        object.__setattr__(self, "_db_path", normalized)

        # NOTE (ADR-007):
        # Bootstrap ownership belongs exclusively to the composition root.
        # This transactional proxy must not initialize schema.

    # ---------------------------------------------------------
    # Transaction execution
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

    def _wrap(
        self,
        operation: str,
        fn: Callable[[StudentManagementSystem], R],
    ) -> R:
        """
        Delegate execution to StudentManagementSystem within a transaction.

        Transaction mode (read vs write) is determined exclusively
        by membership in _WRITE_METHODS.

        This method is the single decision point for transaction mode.
        """

        write = operation in self._WRITE_METHODS

        return self._execute_in_transaction(
            write=write,
            fn=fn,
        )

    # ---------------------------------------------------------
    # Student use cases
    # ---------------------------------------------------------

    def add_student(self, student_id: str, name: str) -> StudentResponse:
        return self._wrap(
            "add_student",
            lambda sms: sms.add_student(student_id, name),
        )

    def get_student(self, student_id: str) -> StudentResponse:
        return self._wrap(
            "get_student",
            lambda sms: sms.get_student(student_id),
        )

    def list_students(self) -> list[StudentResponse]:
        return self._wrap(
            "list_students",
            lambda sms: sms.list_students(),
        )

    def remove_student(self, student_id: str) -> None:
        return self._wrap(
            "remove_student",
            lambda sms: sms.remove_student(student_id),
        )

    def assign_grade_to_student(
            self,
            student_id: str,
            course_code: str,
            value: float,
    ) -> None:
        return self._wrap(
            "assign_grade_to_student",
            lambda sms: sms.assign_grade_to_student(student_id, course_code, value),
        )

    def remove_grade_from_student(
            self,
            student_id: str,
            course_code: str,
    ) -> None:
        return self._wrap(
            "remove_grade_from_student",
            lambda sms: sms.remove_grade_from_student(student_id, course_code),
        )

    def get_student_grade(
            self,
            student_id: str,
            course_code: str,
    ) -> float | None:
        return self._wrap(
            "get_student_grade",
            lambda sms: sms.get_student_grade(student_id, course_code),
        )


    # ---------------------------------------------------------
    # Teacher use cases
    # ---------------------------------------------------------

    def add_teacher(self, teacher_id: str, name: str) -> TeacherResponse:
        return self._wrap(
            "add_teacher",
            lambda sms: sms.add_teacher(teacher_id, name),
        )

    def get_teacher(self, teacher_id: str) -> TeacherResponse:
        return self._wrap(
            "get_teacher",
            lambda sms: sms.get_teacher(teacher_id),
        )

    def list_teachers(self) -> list[TeacherResponse]:
        return self._wrap(
            "list_teachers",
            lambda sms: sms.list_teachers(),
        )

    def remove_teacher(self, teacher_id: str) -> None:
        return self._wrap(
            "remove_teacher",
            lambda sms: sms.remove_teacher(teacher_id),
        )

    def assign_teacher_to_course(
            self,
            teacher_id: str,
            course_code: str,
    ) -> None:
        return self._wrap(
            "assign_teacher_to_course",
            lambda sms: sms.assign_teacher_to_course(teacher_id, course_code),
        )

    def unassign_teacher_from_course(self, course_code: str) -> None:
        return self._wrap(
            "unassign_teacher_from_course",
            lambda sms: sms.unassign_teacher_from_course(course_code),
        )

    # ---------------------------------------------------------
    # Course use cases
    # ---------------------------------------------------------

    def add_course(self, course_code: str, name: str) -> CourseResponse:
        return self._wrap(
            "add_course",
            lambda sms: sms.add_course(course_code, name),
        )

    def get_course(self, code: str) -> CourseResponse:
        return self._wrap(
            "get_course",
            lambda sms: sms.get_course(code),
        )

    def list_courses(self) -> list[CourseResponse]:
        return self._wrap(
            "list_courses",
            lambda sms: sms.list_courses(),
        )

    def remove_course(self, course_code: str) -> None:
        return self._wrap(
            "remove_course",
            lambda sms: sms.remove_course(course_code),
        )

    def enroll_student_in_course(self, student_id: str, course_code: str) -> None:
        return self._wrap(
            "enroll_student_in_course",
            lambda sms: sms.enroll_student_in_course(student_id, course_code),
        )

    def drop_student_from_course(
            self,
            student_id: str,
            course_code: str,
    ) -> None:
        return self._wrap(
            "drop_student_from_course",
            lambda sms: sms.drop_student_from_course(student_id, course_code),
        )

