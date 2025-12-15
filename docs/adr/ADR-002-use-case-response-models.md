# ADR-002: Use-Case Response Models

## Status

Accepted

---

## Context

The Student Management System follows Clean Architecture and Domain-Driven Design principles.

As the system evolved, it became clear that returning **domain entities** from application services caused several issues:

* Accidental domain mutation from outer layers
* Implicit coupling between domain internals and presentation logic
* Difficulty enforcing architectural boundaries

DTOs alone were insufficient because they represent **data shape**, not **use-case intent**.

---

## Decision

Application services SHALL return **Response Models** instead of domain entities or DTOs.

Response Models:

* Represent the **outcome of a specific use case**
* Are immutable snapshots of state at a point in time
* Contain only primitives and immutable collections
* Never reference domain entities

---

## Immutability Semantics

Response Models are implemented as **frozen dataclasses**:

```python
@dataclass(frozen=True, slots=True)
```

### Deep Immutability

* Lists are converted to `tuple`
* Dictionaries are wrapped with `MappingProxyType`

This guarantees:

* No external mutation
* Snapshot behavior
* Predictable system boundaries

---

## Exception Semantics (Explicitly Accepted)

The system intentionally relies on **native Python exception semantics** to enforce immutability.

| Invalid Operation      | Raised Exception      | Reason                       |
| ---------------------- | --------------------- | ---------------------------- |
| Attribute reassignment | `FrozenInstanceError` | Dataclass-level immutability |
| Tuple mutation attempt | `AttributeError`      | No mutation API exists       |
| MappingProxy write     | `TypeError`           | Write forbidden              |

These differences are **not normalized**.

### Rationale

* Preserves Python idioms
* Avoids custom mutation guards
* Makes failure modes explicit and debuggable
* Keeps Response Models minimal and transparent

Tests assert these behaviors intentionally.

---

## Tooling and Testing Considerations

Negative tests intentionally violate immutability.

To remain compatible with static analysis tools (e.g., PyCharm), tests use dynamic mutation attempts:

```python
setattr(response, "field", value)
```

This avoids false-positive IDE errors while preserving runtime correctness.

---

## Consequences

### Positive

* Clear application boundary
* Safer external contracts
* Improved test reliability
* Easier future migration (e.g., Pydantic)

### Trade-offs

* Multiple exception types for immutability violations
* Slightly more verbose response model constructors

These trade-offs are accepted as intentional and beneficial.

---

## Next Steps

With this ADR in place, Phase 3 will refactor application services so that:

* Domain entities never escape the Application layer
* All outward-facing results are expressed via Response Models

This ADR MUST be revisited if response models become mutable or if Python immutability semantics change.
