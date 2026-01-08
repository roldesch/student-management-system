# infrastructure/sqlite/errors.py

class PersistenceError(Exception):
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


class DuplicateEntityError(PersistenceError):
    """
    Raised when an insert or update violates a uniqueness constraint
    (e.g., duplicate primary key or UNIQUE index).
    """
    pass


class EntityNotFoundError(PersistenceError):
    """
    Raised when a repository operation expects an entity to exist,
    but no corresponding row is found.

    This applies only to persistence-layer existence checks (e.g. get/remove),
    not to validation or domain invariant failures.
    """
    pass


class ForeignKeyViolationError(PersistenceError):
    """
    Raised when a foreign key constraint is violated, indicating
    structurally invalid references at the persistence level.
    """
    pass
