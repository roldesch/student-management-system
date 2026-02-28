# tests/application/validation/test_add_course_validation.py

"""
Application-level validation for StudentManagementSystem.add_course

Scope:
    - Validate input shape and semantics (not business rules)
    - Assert on structured validation errors (field + type)
    - Guarantee no side effects on validation failure

Phase: Entity Creation Validation (Course)
"""

import pytest

from application.validation.errors import (
    MissingFieldError,
    EmptyValueError,
    InvalidTypeError,
    InvalidIdentifierError,
)

# ---------------------------------------------------------------------
# course_code validation
# ---------------------------------------------------------------------

def test_add_course_missing_course_code_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.add_course(None, "Math")    # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "missing_field"


def test_add_course_non_string_course_code_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.add_course(123, "Math")    # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_type"


def test_add_course_whitespace_course_code_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.add_course(" ", "Math")

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_identifier"


# ---------------------------------------------------------------------
# name validation
# ---------------------------------------------------------------------

def test_add_course_missing_name_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.add_course("C01", None)    # type: ignore[arg-type]

    assert exc.value.field == "name"
    assert exc.value.code == "missing_field"


def test_add_course_non_string_name_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.add_course("C01", 42)    # type: ignore[arg-type]

    assert exc.value.field == "name"
    assert exc.value.code == "invalid_type"


def test_add_course_whitespace_name_raises_empty_value_error(sms):
    with pytest.raises(EmptyValueError) as exc:
        sms.add_course("C01", " ")

    assert exc.value.field == "name"
    assert exc.value.code == "empty_value"


# ---------------------------------------------------------------------
# side-effect guarantees
# ---------------------------------------------------------------------

def test_add_course_validation_failure_has_no_side_effects(sms):
    with pytest.raises(EmptyValueError):
        sms.add_course("C01", " ")

    # No course should have been persisted
    assert sms.course_repo.list_all() == ()



