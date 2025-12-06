#tests/conftest.py
import pytest

from application.services.student_management_system import StudentManagementSystem

from infrastructure.in_memory.in_memory_student_repository import InMemoryStudentRepository
from infrastructure.in_memory.in_memory_teacher_repository import InMemoryTeacherRepository
from infrastructure.in_memory.in_memory_course_repository import InMemoryCourseRepository

from domain.models.student import Student
from domain.models.teacher import Teacher
from domain.models.course import Course


# ----------------------------
# System-level fixture
# ----------------------------
@pytest.fixture
def sms():
    """
    Fresh StudentManagementSystem for every test.

    This is the correct way to initialize the SMS after refactoring:
    using dependency-injected repository implementations.
    """
    return StudentManagementSystem(
        student_repo=InMemoryStudentRepository(),
        teacher_repo=InMemoryTeacherRepository(),
        course_repo=InMemoryCourseRepository(),
    )

# ----------------------------
# Sample entity factories
# ----------------------------
@pytest.fixture
def make_student():
    """Returns a function that creates students with incremental IDs."""
    counter = {"i": 0}

    def _create_student(name="Student"):
        counter["i"] += 1
        sid = f"S{counter['i']:02d}"
        return Student(sid, name)

    return _create_student

@pytest.fixture
def make_teacher():
    """Returns a function that creates teachers with incremental IDs."""
    counter = {"i": 0}

    def _create_teacher(name="Teacher"):
        counter["i"] += 1
        tid = f"T{counter['i']:02d}"
        return Teacher(tid, name)

    return _create_teacher

@pytest.fixture
def make_course():
    """Returns a function that creates courses with incremental codes."""
    counter = {"i": 0}

    def _create_course(name="Course"):
        counter["i"] += 1
        code = f"C{counter['i']:02d}"
        return Course(code, name)

    return _create_course



