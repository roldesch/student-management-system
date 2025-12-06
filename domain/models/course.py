# domain/models/course.py
from domain.exceptions.domain_exceptions import (
    EnrollmentError,
    TeacherAssignmentError,
)

from typing import Optional, List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.models.student import Student
    from domain.models.teacher import Teacher


class Course:
    def __init__(self, code: str, name: str):
        self._code = code
        self._name = name
        self._students: List[Student] = []
        self._teacher: Optional[Teacher] = None

    # --------- Teacher Management ----------
    def assign_teacher(self, teacher: "Teacher") -> None:
        if self._teacher is not None:
            raise TeacherAssignmentError(
                f"Course '{self._code}' already has a teacher assigned."
            )

        self._teacher = teacher
        teacher._add_course(self)    # protected internal mutation

    def unassign_teacher(self) -> None:
        if self._teacher is None:
            raise TeacherAssignmentError(
                f"Course '{self._code}' has no teacher to unassign."
            )

        teacher = self._teacher
        self._teacher = None
        teacher._remove_course(self)    # protected internal mutation

    # ---------- Student Enrollment -----------
    def enroll(self, student: "Student") -> None:
        if student in self._students:
            raise EnrollmentError(
                f"Student '{student.id}' is already enrolled in '{self.code}'."
            )

        self._students.append(student)
        student._add_course(self)    # protected internal mutation

    def drop(self, student: "Student") -> None:
        if student not in self._students:
            raise EnrollmentError(
                f"Student '{student.id}' is not enrolled in '{self._code}'."
            )

        self._students.remove(student)
        student._remove_course(self)    # protected internal mutation

    # ---------- Read-only properties ----------
    @property
    def code(self) -> str:
        return self._code

    @property
    def name(self) -> str:
        return self._name

    @property
    def teacher(self) -> Optional["Teacher"]:
        return self._teacher

    @property
    def students(self) -> Tuple["Student", ...]:
        return tuple(self._students)

