# tests/application/validation/test_student_validation.py

"""
Application-level validation tests for StudentManagementSystem.get_student

Scope:
    - Validate identifier shape and semantics (not existence)
    - Assert on structured validation errors (field + type)
    - Guarantee validation occurs before repository access

Phase: Query Validation (Student)
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

def test_get_student_missing_student_id_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.get_student(None)    # type: ignore[arg-type]

    assert exc.value.field == "student_id"
    assert exc.value.code == "missing_field"

def test_get_student_non_string_student_id_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.get_student(123)     # type: ignore[arg-type]

    assert exc.value.field == "student_id"
    assert exc.value.code == "invalid_type"

def test_get_student_whitespace_student_id_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.get_student(" ")     # type: ignore[arg-type]

    assert exc.value.field == "student_id"
    assert exc.value.code == "invalid_identifier"