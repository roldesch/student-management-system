# tests/application/validation/test_remove_student_validation.py

"""
Application-level validation tests for StudentManagementSystem.remove_student

Scope:
    - Validate identifier shape and semantics (not existence, not business rules)
    - Assert on structured validation errors (field + type)
    - Guarantee no side effects on validation failure

Phase: Entity Deletion Validation (Student)
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

def test_remove_student_missing_student_id_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.remove_student(None)   # type: ignore[arg-type]

    assert exc.value.field == "student_id"
    assert exc.value.code == "missing_field"

def test_remove_student_non_string_student_id_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.remove_student(123)    # type: ignore[arg-type]

    assert exc.value.field == "student_id"
    assert exc.value.code == "invalid_type"

def test_remove_student_whitespace_student_id_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.remove_student("  ")

    assert exc.value.field == "student_id"
    assert exc.value.code == "invalid_identifier"



# ---------------------------------------------------------------------
# side-effect guarantees
# ---------------------------------------------------------------------

def test_remove_student_validation_failure_has_no_side_effects(sms):
    with pytest.raises(InvalidIdentifierError):
        sms.remove_student(" ")

    # No student should have been persisted
    assert sms.student_repo.list_all() == ()