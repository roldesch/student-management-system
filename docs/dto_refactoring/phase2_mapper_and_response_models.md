# Phase 2 — DTO Mappers and Response Models

## Purpose of Phase 2

Phase 2 establishes the **application boundary** between the Domain layer and any outward-facing consumers (CLI, API, UI, tests).

The goal is to ensure that:

* Domain entities **never escape** the Application layer
* External layers observe **immutable, snapshot-based data**
* Use-case outcomes are represented explicitly and safely

This phase introduces two complementary concepts:

1. **DTO Mappers** — translate Domain → DTO
2. **Response Models** — represent use-case results

---

## DTO Mappers (Recap)

DTO mappers are responsible for:

* Translating rich domain objects into **flattened DTOs**
* Enforcing **one-way dependency** (Domain → Application)
* Preventing accidental leakage of domain behavior

All mapper tests passed prior to completing this phase, confirming:

* Correct shape
* No domain references
* Deterministic output

---

## Response Models

### Why Response Models Exist

DTOs describe **data shape**, not **use-case meaning**.

Response Models exist to:

* Represent the **outcome of a use case**
* Aggregate one or more DTO-derived values
* Serve as the **only return type** of application services

They form the *stable contract* between:

```
Application Layer → Presentation / API / CLI
```

---

## Immutability Contract

Response Models are **deeply immutable snapshots**.

This is a deliberate design choice with several implications:

### Structural Rules

* All response models are implemented as:

```python
@dataclass(frozen=True, slots=True)
```

* Collection fields are stored as:

  * `tuple` instead of `list`
  * `MappingProxyType(dict(...))` instead of `dict`

### Why Deep Immutability Matters

* Prevents accidental mutation by presentation layers
* Guarantees snapshot semantics (no time-based drift)
* Simplifies reasoning about application state
* Enables safe caching and logging

---

## Exception Semantics (Intentional)

Immutability is enforced using **native Python semantics**, not custom guards.

This leads to *different exception types* depending on the invalid operation:

| Operation                                      | Exception             | Rationale                    |
| ---------------------------------------------- | --------------------- | ---------------------------- |
| Rebinding attribute (`response.id = ...`)      | `FrozenInstanceError` | Frozen dataclass enforcement |
| Calling mutation method on tuple (`append`)    | `AttributeError`      | Method does not exist        |
| Mutating mapping proxy (`grades["C01"] = ...`) | `TypeError`           | Write operation forbidden    |

### Why This Is Correct

* Aligns with Python's built-in data model
* Avoids artificial uniformity in exception handling
* Makes failure modes explicit and meaningful

Tests assert these behaviors **deliberately**.

---

## Tooling Considerations

Because response models are frozen, **negative tests** intentionally perform illegal operations.

To avoid false-positive IDE errors (e.g., PyCharm "read-only attribute" warnings), tests use:

```python
setattr(response, "field", value)
```

This preserves runtime behavior while remaining tooling-friendly.

---

## Outcome of Phase 2

At the end of Phase 2:

* DTOs are immutable and domain-safe
* Mappers are deterministic and tested
* Response Models define the application boundary
* Tests encode *true runtime semantics*

This creates a stable foundation for **Phase 3: Application Service Refactor**, where services will return Response Models instead of domain entities.
