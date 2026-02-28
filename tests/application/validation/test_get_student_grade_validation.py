# tests/application/validation/test_get_student_grade_validation.py

"""
Application-level validation tests for StudentManagementSystem.get_student_grade

Scope:
    - Validate identifier shape and semantics (not existence, not relationships)
    - Assert on structured validation errors (field + type)
    - Guarantee validation occurs before any domain interaction

Phase: Grade Validation (Get student grade)
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

def test_get_student_grade_missing_student_id_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.get_student_grade(None, "C01")    # type: ignore[arg-type]

    assert exc.value.field == "student_id"
    assert exc.value.code == "missing_field"


def test_get_student_grade_non_string_student_id_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.get_student_grade(123, "C01")    # type: ignore[arg-type]

    assert exc.value.field == "student_id"
    assert exc.value.code == "invalid_type"


def test_get_student_grade_whitespace_student_id_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.get_student_grade(" ", "C01")

    assert exc.value.field == "student_id"
    assert exc.value.code == "invalid_identifier"


# ---------------------------------------------------------------------
# course_code validation
# ---------------------------------------------------------------------

def test_get_student_grade_missing_course_code_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.get_student_grade("S01", None)    # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "missing_field"


# ---------------------------------------------------------------------
# side-effect guarantees
# ---------------------------------------------------------------------

def test_get_student_grade_validation_failure_has_no_side_effects(sms):
    with pytest.raises(MissingFieldError):
        sms.get_student_grade(None, "C01")

    assert sms.student_repo.list_all() == ()
    assert sms.course_repo.list_all() == ()



def test_get_student_grade_non_string_course_code_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.get_student_grade("S01", 123)  # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_type"


def test_get_student_grade_whitespace_course_code_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.get_student_grade("S01", " ")  # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_identifier"
