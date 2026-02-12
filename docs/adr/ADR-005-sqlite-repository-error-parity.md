ADR-005 — SQLite Repository Error Parity and Taxonomy Boundary Preservation
Status

Accepted

Context

During Phase-6 (System Verification) of SQLite persistence integration, failures were observed in CLI subprocess tests when the SQLite backend was enabled.

Specifically:

Missing entity lookups returned exit code 10 (Unexpected system error)

Expected behavior was exit code 4 (State error)

Stack traces revealed that SQLite repositories were raising:

infrastructure.sqlite.errors.EntityNotFoundError


However, the CLI error renderer classifies state errors based on:

domain.exceptions.domain_exceptions.EntityNotFoundError
domain.exceptions.domain_exceptions.DuplicateEntityError


Because these were distinct classes, the CLI did not recognize SQLite state exceptions and treated them as system-level failures.

This violated Phase-6’s drop-in guarantee:

SQLite must behave identically to the in-memory backend at the observable system level.

At the same time, the broader discussion surfaced a deeper architectural concern:

The current exception taxonomy conflates domain rule violations and repository/state conditions, as both inherit from DomainError.

However, redesigning the taxonomy during Phase-6 would violate execution discipline:

Verification phases must not introduce structural redesign.

Therefore, a strict separation between:

Backend parity correction (Phase-6)

Taxonomy redesign (future ADR)

was required.

Problem

SQLite repositories defined and raised infrastructure-level semantic exceptions:

infrastructure.sqlite.errors.EntityNotFoundError

infrastructure.sqlite.errors.DuplicateEntityError

This introduced:

Duplicate semantic exception hierarchies

Backend-specific exception identity

CLI classification mismatch

Violation of repository contract parity (ADR-00R)

The in-memory repositories define the current system contract. SQLite must conform to it before any redesign.

Decision
1. Canonical Exception Identity

SQLite repositories must raise the same canonical state exception classes as the in-memory repositories:

domain.exceptions.domain_exceptions.EntityNotFoundError
domain.exceptions.domain_exceptions.DuplicateEntityError


These are treated by the CLI as:

EXIT_STATE_ERROR (4)


No new base classes were introduced in this ADR.

2. Removal of Duplicate Infrastructure Semantic Exceptions

The following classes were removed from:

infrastructure/sqlite/errors.py


EntityNotFoundError

DuplicateEntityError

Infrastructure must not define semantic state conditions.

Infrastructure error types are now limited to:

PersistenceError

ConcurrentUpdateError

ForeignKeyViolationError

Other low-level SQLite technical failures

Infrastructure errors represent technical persistence failures only.

3. Contract Test Alignment

SQLite repository contract tests were updated to import and assert against the canonical domain exception classes rather than removed infrastructure exceptions.

This preserves:

Backend-agnostic repository contract enforcement

Single source of truth for semantic state errors

4. Explicit Non-Decision: No Taxonomy Redesign

This ADR explicitly does not:

Introduce a StateError base class

Refactor DomainError hierarchy

Separate domain vs state exceptions structurally

Modify CLI classification logic

Although architectural concerns were identified regarding taxonomy conflation, those are deferred to a separate future ADR.

Phase discipline requires parity verification to complete before structural redesign.

Rationale

This decision preserves:

Phase-6 integrity (drop-in backend guarantee)

Backend substitution correctness

Repository contract parity (ADR-00R)

Error taxonomy consistency within current system contract

Clean separation of semantic vs technical errors at infrastructure boundary

It avoids:

Mixing verification with redesign

Hiding regressions behind structural refactors

Breaking execution sequencing discipline

Consequences
Positive

SQLite backend now behaves identically to in-memory backend at CLI level.

Exit codes match expected semantics.

No duplicate semantic exception hierarchies remain in infrastructure.

Repository contract tests enforce canonical exception identity.

Trade-offs

The existing taxonomy conflation (DomainError including state errors) remains.

Structural cleanup is deferred.

This trade-off is intentional and time-bounded.

Enforcement

The following are now considered architectural violations:

Defining semantic state exceptions in infrastructure namespace.

Allowing backend-specific exception classes to escape to CLI.

Translating repository exceptions in application services.

Redesigning taxonomy during Phase-6 verification.

Follow-Up (Future ADR)

A separate ADR may address:

Separation of DomainError (business rule violations) from StateError (existence/uniqueness conditions)

Introduction of a canonical repository/state base class

CLI mapping refactor to depend on explicit state error hierarchy

That redesign must:

Be isolated from backend integration work

Preserve repository contract strictness

Maintain backward compatibility or provide migration plan

Summary

SQLite integration revealed duplicate semantic exception hierarchies that broke backend parity.

The resolution:

Align SQLite repositories with canonical exception classes.

Remove infrastructure-defined semantic state errors.

Preserve strict phase discipline.

Defer taxonomy redesign.

Phase-6 verifies substitution.
Structural redesign happens only after verification is complete.