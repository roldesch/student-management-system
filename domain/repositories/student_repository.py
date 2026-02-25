#student_repository.py

from abc import abstractmethod
from typing import Iterable

from domain.repositories.base_repository import BaseRepository
from domain.models.student import Student


class StudentRepository(BaseRepository[Student, str]):
    """
    Repository interface for Student entities.

    Even though Student is not an aggregate root in the strict DDD sense
    (Course controls relationship invariants), the application layer still
    requires independent lookup of Student objects. Therefore, the domain
    declares a repository to express this need, while deferring storage
    mechanics to the infrastructure layer.
    """

    @abstractmethod
    def add(self, student: Student) -> None:
        """Persist a new Student."""
        raise NotImplementedError

    @abstractmethod
    def get(self, student_id: str) -> Student:
        """Retrieve a Student by ID."""
        raise NotImplementedError

    @abstractmethod
    def remove(self, student_id: str) -> None:
        """Remove a Student by ID."""
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> Iterable[Student]:
        """Return all Students as a read-only iterable."""
        raise NotImplementedError

    @abstractmethod
    def update(self, student: Student) -> None:
        """
        Persist an existing Student entity.

    Non-aggregate persistence contract:

    - The student identity MUST already exist in the repository.
    - If the identity does not exist, MUST raise EntityNotFoundError.
    - MUST NOT perform upsert (no silent insert).
    - MUST be idempotent when invoked with identical entity state.
    - MUST persist only intrinsic attributes owned by Student.
    - MUST NOT modify cross-aggregate relationships
      (e.g., enrollments, grades, or course assignment).
    - MUST NOT enforce business rules or invariants.
    - MUST assume it is executed inside an active UnitOfWork transaction.

    Student is NOT an aggregate root.
    Relationship integrity and enrollment rules are governed by Course.
        """
        raise NotImplementedError
