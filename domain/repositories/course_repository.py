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

    @abstractmethod
    def update(self, course: Course) -> None:
        """
        Persist an existing Course aggregate.

    Aggregate persistence contract (aggregate root semantics):

    - The course identity MUST already exist in the repository.
    - If the identity does not exist, MUST raise EntityNotFoundError.
    - MUST NOT perform upsert (no silent insert).
    - MUST be idempotent when invoked with identical aggregate state.
    - MUST persist the FULL aggregate state owned by Course, including:
        - Intrinsic attributes (code, name)
        - Teacher assignment (teacher_id)
        - Student enrollments
        - Enrollment-associated grades
    - MUST NOT persist state owned by other aggregates.
    - MUST NOT enforce business rules or invariants.
    - MUST assume it is executed inside an active UnitOfWork transaction.
      Transaction boundaries are not owned by the repository.

    Course is the aggregate root in this domain.
    The repository is responsible for atomic persistence of the aggregate
    state as defined by the UnitOfWork boundary.
        """
        raise NotImplementedError
