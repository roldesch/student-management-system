# cli/app_factory.py

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from application.services.student_management_system import StudentManagementSystem
from infrastructure.in_memory.in_memory_student_repository import InMemoryStudentRepository
from infrastructure.in_memory.in_memory_teacher_repository import InMemoryTeacherRepository
from infrastructure.in_memory.in_memory_course_repository import InMemoryCourseRepository

@dataclass(frozen=True, slots=True)
class PersistenceConfig:
    """
    Persistence selection configuration.

    This config is owned by the composition root and must not cross.
    into application or infrastructure layers.

    It answers one question only: which persistence backend is selected?
    """
    backend: Literal["memory", "sqlite"] = "memory"
    sqlite_path: Path | None = None


def _build_in_memory_sms() -> StudentManagementSystem:
    """
    Build the canonical in-memory StudentManagementSystem.

    This functions preserves the pre-Phase-5 object graph exactly and
    must remain behaviorally identical across Phase-5.
    """
    student_repo = InMemoryStudentRepository()
    teacher_repo = InMemoryTeacherRepository()
    course_repo = InMemoryCourseRepository()

    return StudentManagementSystem(
        student_repo=student_repo,
        teacher_repo=teacher_repo,
        course_repo=course_repo,
    )

def create_sms() -> StudentManagementSystem:
    """
    CLI composition root.

    Returns the canonical in-memory StudentManagementSystem.
    """
    return _build_in_memory_sms()

