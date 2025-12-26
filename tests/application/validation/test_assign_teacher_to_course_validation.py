# tests/application/validation/test_assign_teacher_to_course_validation.py

"""
Application-level validation tests for StudentManagementSystem.assign_teacher_to_course

Scope:
    - Validate identifier shape and semantics (not existence, not relationships)
    - Assert on structured validation errors (field + type)
    - Guarantee validation occurs before any domain interaction

Phase: Relationship Command Validation (Assign Teacher to Course)
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
# teacher_id validation
# ---------------------------------------------------------------------

def test_assign_teacher_missing_teacher_id_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.assign_teacher_to_course(None, "C01")   # type: ignore[arg-type]

    assert exc.value.field == "teacher_id"
    assert exc.value.code == "missing_field"


def test_assign_teacher_non_string_teacher_id_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.assign_teacher_to_course(123, "C01")  # type: ignore[arg-type]

    assert exc.value.field == "teacher_id"
    assert exc.value.code == "invalid_type"


def test_assign_teacher_whitespace_teacher_id_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.assign_teacher_to_course(" ", "C01")

    assert exc.value.field == "teacher_id"
    assert exc.value.code == "invalid_identifier"


# ---------------------------------------------------------------------
# course_code validation
# ---------------------------------------------------------------------

def test_assign_teacher_missing_course_code_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.assign_teacher_to_course("T01", None)    # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "missing_field"


def test_assign_teacher_non_string_course_code_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.assign_teacher_to_course("T01", 123)    # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_type"

def test_assign_teacher_whitespace_course_code_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.assign_teacher_to_course("T01", " ")

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_identifier"


# ---------------------------------------------------------------------
# side-effect guarantees
# ---------------------------------------------------------------------

def test_assign_teacher_validation_failure_has_no_side_effects(sms):
    with pytest.raises(InvalidIdentifierError):
        sms.assign_teacher_to_course(" ", "C01")

    # No repositories should have been mutated
    assert sms.teacher_repo.list_all() == ()
    assert sms.course_repo.list_all() == ()