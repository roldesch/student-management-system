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