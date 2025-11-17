from exceptions.domain_exceptions import TeacherAssignmentError, EntityError

from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from models.course import Course

class Teacher:
    def __init__(self, teacher_id: str, name: str):
        self._id = teacher_id
        self._name = name
        self._courses: List["Course"] = []

    # ---------- Protected internal access (only Course should call these) ----------
    def _add_course(self, course: "Course") -> None:
        if course in self._courses:
            raise TeacherAssignmentError(
                f"Teacher '{self._id}' is already assigned to '{course.code}'"
            )

        self._courses.append(course)

    def _remove_course(self, course: "Course") -> None:
        if course not in self._courses:
            raise TeacherAssignmentError(
                f"Teacher '{self._id}' is not assigned to '{course.code}'"
            )

        self._courses.remove(course)

    # ---------- Public properties (queries only) ----------
    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        if not new_name.strip():
            raise EntityError(
                "Teacher name cannot be empty."
            )

        self._name = new_name

    @property
    def courses(self) -> Tuple[Course, ...]:
        return tuple(self._courses)

