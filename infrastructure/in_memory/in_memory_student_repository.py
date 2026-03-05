# infrastructure/in_memory/in_memory_student_repository.py

from __future__ import annotations
from typing import Iterable

from domain.models.student import Student
from domain.repositories.student_repository import StudentRepository
from domain.exceptions.domain_exceptions import (
    DuplicateEntityError,
    EntityNotFoundError,
)

from infrastructure.in_memory.in_memory_store import (
    InMemoryStore,
    StudentSnapshot,
)


class InMemoryStudentRepository(StudentRepository):
    """
    In-memory implementation of StudentRepository with detached semantics.

    Parity with SQLite StudentRepository.get():
      - Reconstructs Student primitives only (id, name)
      - Does NOT reconstruct relationships (courses, grades)
    """

    def __init__(self, store: InMemoryStore) -> None:
        self._store = store


    def add(self, student: Student) -> None:
        student_id = student.id

        if student_id in self._store.students:
            raise DuplicateEntityError(f"Student '{student_id}' already exists.")
        self._store.students[student_id] = self._to_snapshot(student)


    def get(self, student_id: str) -> Student:
        snap = self._store.students.get(student_id)

        if snap is None:
            raise EntityNotFoundError(f"Student '{student_id}' not found.")
        return self._from_snapshot(snap)


    def remove(self, student_id: str) -> None:
        if student_id not in self._store.students:
            raise EntityNotFoundError(f"Student '{student_id}' not found.")
        del self._store.students[student_id]


    def list_all(self) -> Iterable[Student]:
        return tuple(self._from_snapshot(s) for s in self._store.students.values())


    def update(self, student: Student) -> None:
        student_id = student.id

        if student_id not in self._store.students:
            raise EntityNotFoundError(f"Student '{student_id}' not found.")
        self._store.students[student_id] = self._to_snapshot(student)


    # Test utility - not part of the domain interface.
    def clear(self) -> None:
        self._store.students.clear()


    @staticmethod
    def _to_snapshot(student: Student) -> StudentSnapshot:
        return StudentSnapshot(
            student_id=student.id,
            name=student.name,
        )

    @staticmethod
    def _from_snapshot(snap: StudentSnapshot) -> Student:
        # SQLite parity: reconstruction only - no relationships
        return Student(
            student_id=snap.student_id,
            name=snap.name,
        )

