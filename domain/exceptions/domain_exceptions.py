# domain/exceptions/domain_exceptions.py

# -------------------------------------------------
# SMS Semantic Root
# -------------------------------------------------

class SMSError(Exception):
    """
    Root exception for all SMS runtime semantic errors.

    This provides a shared classification boundary across
    domain, repository/state, and infrastructure layers.
    """
    pass


# -------------------------------------------------
# Domain Errors
# -------------------------------------------------

class DomainError(SMSError):
    """
    Base class for all domain-related exceptions.

    Used to differentiate domain rule violations from
    repository/state and infrastructure failures.
    """
    pass

# -------------- Entity Errors -------------------

class EntityError(DomainError):
    """Base class for errors related to entities (Student, Teacher, Course)."""
    pass

class EntityNotFoundError(EntityError):
    """Raised when a student, teacher, or course cannot be found."""
    pass

class DuplicateEntityError(EntityError):
    """Raised when attempting to create an entity that already exists."""
    pass

# -------------- Relationship Errors ----------------------

class RelationshipError(DomainError):
    """Base class for errors involving relationships between entities."""
    pass

class EnrollmentError(RelationshipError):
    """Raised when enrollment rules are violated (duplicate enrollment, invalid drop, etc.)."""
    pass

class TeacherAssignmentError(RelationshipError):
    """Raised when assignment rules are violated."""
    pass

class GradeError(RelationshipError):
    """Raised when grade-related rules are violated."""
    pass


# -------------------------------------------------
# Repository / State Errors
# -------------------------------------------------

class StateError(SMSError):
    """
    Base class for repository/state contract failures.

    These errors represent identity existence and uniqueness
    violations at the repository boundary.
    """
    pass