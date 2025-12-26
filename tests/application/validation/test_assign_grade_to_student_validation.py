# tests/application/validation/test_assign_grade_to_student_validation.py

"""
Application-level validation tests for StudentManagementSystem.assign_grade_to_student

Scope:
    - Validate identifier shape and semantics (not existence, not relationships)
    - Validate grade value semantic correctness (type + finiteness)
    - Assert on structured validation errors (field + type)
    - Guarantee validation occurs before any domain interaction

Phase: Grade Validation (Assign Grade to Student)
"""

import math
import pytest

from application.services.student_management_system import StudentManagementSystem
from application.validation.errors import (
    MissingFieldError,
    InvalidTypeError,
    InvalidIdentifierError,
    InvalidValueError,
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

def test_assign_grade_missing_student_id_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.assign_grade_to_student(None, "C01", 9.0)    # type: ignore[arg-type]

    assert exc.value.field == "student_id"
    assert exc.value.code == "missing_field"


def test_assign_grade_non_string_student_id_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.assign_grade_to_student(123, "C01", 9.0)    # type: ignore[arg-type]

    assert exc.value.field == "student_id"
    assert exc.value.code == "invalid_type"


def test_assign_grade_whitespace_student_id_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.assign_grade_to_student(" ", "C01", 9.0)

    assert exc.value.field == "student_id"
    assert exc.value.code == "invalid_identifier"


# ---------------------------------------------------------------------
# course_code validation
# ---------------------------------------------------------------------

def test_assign_grade_missing_course_code_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.assign_grade_to_student("S01", None, 9.0)    # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "missing_field"


def test_assign_grade_non_string_course_code_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.assign_grade_to_student("S01", 123, 9.0)  # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_type"


def test_assign_grade_whitespace_course_code_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.assign_grade_to_student("S01", " ", 9.0)  # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_identifier"


# ---------------------------------------------------------------------
# value validation
# ---------------------------------------------------------------------

def test_assign_grade_missing_value_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.assign_grade_to_student("S01", "C01", None)    #type: ignore[arg-type]

    assert exc.value.field == "value"
    assert exc.value.code == "missing_field"


def test_assign_grade_non_numeric_value_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.assign_grade_to_student("S01", "C01", "A+")  # type: ignore[arg-type]

    assert exc.value.field == "value"
    assert exc.value.code == "invalid_type"


def test_assign_grade_boolean_value_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.assign_grade_to_student("S01", "C01", True)  # bool must be rejected

    assert exc.value.field == "value"
    assert exc.value.code == "invalid_type"


def test_assign_grade_nan_value_raises_invalid_value_error(sms):
    with pytest.raises(InvalidValueError) as exc:
        sms.assign_grade_to_student("S01", "C01", math.nan)

    assert exc.value.field == "value"
    assert exc.value.code == "invalid_value"


def test_assign_grade_infinite_value_raises_invalid_value_error(sms):
    with pytest.raises(InvalidValueError) as exc:
        sms.assign_grade_to_student("S01", "C01", math.inf)

    assert exc.value.field == "value"
    assert exc.value.code == "invalid_value"


# ---------------------------------------------------------------------
# side-effect guarantees
# ---------------------------------------------------------------------

def test_assign_grade_validation_failure_has_no_side_effects(sms):
    with pytest.raises(MissingFieldError):
        sms.assign_grade_to_student("S01", "C01", None)

    assert sms.student_repo.list_all() == ()
    assert sms.course_repo.list_all() == ()
