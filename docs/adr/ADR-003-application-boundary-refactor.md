# ADR-003: Application Boundary Refactor

## Status

Accepted

---

## Context

Prior to this decision, application services in the Student Management System returned **domain entities** directly.

This led to:

* Accidental domain mutation from presentation layers
* Tight coupling between domain internals and external consumers
* Difficulty enforcing Clean Architecture boundaries

Phases 1 and 2 introduced DTOs, mappers, and Response Models, but the boundary was not enforced until services were refactored.

---

## Decision

Application services SHALL enforce a **strict boundary**:

* Domain entities are internal only
* Public service methods return:

  * Response Models
  * Primitive values
  * `None` for commands

This decision applies to all current and future application services.

---

## Design Consequences

### Internal Structure

* Services may retrieve domain entities internally via repositories
* Mapping to Response Models occurs **at the boundary**
* DTOs remain an internal translation mechanism

### External Contract

* Consumers observe immutable snapshots
* No consumer can mutate domain state
* Domain model evolution does not break external callers

---

## Testing Implications

System tests were updated to:

* Assert only observable behavior
* Avoid inspecting domain internals
* Validate cleanup and invariants through re-queries

Negative tests for immutability remain at the Response Model level.

---

## Alternatives Considered

### Returning Domain Entities

Rejected due to:

* Boundary leakage
* High coupling
* Unsafe mutation risks

### Returning DTOs Directly

Rejected because:

* DTOs represent data shape, not use-case intent
* DTOs lack semantic meaning for consumers

---

## Trade-offs

### Accepted Costs

* Additional mapping code in services
* More explicit test assertions

### Benefits

* Strong architectural boundary
* Clear separation of concerns
* Safer evolution of the domain model
* Ready for external API exposure

---

## Relationship to Other ADRs

* ADR-001: Introduce DTOs
* ADR-002: Use-Case Response Models

ADR-003 completes the boundary refactor initiated by ADR-001 and ADR-002.

---

## Enforcement

This ADR MUST be revisited if:

* Domain entities are exposed publicly
* Response Models become mutable
* Application services bypass the mapping boundary

Until then, this decision is considered stable and binding.
