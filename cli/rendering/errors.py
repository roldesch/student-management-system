# cli/rendering/errors.py

from typing import Tuple

# -------------------------------------------------
# Import exception types (classification only)
# -------------------------------------------------
from cli.errors import ConfigurationError
from application.validation.errors import ApplicationValidationError
from domain.exceptions.domain_exceptions import (
    DomainError,
    EntityNotFoundError,
    DuplicateEntityError,
)

# -------------------------------------------------
# Exit code constants (must match CLI policy)
# -------------------------------------------------
EXIT_CONFIGURATION_ERROR = 2
EXIT_VALIDATION_ERROR = 2
EXIT_DOMAIN_ERROR = 3
EXIT_STATE_ERROR = 4
EXIT_SYSTEM_ERROR = 10


# -------------------------------------------------
# Public API
# -------------------------------------------------
def render_error(exc: Exception) -> Tuple[int, str]:
    """
    Convert an exception into a (exit_code, message) tuple.

    This function:
        - Performs NO side effects
        - Does NOT exit the process
        - Does NOT print
        - Encodes CLI error policy in one place

    It is safe to unit-test in isolation.
    """
    # -------------------------------------------------
    # Configuration errors (composition boundary)
    # -------------------------------------------------
    if isinstance(exc, ConfigurationError):
        return (
            EXIT_CONFIGURATION_ERROR,
            _render_configuration_error(exc),
        )

    # -------------------------------------------------
    # Application-level validation errors
    # -------------------------------------------------
    if isinstance(exc, ApplicationValidationError):
        return (
            EXIT_VALIDATION_ERROR,
            _render_application_validation_error(exc),
        )

    # -------------------------------------------------
    # Repository / state errors
    # -------------------------------------------------
    if isinstance(exc, (EntityNotFoundError, DuplicateEntityError)):
        return (
            EXIT_STATE_ERROR,
            _render_state_error(exc),
        )

    # -------------------------------------------------
    # Domain rule violations
    # -------------------------------------------------
    if isinstance(exc, DomainError):
        return (
            EXIT_DOMAIN_ERROR,
            _render_domain_error(exc),
            )

    # -------------------------------------------------
    # Fallback: system / unexpected error
    # -------------------------------------------------
    return (
        EXIT_SYSTEM_ERROR,
        "Unexpected system error.",
    )


# -------------------------------------------------
# Rendering helpers (private)
# -------------------------------------------------
def _render_configuration_error(exc: ConfigurationError) -> str:
    """
    Render configuration errors into stable, human-readable form.

    Messages here are stable CLI output, not internal exception text.
    """
    # Stable prefix + deterministic message payload
    return f"Invalid configuration: {str(exc)}"


def _render_application_validation_error(
        exc: ApplicationValidationError,
) -> str:
    """
    Render application validation errors into human-readable form.

    Messages here are stable CLI output, not internal exception text.
    """
    field = getattr(exc, "field", None)

    if field:
        return f"Invalid input: {field}"
    return "Invalid input."


def _render_state_error(exc: Exception) -> str:
    """
    Render entity existence / state-related errors.
    """
    return "Operation failed due to system state."

def _render_domain_error(exc: DomainError) -> str:
    """
    Render domain rule violations.
    """
    return "Operation violates business rules."


