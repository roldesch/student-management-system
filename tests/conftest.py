import pytest

from core.student_management_system import StudentManagementSystem
from models.student import Student
from models.teacher import Teacher
from models.course import Course

@pytest.fixture
def sms():
    return StudentManagementSystem()

@pytest.fixture
def make_student():
    def _make_student(student_id="S01", name="Alice"):
        return Student(student_id, name)
    return _make_student

@pytest.fixture
def make_teacher():
    def _make_teacher(teacher_id="T01", name="Dr. Smith"):
        return Teacher(teacher_id, name)
    return _make_teacher

@pytest.fixture
def make_course():
    def _make_course(code="CS101", name="Intro to Computer Science"):
        return Course(code, name)
    return _make_course

@pytest.fixture
def student_factory():
    """Returns a function that creates students with incremental IDs."""
    counter = {"i": 0}

    def _create_student(name="Student"):
        counter["i"] += 1
        sid = f"S{counter['i']:02d}"
        return Student(sid, name)

    return _create_student

