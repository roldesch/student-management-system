# infrastructure/in_memory/in_memory_teacher_repository.py

from __future__ import annotations
from typing import Dict, Iterable

from domain.models.teacher import Teacher
from domain.repositories.teacher_repository import TeacherRepository
from domain.exceptions.domain_exceptions import (
    DuplicateEntityError,
    EntityNotFoundError
)

class InMemoryTeacherRepository(TeacherRepository):
    """
    In-memory implementation of TeacherRepository.

    Backed by a mapping:
        { teacher_id: Teacher }

    This repository stores teacher aggregates but does not enforce
    domain-level invariants like assignment/unassignment. Those are
    handled through the Course aggregate and application service layer.
    """

    def __init__(self) -> None:
        self._teachers: Dict[str, Teacher] = {}

    def add(self, teacher: Teacher) -> None:
        teacher_id = teacher.id
        if teacher_id in self._teachers:
            raise DuplicateEntityError(f"Teacher '{teacher_id}' already exists.")
        self._teachers[teacher_id] = teacher

    def get(self, teacher_id: str) -> Teacher:
        if teacher_id not in self._teachers:
            raise EntityNotFoundError(f"Teacher '{teacher_id}' not found.")
        return self._teachers[teacher_id]

    def remove(self, teacher_id: str) -> None:
        if teacher_id not in self._teachers:
            raise EntityNotFoundError(f"Teacher '{teacher_id}' not found.")
        del self._teachers[teacher_id]

    def list_all(self) -> Iterable[Teacher]:
        # Return an immutable snapshot to protect internal storage.
        return tuple(self._teachers.values())

    # Test utility - not part of domain interface
    def clear(self) -> None:
        self._teachers.clear()
