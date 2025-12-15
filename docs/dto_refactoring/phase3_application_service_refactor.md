# Phase 3 — Application Service Refactor

## Purpose of Phase 3

Phase 3 completes the DTO boundary refactoring by enforcing a **hard application boundary**:

> **No domain entity may escape the Application layer.**

All outward-facing operations of the application now return **Response Models**, primitives, or `None`.

This phase refactors the `StudentManagementSystem` service to become the **single orchestration point** between:

* Domain entities (internal)
* DTOs (internal, transitional)
* Response Models (external contract)

---

## Architectural Rule Introduced

### Boundary Rule (Authoritative)

* Domain models (`Student`, `Teacher`, `Course`) are **never returned** by application services
* Application services return only:

  * Response Models
  * Primitive values (`float | None`)
  * `None` for command-style use cases

This rule is enforced by:

* Type signatures
* Tests
* Service implementation structure

---

## Refactoring Strategy

### Step 1 — Internalize Domain Access

All access to repositories returning domain entities was moved to **private helper methods**:

```python
_get_student_entity(...)
_get_teacher_entity(...)
_get_course_entity(...)
```

This prevents accidental exposure of domain entities from public methods.

---

### Step 2 — Introduce Explicit Mapping at the Boundary

Each public query method applies the same pipeline:

```
Domain Entity
   ↓
DTO Mapper (Phase 2)
   ↓
Response Model (immutable snapshot)
```

Mapping is performed **after domain logic completes**, ensuring:

* No mutation occurs during mapping
* Response Models represent a stable snapshot

---

### Step 3 — Refactor Public Service Methods

Public methods were classified and refactored accordingly:

#### Query — Single

* `get_student`
* `get_teacher`
* `get_course`

Return a single Response Model.

#### Query — Collection

* `list_students`
* `list_teachers`
* `list_courses`

Return `tuple[ResponseModel, ...]`.

#### Commands

* Enrollment, assignment, removal, grading

Return `None` and expose effects only through subsequent queries.

#### Primitive Query

* `get_student_grade`

Returns `float | None`, which is already boundary-safe.

---

## Testing Impact

### System Tests

System tests were refactored to:

* Assert only against **Response Model fields**
* Re-query the service to observe side effects
* Avoid all domain inspection (`.courses`, `.students`, `.teacher`)

This ensures tests validate **observable behavior**, not internal structure.

---

## Outcome of Phase 3

At the end of Phase 3:

* The Application layer has a clean, enforced boundary
* Domain invariants remain fully enforced
* DTOs are internal and replaceable
* Response Models define the stable outward contract

This completes the DTO boundary refactor.

---

## Readiness for Next Phases

With Phase 3 complete, the system is prepared for:

* Phase 4: CLI / UI / API integration
* Migration to Pydantic or other serialization frameworks
* External API exposure without domain leakage

The boundary is now explicit, tested, and documented.
