# tests/application/validation/test_remove_course_validation.py

"""
Application-level validation for StudentManagementSystem.remove_course

Scope:
    - Validate input shape and semantics (not business rules)
    - Assert on structured validation errors (field + type)
    - Guarantee no side effects on validation failure

Phase: Entity Deletion Validation (Course)
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

def test_remove_course_missing_course_code_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.remove_course(None)    # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "missing_field"


def test_remove_course_non_string_course_code_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.remove_course(123)    # type: ignore[arg-type]

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_type"


def test_remove_course_whitespace_course_code_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.remove_course(" ")

    assert exc.value.field == "course_code"
    assert exc.value.code == "invalid_identifier"


# ---------------------------------------------------------------------
# side-effect guarantees
# ---------------------------------------------------------------------

def test_remove_course_validation_failure_has_no_side_effects(sms):
    with pytest.raises(InvalidIdentifierError):
        sms.remove_course(" ")

    # No course should have been persisted
    assert sms.course_repo.list_all() == ()



