# cli/app_factory.py

from application.services.student_management_system import StudentManagementSystem
from infrastructure.in_memory.in_memory_student_repository import InMemoryStudentRepository
from infrastructure.in_memory.in_memory_teacher_repository import InMemoryTeacherRepository
from infrastructure.in_memory.in_memory_course_repository import InMemoryCourseRepository


def create_sms() -> StudentManagementSystem:
    """
    CLI composition root.

    Wires repositories to the application service.
    """
    student_repo = InMemoryStudentRepository()
    teacher_repo = InMemoryTeacherRepository()
    course_repo = InMemoryCourseRepository()

    return StudentManagementSystem(
        student_repo=student_repo,
        teacher_repo=teacher_repo,
        course_repo=course_repo,
    )
