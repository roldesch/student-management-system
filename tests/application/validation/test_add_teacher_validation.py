# tests/application/validation/test_add_teacher_validation.py

"""
Application-level validation tests for StudentManagementSystem.add_teacher

Scope:
    - Validate input shape and semantics (not business rules)
    - Assert on structured validation errors (field + type)
    - Guarantee no side effects on validation failure

Phase: Entity Creation Validation (Teacher)
"""

import pytest

from application.services.student_management_system import StudentManagementSystem
from application.validation.errors import (
    MissingFieldError,
    EmptyValueError,
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

def test_add_teacher_missing_teacher_id_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.add_teacher(None, "Dr. Smith")    # type: ignore[arg-type]

    assert exc.value.field == "teacher_id"
    assert exc.value.code == "missing_field"


def test_add_teacher_non_string_teacher_id_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.add_teacher(123, "Dr. Smith")    # type: ignore[arg-type]

    assert exc.value.field == "teacher_id"
    assert exc.value.code == "invalid_type"


def test_add_teacher_whitespace_teacher_id_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.add_teacher(" ", "Dr. Smith")

    assert exc.value.field == "teacher_id"
    assert exc.value.code == "invalid_identifier"


# ---------------------------------------------------------------------
# name validation
# ---------------------------------------------------------------------

def test_add_teacher_missing_name_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.add_teacher("T01", None)    # type: ignore[arg-type]

    assert exc.value.field == "name"
    assert exc.value.code == "missing_field"


def test_add_teacher_non_string_name_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.add_teacher("T01", 42)    # type: ignore[arg-type]

    assert exc.value.field == "name"
    assert exc.value.code == "invalid_type"


def test_add_teacher_whitespace_name_raises_empty_value_error(sms):
    with pytest.raises(EmptyValueError) as exc:
        sms.add_teacher("T01", " ")

    assert exc.value.field == "name"
    assert exc.value.code == "empty_value"


# ---------------------------------------------------------------------
# side-effect guarantees
# ---------------------------------------------------------------------

def test_add_teacher_validation_failure_has_no_side_effects(sms):
    with pytest.raises(EmptyValueError):
        sms.add_teacher("T01", " ")

    # No teacher should have been persisted
    assert sms.teacher_repo.list_all() == ()
