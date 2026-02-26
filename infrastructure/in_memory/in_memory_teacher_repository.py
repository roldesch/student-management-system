# infrastructure/in_memory/in_memory_teacher_repository.py

from __future__ import annotations
from typing import Iterable

from domain.models.teacher import Teacher
from domain.repositories.teacher_repository import TeacherRepository
from domain.exceptions.domain_exceptions import (
    DuplicateEntityError,
    EntityNotFoundError,
)

from infrastructure.in_memory.in_memory_store import (
    InMemoryStore,
    TeacherSnapshot,
)


class InMemoryTeacherRepository(TeacherRepository):
    """
    In-memory implementation of TeacherRepository with detached semantics.

    Parity with SQLite TeacherRepository.get():
      - Reconstructs Teacher primitives only (id, name)
      - Does NOT reconstruct relationships (courses)
    """


    def __init__(self, store: InMemoryStore) -> None:
        self._store = store


    def add(self, teacher: Teacher) -> None:
        teacher_id = teacher.id

        if teacher_id in self._store.teachers:
            raise DuplicateEntityError(f"Teacher '{teacher_id}' already exists.")
        self._store.teachers[teacher_id] = self._to_snapshot(teacher)


    def get(self, teacher_id: str) -> Teacher:
        snap = self._store.teachers.get(teacher_id)

        if snap is None:
            raise EntityNotFoundError(f"Teacher '{teacher_id}' not found.")
        return self._from_snapshot(snap)


    def remove(self, teacher_id: str) -> None:
        if teacher_id not in self._store.teachers:
            raise EntityNotFoundError(f"Teacher '{teacher_id}' not found.")
        del self._store.teachers[teacher_id]


    def list_all(self) -> Iterable[Teacher]:
        return tuple(self._from_snapshot(s) for s in self._store.teachers.values())


    def update(self, teacher: Teacher) -> None:
        teacher_id = teacher.id

        if teacher_id not in self._store.teachers:
            raise EntityNotFoundError(f"Teacher '{teacher_id}' not found.")
        self._store.teachers[teacher_id] = self._to_snapshot(teacher)


    # Test utility - not part of domain interface
    def clear(self) -> None:
        self._store.teachers.clear()


    @staticmethod
    def _to_snapshot(teacher: Teacher) -> TeacherSnapshot:
        return TeacherSnapshot(
            teacher_id=teacher.id,
            name=teacher.name,
        )


    @staticmethod
    def _from_snapshot(snap: TeacherSnapshot) -> Teacher:
        # SQLite parity: reconstruction only - no relationships
        return Teacher(
            teacher_id=snap.teacher_id,
            name=snap.name,
        )