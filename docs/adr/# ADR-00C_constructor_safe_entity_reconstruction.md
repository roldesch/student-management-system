# ADR-00C — Constructor-Safe Entity Reconstruction

## Status

Accepted

---

## Context

The Student Management System (SMS) uses repositories in the infrastructure layer to reconstruct domain entities (e.g. `Student`, `Teacher`, `Course`) from persistence.

As SQLite persistence was introduced, a design question emerged:

> Should repositories reconstruct entities using **constructors**, or should the domain expose **explicit reconstitution APIs** (e.g. `reconstitute()` methods) for persistence purposes?

Both approaches are valid in Domain-Driven Design (DDD), but they carry different trade-offs in terms of domain evolution, architectural clarity, and implementation cost.

Previously, this decision was **implicit**, creating the risk of inconsistent assumptions across repositories and future refactors.

This ADR exists to **make the trade-off explicit and binding**, while preserving a documented evolution path.

---

## Decision

### Chosen Policy — Constructor-Safe Entity Reconstruction

The system adopts the following rule:

> **Domain entity constructors MUST remain persistence-safe.**
> Repositories MAY reconstruct domain entities exclusively using constructors, unless superseded by a future ADR.

This decision applies to all current domain entities, including (but not limited to):

* `Student`
* `Teacher`
* `Course`

Repositories are permitted to call entity constructors when reconstructing state from persistence.

---

## Constructor Safety Requirements (Binding)

Under this policy, all domain entity constructors **MUST** adhere to the following constraints.

Constructors **MUST NOT**:

* Perform I/O
* Enforce business rules or domain invariants
* Introduce validation logic that depends on system or persistence state
* Mutate relationships
* Trigger side effects
* Depend on external services or repositories

Constructors **MAY**:

* Assign identity and primitive attributes
* Initialize empty internal collections
* Establish a neutral, persistence-safe baseline state

Business invariants, relationship management, and rule enforcement **remain the exclusive responsibility of domain methods**, not constructors.

Constructors **MAY**:

* Assign identity and primitive attributes
* Initialize empty internal collections
* Establish a neutral, persistence-safe baseline state

Business invariants, relationship management, and rule enforcement **remain the exclusive responsibility of domain methods**, not constructors.

---

## Explicitly Deferred Alternative (Not Rejected)

### Path B — Explicit Reconstitution APIs

An alternative design was considered:

> Domain entities expose explicit reconstitution APIs
> (e.g. `Student.reconstitute(...)`, `Teacher.reconstitute(...)`)
> used exclusively by repositories.

This approach provides stronger separation between:

* Creation semantics
* Persistence reconstruction semantics

However, it requires:

* Domain refactoring
* Consistent adoption across all entities and repositories
* Clear definition of which invariants are bypassed

### Current Status

This alternative is **explicitly deferred**, not rejected.

If future system evolution introduces:

* Complex creation-time invariants
* Multiple construction contexts (APIs, imports, migrations)
* Domain lifecycle complexity that constructors can no longer safely handle

then **Path B MUST be introduced via a dedicated ADR** (e.g. *"Domain Reconstitution APIs"*).

Repositories MUST NOT introduce reconstitution methods ad hoc without such an ADR.

---

## Consequences

### Positive

* Matches the existing codebase and repository implementations
* Avoids premature domain refactoring
* Keeps repository logic simple and consistent
* Removes ambiguity for reviewers and contributors
* Preserves Clean Architecture boundaries

### Trade-offs

* Constructors carry dual responsibility (creation + persistence)
* Requires discipline when evolving domain constructors
* Future refactoring cost increases if deferred too long

These trade-offs are accepted as intentional and appropriate for the current phase of the system.

---

## Enforcement

The following are **architectural violations** under this ADR:

* Adding business rule enforcement to constructors
* Introducing side effects or I/O in constructors
* Mixing relationship management into constructors
* Introducing ad hoc `reconstitute()` methods without a new ADR
* Inconsistent reconstruction strategies across repositories

Any such occurrence must be treated as an architectural defect, not an implementation detail.

---

## Relationship to Other ADRs

This ADR complements and refines:

* ADR-00X — Domain Model Authority and Boundaries
* ADR-00Y — Repository Role and Limitations

It does not override them; it makes an implicit assumption **explicit and enforceable**.

---

## Enforcement Reference

All repository reviews MUST verify compliance with this ADR.

Entity reconstruction in repositories MUST conform to:

* **ADR-00? — Constructor-Safe Entity Reconstruction**

Any deviation requires explicit architectural review.

---

## Summary

This ADR deliberately chooses a **constructor-safe policy** as the current architectural baseline, while documenting a **clean, explicit evolution path** should the domain require stronger lifecycle separation in the future.

> **Explicit trade-offs are safer than implicit drift.**
