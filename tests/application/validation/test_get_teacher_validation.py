# tests/application/validation/test_get_teacher_validation.py

"""
Application-level validation tests for StudentManagementSystem.get_teacher

Scope:
    - Validate identifier shape and semantics (not existence)
    - Assert on structured validation errors (field + type)
    - Guarantee validation occurs before repository access

Phase: Query Validation (Teacher)
"""

import pytest

from application.services.student_management_system import StudentManagementSystem
from application.validation.errors import (
    MissingFieldError,
    InvalidTypeError,
    InvalidIdentifierError,
)

from infrastructure.in_memory.in_memory_student_repository import (
    InMemoryStudentRepository,
)
from infrastructure.in_memory.in_memory_teacher_repository import (
    InMemoryTeacherRepository,
)
from infrastructure.in_memory.in_memory_course_repository import (
    InMemoryCourseRepository,
)


# ---------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------

@pytest.fixture
def sms() -> StudentManagementSystem:
    """Fresh SMS instance with empty in-memory repositories."""
    return StudentManagementSystem(
        student_repo=InMemoryStudentRepository(),
        teacher_repo=InMemoryTeacherRepository(),
        course_repo=InMemoryCourseRepository(),
    )


# ---------------------------------------------------------------------
# identifier validation
# ---------------------------------------------------------------------

def test_get_teacher_missing_teacher_id_raises_missing_field_error(sms):
    with pytest.raises(MissingFieldError) as exc:
        sms.get_teacher(None)    # type: ignore[arg-type]

    assert exc.value.field == "teacher_id"
    assert exc.value.code == "missing_field"

def test_get_teacher_non_string_teacher_id_raises_invalid_type_error(sms):
    with pytest.raises(InvalidTypeError) as exc:
        sms.get_teacher(123)     # type: ignore[arg-type]

    assert exc.value.field == "teacher_id"
    assert exc.value.code == "invalid_type"

def test_get_teacher_whitespace_teacher_id_raises_invalid_identifier_error(sms):
    with pytest.raises(InvalidIdentifierError) as exc:
        sms.get_teacher(" ")     # type: ignore[arg-type]

    assert exc.value.field == "teacher_id"
    assert exc.value.code == "invalid_identifier"