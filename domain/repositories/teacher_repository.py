#teacher_repository.py

from abc import abstractmethod
from typing import Iterable

from domain.repositories.base_repository import BaseRepository
from domain.models.teacher import Teacher


class TeacherRepository(BaseRepository[Teacher, str]):
    """
    Repository interface for Teacher entities.

    Teacher are not aggregate roots in the strict DDD sense since Courses
    govern assignment invariants. However, the application layer must be able
    to retrieve teachers independently (e.g., assign_teacher_to_course),
    therefore the domain declares this repository to express that need while
    deferring storage concerns to infrastructure implementations.
    """

    @abstractmethod
    def add(self, teacher: Teacher) -> None:
        """Persist a new Teacher."""
        raise NotImplementedError

    @abstractmethod
    def get(self, teacher_id: str) -> Teacher:
        """Retrieve a Teacher by ID."""
        raise NotImplementedError

    @abstractmethod
    def remove(self, teacher_id: str) -> None:
        """Remove a Teacher by ID."""
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> Iterable[Teacher]:
        """Returns all Teachers as a read-only iterable."""
        raise NotImplementedError

    @abstractmethod
    def update(self, teacher: Teacher) -> None:
        """
            Persist an existing Teacher entity.

    Non-aggregate persistence contract:

    - The teacher identity MUST already exist in the repository.
    - If the identity does not exist, MUST raise EntityNotFoundError.
    - MUST NOT perform upsert (no silent insert).
    - MUST be idempotent when invoked with identical entity state.
    - MUST persist only intrinsic attributes owned by Teacher.
    - MUST NOT modify cross-aggregate relationships
      (e.g., course assignments or enrollments).
    - MUST NOT enforce business rules or invariants.
    - MUST assume it is executed inside an active UnitOfWork transaction.

    Teacher is NOT an aggregate root.
    Assignment invariants are governed by Course.
        """
        raise NotImplementedError