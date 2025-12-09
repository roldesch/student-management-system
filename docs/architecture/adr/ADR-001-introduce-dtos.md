
---

## 3️⃣ `docs/architecture/adr/ADR-001-introduce-dtos.md`

```markdown
# ADR-001: Introduce Application-Layer DTOs

## Status

Accepted

## Context

The Student Management System (SMS) currently has:

- A rich Domain Model:
  - `Student`, `Teacher`, `Course` with invariants and bidirectional relationships.
- An Application Service:
  - `StudentManagementSystem` orchestrating use cases.
- In-memory repository implementations.
- A comprehensive automated test suite (domain, integration, system).

However, the Application Service currently **returns domain entities directly**. This leads to:

- Tight coupling between UI/CLI/tests and internal domain structure.
- Risk of accidentally mutating aggregates from outside.
- Fragile public contracts: any domain model refactor can break external consumers.
- Violations of Clean Architecture:
  - Entities (domain) are crossing the application boundary.

We anticipate:

- A CLI interface.
- Possibly a future REST API.
- Ongoing evolution of the domain model.

We need a stable, explicit, and boundary-safe representation of domain state.

## Decision

We will introduce **Application-Layer Data Transfer Objects (DTOs)** implemented as **immutable `@dataclass` types** under:

```text
application/dtos/
