# tests/application/validation/test_drop_student_from_course_validation.py

"""
Application-level validation tests for StudentManagementSystem.drop_student_from_course

Scope:
    - Validate identifier shape and semantics (not existence, not relationships)
    - Assert on structured validation errors (field + type)
    - Guarantee validation occurs before any domain interaction

Phase: Relationship Command Validation (Drop a Student from a Course)
"""

import pytest

from application.validation.errors import (
    MissingFieldError,
    InvalidTypeError,
    InvalidIdentifierError,
)


# ---------------------------------------------------------------------
# student_id validation
# ---------------------------------------------------------------------

def test_drop_student_missing_student_id_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.drop_student_from_course(None, "C01")   # type: ignore[arg-type]

    assert exc.value.field == "student_id"
    assert exc.value.code == "missing_field"


def test_drop_student_non_string_student_id_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.drop_student_from_course(123, "C01")  # type: ignore[arg-type]

    assert exc.value.field == "student_id"
    assert exc.value.code == "invalid_type"


def test_drop_student_whitespace_student_id_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.drop_student_from_course(" ", "C01")

    assert exc.value.field == "student_id"
    assert exc.value.code == "invalid_identifier"


# ---------------------------------------------------------------------
# course_code validation
# ---------------------------------------------------------------------

def test_drop_student_missing_course_code_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.drop_student_from_course("S01", None)    # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "missing_field"


def test_drop_student_non_string_course_code_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.drop_student_from_course("S01", 123)    # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_type"

def test_drop_student_whitespace_course_code_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.drop_student_from_course("S01", " ")

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_identifier"


# ---------------------------------------------------------------------
# side-effect guarantees
# ---------------------------------------------------------------------

def test_drop_student_validation_failure_has_no_side_effects(sms):
    with pytest.raises(InvalidIdentifierError):
        sms.drop_student_from_course(" ", "C01")

    # No repositories should have been mutated
    assert sms.student_repo.list_all() == ()
    assert sms.course_repo.list_all() == ()