import pytest

from cli.rendering.errors import (
    render_error,
    EXIT_VALIDATION_ERROR,
    EXIT_DOMAIN_ERROR,
    EXIT_STATE_ERROR,
    EXIT_SYSTEM_ERROR,
)

from application.validation.errors import ApplicationValidationError
from domain.exceptions.domain_exceptions import (
    DomainError,
    EntityNotFoundError,
    DuplicateEntityError,
    EnrollmentError,
    GradeError,
)


# -------------------------------------------------
# Application-level validation errors
# -------------------------------------------------

def test_application_validation_error_with_field():
    exc = ApplicationValidationError(field="student_id")

    exit_code, message = render_error(exc)

    assert exit_code == EXIT_VALIDATION_ERROR
    assert message == "Invalid input: student_id"


# -------------------------------------------------
# State / repository errors
# -------------------------------------------------

def test_entity_not_found_error():
    exc = EntityNotFoundError("Student not found")

    exit_code, message = render_error(exc)

    assert exit_code == EXIT_STATE_ERROR
    assert message == "Operation failed due to system state."


def test_duplicate_entity_error():
    exc = DuplicateEntityError("Student already exists")

    exit_code, message = render_error(exc)

    assert exit_code == EXIT_STATE_ERROR
    assert message == "Operation failed due to system state."


# -------------------------------------------------
# Domain rule violations
# -------------------------------------------------

def test_domain_error():
    exc = DomainError("Generic domain violation")

    exit_code, message = render_error(exc)

    assert exit_code == EXIT_DOMAIN_ERROR
    assert message == "Operation violates business rules."


@pytest.mark.parametrize(
    "exception",
    [
        EnrollmentError("Duplicate enrollment"),
        GradeError("Invalid grade"),
    ],
)
def test_domain_subclass_errors(exception):
    exit_code, message = render_error(exception)

    assert exit_code == EXIT_DOMAIN_ERROR
    assert message == "Operation violates business rules."


# -------------------------------------------------
# Unexpected / system errors
# -------------------------------------------------

def test_unexpected_exception():
    exc = RuntimeError("Something went very wrong")

    exit_code, message = render_error(exc)

    assert exit_code == EXIT_SYSTEM_ERROR
    assert message == "Unexpected system error."


# -------------------------------------------------
# Purity / determinism contract
# -------------------------------------------------

def test_render_error_is_pure_and_deterministic():
    exc = RuntimeError("Boom")

    result1 = render_error(exc)
    result2 = render_error(exc)

    assert result1 == result2
