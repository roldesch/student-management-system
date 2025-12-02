# infrastructure/in_memory/in_memory_course_repository.py

from __future__ import annotations
from typing import Dict, Iterable

from domain.models.course import Course
from domain.repositories.course_repository import CourseRepository
from domain.exceptions.domain_exceptions import (
    DuplicateEntityError,
    EntityNotFoundError
)


class InMemoryCourseRepository(CourseRepository):
    """
    In-memory implementation of CourseRepository.

    Backed by a simple mapping:
        { course_code: Course }

    This repository does NOT enforce relationship rules (e.g. dropping
    students, unassigning teachers). That is the responsibility of the
    Course aggregate and the application service layer orchestrating them.
    """

    def __init__(self) -> None:
        self._courses: Dict[str, Course] = {}

    def add(self, course: Course) -> None:
        code = course.code
        if code in self._courses:
            raise DuplicateEntityError(f"Course '{code}' already exists.")
        self._courses[code] = course

    def get(self, course_code: str) -> Course:
        if course_code not in self._courses:
            raise EntityNotFoundError(f"Course '{course_code}' not found.")
        return self._courses[course_code]

    def remove(self, course_code: str) -> None:
        if course_code not in self._courses:
            raise EntityNotFoundError(f"Course '{course_code}' not found.")
        del self._courses[course_code]

    def list_all(self) -> Iterable[Course]:
        # Return a tuple to prevent external mutation of internal state
        return tuple(self._courses.values())

    # Test utility - not part of domain interface
    def clear(self) -> None:
        self._courses.clear()
