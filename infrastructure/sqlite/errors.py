# infrastructure/sqlite/errors.py

from domain.exceptions.domain_exceptions import SMSError


class PersistenceError(SMSError):
    """
    Base class for all persistence-layer errors.

    These errors represent failures at the infrastructure boundary and
    must never be raised by the domain or application layers.
    """
    pass


class ConcurrentUpdateError(PersistenceError):
    """
    Raised when a SQLite operation fails due to concurrency constraints,
    such as database locks or busy timeouts.
    """
    pass


class ForeignKeyViolationError(PersistenceError):
    """
    Raised when a foreign key constraint is violated, indicating
    structurally invalid references at the persistence level.
    """
    pass
