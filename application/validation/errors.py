# application/validation/errors.py

"""
Application-level validation exceptions.

These exceptions represent *invalid input* to application services.
They are raised **before** any domain logic executes and must never be
raised from the Domain Layer.

Design principles:
- Structured (FIELDS-based), not message-based
- One field, one cause
- No business-rule semantics
- CLI / API layers are responsible for rendering messages
"""

from __future__ import annotations


class ApplicationError(Exception):
    """
    Base class for all application-layer errors.

    This sits above validation errors and allows the presentation layer
    (CLI / API) to distinguish application failures from domain failures.
    """
    pass


class ApplicationValidationError(ApplicationError):
    """
    Base class for application-level *input validation* errors.

    Characteristics:
    - Raised before domain objects are created
    - Side-effect free
    - Deterministic

    Attributes:
        field: The name of the invalid input field
    """

    code: str = "validation_error"

    def __init__(self, *, field: str) -> None:
        self.field = field
        super().__init__(field)


class MissingFieldError(ApplicationValidationError):
    """
    Raised when a required input field is missing (value is None).
    """
    code = "missing_field"


class EmptyValueError(ApplicationValidationError):
    """
    Raised when a value is present but empty or whitespace-only.
    """
    code = "empty_value"


class InvalidTypeError(ApplicationValidationError):
    """
    Raised when a value has the wrong semantic type.

    Examples:
        - grade value is not numeric
        - identifier is not a string
    """
    code = "invalid_type"


class InvalidValueError(ApplicationValidationError):
    """
    Raised when a value has the correct type but is semantically invalid.

    Examples:
        - NaN or infinite number
    """
    code = "invalid_value"


class InvalidIdentifierError(ApplicationValidationError):
    """
    Raised when an identifier is structurally invalid.

    Examples:
        - empty or whitespace-only identifier
        - Malformed identifier format
    """
    code = "invalid_identifier"