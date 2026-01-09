## Exception Handling Responsibility Rule

This section defines the **authoritative exception-handling policy** for the Student Management System (SMS).

The goal is to prevent accidental error swallowing, inappropriate translation, and architectural drift by clearly assigning **where exceptions may be caught** and **where they must be raised directly**.

This rule is **normative**.

---

## Core Principle

> **A layer may catch exceptions only if it owns cleanup or translation responsibility.**
>
> If a layer does not own cleanup or translation, it must raise exceptions directly and allow them to propagate.

This principle applies uniformly across the system and explains intentional differences in exception-handling style between layers.

---

## Layer-Specific Rules

### Domain Layer

**Policy:** *Raise-only*

The Domain layer:

* Raises domain exceptions to express business rule violations
* Does **not** catch exceptions
* Does **not** perform cleanup or translation

Rationale:

* Domain exceptions represent **business truth**, not recoverable failures
* Catching exceptions in the domain would hide invariant violations or corrupt intent

Example:

```python
if course in self._courses:
    raise EnrollmentError(...)
```

---

### Application Validation Layer

**Policy:** *Raise-only*

The Application Validation layer:

* Raises validation exceptions to reject invalid input
* Performs no side effects prior to raising
* Does **not** catch exceptions

Rationale:

* Validation is fail-fast
* No resources have been acquired
* No cleanup is required

Example:

```python
if not student_id.strip():
    raise InvalidIdentifierError(field="student_id")
```

---

### Infrastructure Layer (UnitOfWork, Repositories)

**Policy:** *Selective catch-and-rethrow*

Infrastructure components may catch exceptions **only** to:

* Restore system integrity (e.g., rollback a transaction)
* Release owned resources (e.g., close a database connection)
* Translate low-level failures into stable infrastructure exceptions

Rules:

* Catch exceptions **only** where cleanup or translation is required
* Always re-raise after responsibility is fulfilled
* Never swallow exceptions
* Never collapse distinct failure modes into generic errors

Rationale:

* Infrastructure layers manage fragile external resources
* Failure may leave the system in a partially modified state
* Cleanup is mandatory before propagation

Example:

```python
try:
    connection.commit()
except sqlite3.Error:
    connection.rollback()
    raise
```

---

### Presentation Layer (CLI, API Adapters)

**Policy:** *Catch and render*

The Presentation layer:

* Catches exceptions from lower layers
* Maps exception types to exit codes, messages, or HTTP responses
* Does **not** rethrow after rendering

Rationale:

* Presentation layers terminate execution or return responses
* They are responsible for user-facing interpretation

---

## Summary Rule of Thumb

> **Layers that express truth raise exceptions.**
>
> **Layers that manage resources may catch exceptions to restore integrity, then re-raise.**
>
> **Layers that face users catch exceptions to render outcomes.**

Any deviation from this policy must be treated as an architectural violation and explicitly justified.

---

## Status

This rule is **locked** and applies to all current and future components of the Student Management System.
