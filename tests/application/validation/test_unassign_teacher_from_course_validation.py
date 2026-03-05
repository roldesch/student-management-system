# tests/application/validation/test_unassign_teacher_from_course_validation.py

"""
Application-level validation tests for StudentManagementSystem.unassign_teacher_from_course

Scope:
    - Validate identifier shape and semantics (not existence, not relationships)
    - Assert on structured validation errors (field + type)
    - Guarantee validation occurs before any domain interaction

Phase: Relationship Command Validation (Unassign a Teacher from a Course)
"""

import pytest

from application.validation.errors import (
    MissingFieldError,
    InvalidTypeError,
    InvalidIdentifierError,
)


# ---------------------------------------------------------------------
# course_code validation
# ---------------------------------------------------------------------

def test_unassign_teacher_missing_course_code_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.unassign_teacher_from_course(None)    # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "missing_field"


def test_unassign_teacher_non_string_course_code_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.unassign_teacher_from_course(123)    # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_type"

def test_unassign_teacher_whitespace_course_code_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.unassign_teacher_from_course(" ")

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_identifier"


# ---------------------------------------------------------------------
# side-effect guarantees
# ---------------------------------------------------------------------

def test_unassign_teacher_validation_failure_has_no_side_effects(sms):
    with pytest.raises(InvalidIdentifierError):
        sms.unassign_teacher_from_course(" ")

    # No repositories should have been mutated
    assert sms.teacher_repo.list_all() == ()
    assert sms.course_repo.list_all() == ()