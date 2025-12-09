
---

## 2️⃣ `docs/architecture/dto_refactoring/phase1_dto_design.md`

```markdown
# Phase 1 – Application DTO Design

## 1. Goal

Define and introduce **immutable Application-Layer DTOs** that:

- Represent domain entities (`Student`, `Teacher`, `Course`) in a **flattened** and **boundary-safe** way.
- Contain **only primitive types** and simple collections (`str`, `list`, `dict`, `Optional[...]`).
- Are **immutable** snapshots (`frozen=True`) suitable for UI/CLI/API consumption.
- Do **not** contain any domain behavior or references to domain entities.

No application service behavior changes in this phase.

## 2. Design Principles

### 2.1 Immutable Data

DTOs are implemented as:

```python
@dataclass(frozen=True, slots=True)
class SomeDTO:
    ...
