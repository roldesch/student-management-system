import pytest

from core.student_management_system import StudentManagementSystem
from models.student import Student
from models.teacher import Teacher
from models.course import Course


# ----------------------------
# System-level fixture
# ----------------------------
@pytest.fixture
def sms():
    """Fresh StudentManagementSystem for every test."""
    return StudentManagementSystem()


# ----------------------------
# Sample entity factories
# ----------------------------
@pytest.fixture
def student_factory():
    """Returns a function that creates students with incremental IDs."""
    counter = {"i": 0}

    def _create_student(name="Student"):
        counter["i"] += 1
        sid = f"S{counter['i']:02d}"
        return Student(sid, name)

    return _create_student


@pytest.fixture
def teacher_factory():
    """Returns a function that creates teachers with incremental IDs."""
    counter = {"i": 0}

    def _create_teacher(name="Teacher"):
        counter["i"] += 1
        tid = f"T{counter['i']:02d}"
        return Teacher(tid, name)

    return _create_teacher


@pytest.fixture
def course_factory():
    """Returns a function that creates courses with incremental codes."""
    counter = {"i": 0}

    def _create_course(name="Course"):
        counter["i"] += 1
        code = f"C{counter['i']:02d}"
        return Course(code, name)

    return _create_course
