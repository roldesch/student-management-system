#course_repository.py

from abc import abstractmethod
from typing import Iterable

from domain.repositories.base_repository import BaseRepository
from domain.models.course import Course


class CourseRepository(BaseRepository[Course, str]):
    """
    Repository interface for Course entities.

    Course is the aggregate root in this domain: it governs enrollment rules,
    teacher assignment invariants, and relationship integrity across students
    and teachers. Therefore, this repository is the primary gateway through
    which the application layer retrieves and persists course aggregates.
    """

    @abstractmethod
    def add(self, course: Course) -> None:
        """Persist a new Course."""
        raise NotImplementedError

    @abstractmethod
    def get(self, course_code: str) -> Course:
        """Retrieve a Course by its code."""
        raise NotImplementedError

    @abstractmethod
    def remove(self, course_code: str) -> None:
        """Remove a Course by its code."""
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> Iterable[Course]:
        """Return all Courses as a read-only iterable."""
        raise NotImplementedError