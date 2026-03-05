# infrastructure/in_memory/in_memory_store.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple


@dataclass(frozen=True, slots=True)
class StudentSnapshot:
    student_id: str
    name: str


@dataclass(frozen=True, slots=True)
class TeacherSnapshot:
    teacher_id: str
    name: str


@dataclass(frozen=True, slots=True)
class EnrollmentSnapshot:
    student_id: str
    grade: Optional[float]


@dataclass(frozen=True, slots=True)
class CourseSnapshot:
    code: str
    name: str
    assigned_teacher_id: Optional[str]
    enrollments: Tuple[EnrollmentSnapshot, ...]


class InMemoryStore:
    """
    Shared persistence-shaped store for in-memory repositories.

    Repositories store snapshots (primitives/ids) and reconstruct fresh instances on read.
    This enforces detached semantics and matches the SQLite backend's reconstruction shape.
    """

    def __init__(self) -> None:
        self.students: Dict[str, StudentSnapshot] = {}
        self.teachers: Dict[str, TeacherSnapshot] = {}
        self.courses: Dict[str, CourseSnapshot] = {}