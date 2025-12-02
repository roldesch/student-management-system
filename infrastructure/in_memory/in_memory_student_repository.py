# infrastructure/in_memory/in_memory_student_repository.py

from __future__ import annotations
from typing import Dict, Iterable

from domain.models.student import Student
from domain.repositories.student_repository import StudentRepository
from domain.exceptions.domain_exceptions import (
    DuplicateEntityError,
    EntityNotFoundError
)

class InMemoryStudentRepository(StudentRepository):
    """
    In-memory implementation of StudentRepository.

    Backed by a mapping:
        { student_id: Student }

    This repository is intentionally simple: it stores and retrieves
    Student aggregates but does not enforce enrollment/un-enrollment
    invariants. Those are handled through the Course and Student aggregates
    and orchestrated by the application service layer.
    """

    def __init__(self) -> None:
        self._students: Dict[str, Student] = {}

    def add(self, student: Student) -> None:
        student_id = student.id
        if student_id in self._students:
            raise DuplicateEntityError(f"Student '{student_id}' already exists.")
        self._students[student_id] = student

    def get(self, student_id: str) -> Student:
        if student_id not in self._students:
            raise EntityNotFoundError(f"Student '{student_id}' not found.")
        return self._students[student_id]

    def remove(self, student_id: str) -> None:
        if student_id not in self._students:
            raise EntityNotFoundError(f"Student '{student_id}' not found.")
        del self._students[student_id]

    def list_all(self) -> Iterable[Student]:
        # Return an immutable snapshot to avoid exposing internal state.
        return tuple(self._students.values())

    # Test utility - not part of the domain interface.
    def clear(self) -> None:
        self._students.clear()
