# tests/application/validation/test_remove_teacher_validation.py

"""
Application-level validation tests for StudentManagementSystem.remove_teacher

Scope:
    - Validate identifier shape and semantics (not existence, not business rules)
    - Assert on structured validation errors (field + type)
    - Guarantee no side effects on validation failure

Phase: Entity Deletion Validation (Teacher)
"""

import pytest

from application.validation.errors import (
    MissingFieldError,
    InvalidTypeError,
    InvalidIdentifierError,
)


# ---------------------------------------------------------------------
# teacher_id validation
# ---------------------------------------------------------------------

def test_remove_teacher_missing_teacher_id_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.remove_teacher(None)   # type: ignore[arg-type]

    assert exc.value.field == "teacher_id"
    assert exc.value.code == "missing_field"

def test_remove_teacher_non_string_teacher_id_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.remove_teacher(123)    # type: ignore[arg-type]

    assert exc.value.field == "teacher_id"
    assert exc.value.code == "invalid_type"

def test_remove_teacher_whitespace_teacher_id_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.remove_teacher("  ")

    assert exc.value.field == "teacher_id"
    assert exc.value.code == "invalid_identifier"



# ---------------------------------------------------------------------
# side-effect guarantees
# ---------------------------------------------------------------------

def test_remove_teacher_validation_failure_has_no_side_effects(sms):
    with pytest.raises(InvalidIdentifierError):
        sms.remove_teacher(" ")

    # No teacher should have been persisted
    assert sms.teacher_repo.list_all() == ()