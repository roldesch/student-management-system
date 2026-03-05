# tests/application/validation/test_add_student_validation.py

"""
Application-level validation tests for StudentManagementSystem.add_student

Scope:
    - Validate input shape and semantics (not business rules)
    - Assert on structured validation errors (field + type)
    - Guarantee no side effects on validation failure

Phase: Entity Creation Validation (Student)
"""

import pytest

from application.validation.errors import (
    MissingFieldError,
    EmptyValueError,
    InvalidTypeError,
    InvalidIdentifierError,
)


# ---------------------------------------------------------------------
# student_id validation
# ---------------------------------------------------------------------

def test_add_student_missing_student_id_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.add_student(None, "Alice")   # type: ignore[arg-type]

    assert exc.value.field == "student_id"
    assert exc.value.code == "missing_field"

def test_add_student_non_string_student_id_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.add_student(123, "Alice")    # type: ignore[arg-type]

    assert exc.value.field == "student_id"
    assert exc.value.code == "invalid_type"

def test_add_student_whitespace_student_id_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.add_student("  ", "Alice")

    assert exc.value.field == "student_id"
    assert exc.value.code == "invalid_identifier"

# ---------------------------------------------------------------------
# name validation
# ---------------------------------------------------------------------

def test_add_student_missing_name_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.add_student("S01", None)    # type: ignore[arg-type]

    assert exc.value.field == "name"
    assert exc.value.code == "missing_field"

def test_add_student_non_string_name_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.add_student("S01", 42)    # type: ignore[arg-type]

    assert exc.value.field == "name"
    assert exc.value.code == "invalid_type"

def test_add_student_whitespace_name_raises_empty_value_error(sms):
    with pytest.raises(EmptyValueError) as exc:
        sms.add_student("S01", "  ")

    assert exc.value.field == "name"
    assert exc.value.code == "empty_value"

# ---------------------------------------------------------------------
# side-effect guarantees
# ---------------------------------------------------------------------

def test_add_student_validation_failure_has_no_side_effects(sms):
    with pytest.raises(EmptyValueError):
        sms.add_student("S01", "")

    # No student should have been persisted
    assert sms.student_repo.list_all() == ()

