# tests/application/validation/test_remove_grade_from_student_validation.py

"""
Application-level validation tests for StudentManagementSystem.remove_grade_from_student

Scope:
    - Validate identifier shape and semantics (not existence, not relationships)
    - Assert on structured validation errors (field + type)
    - Guarantee validation occurs before any domain interaction

Phase: Grade Validation (Remove grade from student)
"""

import pytest

from application.services.student_management_system import StudentManagementSystem
from application.validation.errors import (
    MissingFieldError,
    InvalidTypeError,
    InvalidIdentifierError,
)

from infrastructure.in_memory.in_memory_student_repository import (
    InMemoryStudentRepository,
)
from infrastructure.in_memory.in_memory_teacher_repository import (
    InMemoryTeacherRepository,
)
from infrastructure.in_memory.in_memory_course_repository import (
    InMemoryCourseRepository,
)


# ---------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------

@pytest.fixture
def sms() -> StudentManagementSystem:
    """Fresh SMS instance with empty in-memory repositories."""
    return StudentManagementSystem(
        student_repo=InMemoryStudentRepository(),
        teacher_repo=InMemoryTeacherRepository(),
        course_repo=InMemoryCourseRepository(),
    )


# ---------------------------------------------------------------------
# student_id validation
# ---------------------------------------------------------------------

def test_remove_grade_missing_student_id_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.remove_grade_from_student(None, "C01")    # type: ignore[arg-type]

    assert exc.value.field == "student_id"
    assert exc.value.code == "missing_field"


def test_remove_grade_non_string_student_id_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.remove_grade_from_student(123, "C01")    # type: ignore[arg-type]

    assert exc.value.field == "student_id"
    assert exc.value.code == "invalid_type"


def test_remove_grade_whitespace_student_id_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.remove_grade_from_student(" ", "C01")

    assert exc.value.field == "student_id"
    assert exc.value.code == "invalid_identifier"


# ---------------------------------------------------------------------
# course_code validation
# ---------------------------------------------------------------------

def test_remove_grade_missing_course_code_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.remove_grade_from_student("S01", None)    # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "missing_field"


def test_remove_grade_non_string_course_code_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.remove_grade_from_student("S01", 123)  # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_type"


def test_remove_grade_whitespace_course_code_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.remove_grade_from_student("S01", " ")  # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_identifier"


# ---------------------------------------------------------------------
# side-effect guarantees
# ---------------------------------------------------------------------

def test_remove_grade_validation_failure_has_no_side_effects(sms):
    with pytest.raises(MissingFieldError):
        sms.remove_grade_from_student("S01", None)

    assert sms.student_repo.list_all() == ()
    assert sms.course_repo.list_all() == ()