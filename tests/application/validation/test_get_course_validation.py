# tests/application/validation/test_get_course_validation.py

"""
Application-level validation tests for StudentManagementSystem.get_course

Scope:
    - Validate identifier shape and semantics (not existence)
    - Assert on structured validation errors (field + type)
    - Guarantee validation occurs before repository access

Phase: Query Validation (Course)
"""

import pytest

from application.validation.errors import (
    MissingFieldError,
    InvalidTypeError,
    InvalidIdentifierError,
)


# ---------------------------------------------------------------------
# identifier validation
# ---------------------------------------------------------------------

def test_get_course_missing_course_code_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.get_course(None)    # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "missing_field"

def test_get_course_non_string_course_code_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.get_course(123)     # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_type"

def test_get_course_whitespace_course_code_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.get_course(" ")     # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_identifier"