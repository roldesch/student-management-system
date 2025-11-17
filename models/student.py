from exceptions.domain_exceptions import (
    EntityError,
    GradeError,
    EnrollmentError
)

from typing import List, Dict, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from models.course import Course


class Student:
    def __init__(self, student_id: str, name: str):
        self._id = student_id
        self._name = name
        self._courses: List[Course] = []
        self._grades: Dict[Course, float] = {}

    # ----------- Protected internal access (only Course should call these) ----------
    def _add_course(self, course: "Course") -> None:
        if course in self._courses:
            raise EnrollmentError(
                f"Student '{self._id}' is already enrolled in '{course.code}'."
            )

        self._courses.append(course)

    def _remove_course(self, course: "Course") -> None:
        if course not in self._courses:
            raise EnrollmentError(
                f"Student '{self._id}' is not enrolled in '{course.code}'"
            )

        self._courses.remove(course)
        self._grades.pop(course, None)    # remove grade if existed

    # ---------- Grade Management ----------
    def assign_grade(self, course: "Course", value: float) -> None:
        if course not in self._courses:
            raise GradeError(
                f"Cannot assign grade to course '{course.code}'."
                f"Student '{self._id}' is not enrolled."
            )

        if not (0.0 <= value <= 10.0):
            raise GradeError(
                "Grades must be between 0.0 and 10.0 (inclusive)."
            )

        self._grades[course] = value

    def remove_grade(self, course: "Course") -> None:
        if course not in self._grades:
            raise GradeError(
                f"No grade assigned for course '{course.code}'."
            )

        del self._grades[course]

    def get_grade(self, course: "Course") -> Optional[float]:
        return self._grades.get(course)

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
                "Student name cannot be empty."
                )

        self._name = new_name

    @property
    def courses(self) -> Tuple["Course", ...]:
        return tuple(self._courses)

    @property
    def grades(self) -> Dict["Course", float]:
        return dict(self._grades)

