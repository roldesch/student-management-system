#base_repository.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Iterable

T = TypeVar("T")
K = TypeVar("K")


class BaseRepository(ABC, Generic[T, K]):
    """
    Generic repository interface for domain entities.
    Although primarily intended for aggregate roots, the application layer
    may require repositories for other entities as well.
    """

    @abstractmethod
    def add(self, entity: T) -> None:
        """Persist a new entity. Raises DuplicateEntityError on conflict."""
        raise NotImplementedError

    @abstractmethod
    def get(self, key: K) -> T:
        """Retrieve an entity by its identity key. Raises EntityNotFoundError."""
        raise NotImplementedError

    @abstractmethod
    def remove(self, key: K) -> None:
        """Delete an entity. Must enforce cleanup through aggregate roots."""
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> Iterable[T]:
        """Return a read-only iterable of all stored entities."""
        raise NotImplementedError
