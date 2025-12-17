# Application-Level Validation

## Purpose

Application-level validation exists to act as the **semantic gateway** into the Student Management System.

Its purpose is to:

* Reject malformed or nonsensical input **before** any domain logic executes
* Protect the domain layer from invalid construction or invocation
* Provide a **stable, predictable validation contract** to all presentation layers (CLI, future APIs)

Application-level validation answers a single question:

> *“Is this input structurally and semantically valid for this use case?”*

It is intentionally positioned **upstream of domain execution** and downstream of syntax-only concerns handled by presentation layers.

---

## Non-Goals

Application-level validation must **not**:

* Enforce business rules or invariants
* Inspect repository state or entity existence
* Perform persistence-related checks
* Normalize, coerce, or repair invalid input
* Aggregate multiple validation failures
* Produce human-readable or user-facing messages

If any of the above behaviors are required, validation is misplaced and must be relocated to the appropriate layer.

---

## Layered Responsibility Split

Validation responsibilities are explicitly divided across architectural layers:

| Concern                         | Responsible Layer  |
| ------------------------------- | ------------------ |
| Argument presence (syntax)      | Presentation (CLI) |
| Type coercion (e.g. str → int)  | Presentation (CLI) |
| Input shape & semantic validity | **Application**    |
| Business invariants             | Domain             |
| Persistence constraints         | Repositories       |
| Error rendering & messaging     | Presentation (CLI) |

The application layer is the **semantic boundary** of the system. All input crossing into the domain must first pass through this gate.

---

## Validation Placement Rule

Application-level validation is performed:

* **Inline** within each public application service method
* **Before**:

  * Any repository access
  * Any domain object construction
  * Any side effects

No shared validator modules or external validation frameworks are introduced at this stage.

Validation logic must remain **explicit, visible, and reviewable** at the application boundary.

---

## Error Model Principles

Application-level validation failures are expressed through a dedicated error model governed by the following principles:

* **Distinct from domain errors**
  Validation errors are never domain exceptions and must not be interpreted as business rule violations.

* **Fail-fast**
  The first detected validation failure immediately aborts execution.

* **Single-field, single-cause**
  Each validation error refers to exactly one input field and exactly one cause.

Validation errors are **structural signals**, not narrative explanations. Interpretation and presentation are delegated to consuming layers.

---

## Conceptual Validation Error Taxonomy

The application layer defines a conceptual hierarchy of validation errors to describe invalid input precisely and consistently.

> **Status:** Conceptual, not yet fully implemented

```
ApplicationValidationError
├── MissingFieldError
├── EmptyValueError
├── InvalidTypeError
├── InvalidValueError
└── InvalidIdentifierError
```

Each error type:

* Represents one semantic class of invalid input
* Refers to exactly one input field
* Carries structured facts, not human-readable messages

This taxonomy is **normative** for all future presentation layers and must not be bypassed or substituted.

---

## Strict Boundary Rule: What Is **Not** an ApplicationValidationError

This section is **normative**. Treat it as a hard architectural rule.

### Definition

An `ApplicationValidationError` represents **only** failures that:

* Occur at the **application boundary**
* Are detected **before any domain logic executes**
* Are **independent** of business rules, system state, and infrastructure concerns

Anything outside this definition must **not** use `ApplicationValidationError` or any of its subclasses.

---

### Explicitly Not Application Validation Errors

The following categories must **never** raise `ApplicationValidationError`.

#### ❌ Domain rule violations

Domain exceptions must never be wrapped, translated, or rethrown as application validation errors.

Examples include (but are not limited to):

* `EnrollmentError`
* `TeacherAssignmentError`
* `GradeError`
* `EntityError`

These represent **business invariants**, not invalid input.

**Rule:**
If the domain rejected it, it is not an application validation error.

---

#### ❌ Entity existence or state-based failures

Examples:

* Student not found
* Course does not exist
* Teacher identifier unknown

These are **state-based** failures, not input-shape failures.

They belong to:

* Repository behavior (e.g. `EntityNotFoundError`), or
* Domain logic, if modeled there

**Rule:**
“Valid identifier, but nothing exists” is not validation.

---

#### ❌ Cross-field or relational validation

Examples:

* “student_id and course_code must match”
* “teacher cannot be assigned to two courses”
* “grade requires enrollment”

These checks express **business semantics**, even when they appear obvious.

**Rule:**
If validation depends on another field or any system state, it is not application validation.

---

#### ❌ Side-effect or system failures

Examples:

* Persistence errors
* Repository I/O failures
* Transaction failures
* Unexpected runtime exceptions

These are **system failures**, not user input failures.

**Rule:**
Application validation errors are deterministic. If a failure can occur nondeterministically, it does not belong here.

---

#### ❌ Data normalization or automatic repair

Examples:

* Trimming input automatically
* Silently coercing types
* Defaulting missing values

**Rule:**
Application validation rejects invalid input. It does not repair it.

---

## Positive Litmus Test

An error may be an `ApplicationValidationError` **if and only if** all of the following conditions are true:

* ❏ It can be detected without accessing repositories
* ❏ It depends on exactly one input field
* ❏ It is independent of business rules
* ❏ It is deterministic
* ❏ It occurs before any domain object is created

If **any** condition fails, the error is **not** an application validation error.

---

## Enforcement Rules (Non-Negotiable)

* Domain code must **never** import from `application.validation`
* Application validation must **never** catch domain exceptions

If either rule is violated, the architectural boundary has already been breached.

---

## Architectural Outcome

By enforcing this validation model and its boundaries, the system guarantees:

* Validation errors are predictable and structurally consistent
* Domain exceptions retain semantic purity
* Presentation layers (CLI, APIs) remain decoupled from domain internals
* Future APIs gain a stable, enforceable error contract

Any deviation from this document constitutes an **architectural regression**.
