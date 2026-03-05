# Canonical SQLite Persistence Plan

This document is the **authoritative persistence strategy** for integrating SQLite into the Student Management System (SMS), resulting from merging the original SMS Architect plan with the refinements from the RDB Persistence Architect review.

It is **normative**: deviations should be treated as architectural violations unless explicitly justified.

---

## 1. Architectural Goals (Locked)

The persistence layer must:

* Preserve **Domain purity** (no SQL, no DB concepts in domain models)
* Respect **Clean Architecture boundaries**
* Enforce **aggregate consistency** (Course is the aggregate root)
* Be **swappable** (SQLite ↔ In-memory ↔ future DBs)
* Be **test-safe and incremental**
* Handle SQLite-specific constraints correctly

SQLite is an **implementation detail**, not a design driver.

---

## 2. High-Level Principles (Non-Negotiable)

1. **Domain Layer**

   * Persistence-agnostic
   * Owns business invariants and bidirectional relationships

2. **Application Layer**

   * Transaction-agnostic
   * Validation and orchestration only
   * Depends only on repository interfaces

3. **Infrastructure Layer**

   * Owns persistence, transactions, and DB error translation
   * Implements repository interfaces

4. **Repositories**

   * Are the *only* persistence boundary
   * Never mutate domain internals directly
   * Never manage transactions

---

## 3. Canonical Infrastructure Structure

```
infrastructure/
└── sqlite/
    ├── __init__.py
    ├── connection.py          # low-level helpers (PRAGMA, row_factory)
    ├── unit_of_work.py        # owns connection + transaction lifecycle
    ├── repositories/
    │   ├── sqlite_student_repository.py
    │   ├── sqlite_teacher_repository.py
    │   └── sqlite_course_repository.py
    └── row_mappers/
        ├── __init__.py
        ├── student_rows.py
        ├── teacher_rows.py
        └── course_rows.py
```

---

## 4. Unit of Work (Authoritative Concept)

### Purpose

The **UnitOfWork** is the *only* component allowed to:

* Open and close SQLite connections
* Start, commit, and roll back transactions
* Enforce one-transaction-per-use-case semantics
* Select the **transaction start mode** (read vs write)

### Rules

* One **application service method invocation** = one UnitOfWork
* Repositories **assume** an active transaction
* Repositories must **never** call BEGIN / COMMIT / ROLLBACK
* **Repositories must not open or close database connections**
* **Repositories must never choose or influence the transaction mode**
* Connections and cursors are treated as externally owned and opaque
* No nested transactions (SQLite limitation)

Transaction start semantics (SQLite-specific, locked):

* Read-only UnitOfWork → `BEGIN` (deferred)
* Write UnitOfWork → `BEGIN IMMEDIATE`

The Application layer remains **transaction-agnostic**.

---

## 5. Repository Responsibilities

### General Rules (All Repositories)

* Implement domain repository interfaces exactly
* Accept a transaction-bound connection or cursor
* Translate SQLite errors → domain/state exceptions
* Never perform validation (already done at application boundary)

---

### StudentRepository (SQLite)

Responsibilities:

* `add(student)` → insert student row
* `get(student_id)` → load *student only* (no courses)
* `remove(student_id)` → delete student
* `list_all()` → shallow list

Notes:

* Enrollment is **not** handled here
* No relationship loading

---

### TeacherRepository (SQLite)

Responsibilities mirror StudentRepository:

* Shallow persistence and retrieval only
* No course graph construction

---

### CourseRepository (SQLite) — Aggregate Root

Responsibilities:

* Persist Course entities
* Load **full aggregate**:

  * Course
  * Assigned Teacher (if any)
  * Enrolled Students
* Rebuild relationships using **domain methods only**:

  * `course.assign_teacher(teacher)`
  * `course.enroll(student)`
* Remove course with proper cleanup

Rule:

> If relationships are required, they are loaded via CourseRepository.

---

## 6. Row Mapper Rules (Strict)

Row mappers are **intentionally limited**.

### Allowed

* Map a single DB row → primitive structure (`dict`, tuple)
* Rename columns
* Normalize DB-specific naming

### Forbidden

* Constructing domain entities
* Calling domain methods
* Encoding business logic
* Creating partial aggregates
* Returning data structures shaped to be directly fed into aggregate constructors

Example:

```python
# GOOD
{"student_id": row["student_id"], "name": row["name"]}

# BAD
Student(row["student_id"], row["name"])
```

Aggregate construction belongs **only** in repositories.

---

## 7. Aggregate Reconstruction Rule

All aggregate reconstruction must:

1. Load rows via SQL
2. Convert rows → primitives (row mappers)
3. Construct domain entities via constructors
4. Rebuild relationships **only through domain methods**

This guarantees:

* Invariants always execute
* Bidirectional consistency
* Future domain evolution safety

---

## 8. Error Translation Policy

### Rule

SQLite errors must **never** leak beyond the infrastructure layer.

### Translation Location

* **Repository implementations only**

### Canonical Error Taxonomy

Repositories must translate low-level SQLite failures into a **stable, minimal exception set**:

* `DuplicateEntityError` — UNIQUE constraint violation on insert
* `EntityNotFoundError` — missing row during `get()` or `remove()` of a known identifier
* `ConcurrentUpdateError` — database locked / busy timeout exceeded
* `PersistenceError` — unexpected or unclassified persistence failure

### Clarification: `EntityNotFoundError`

`EntityNotFoundError` applies **only** when:

* A repository is asked to retrieve or remove an entity by identifier, and
* The identifier is structurally valid, but
* No corresponding row exists in persistence

It must **not** be used for:

* Application-level validation failures
* Domain invariant violations
* Cross-entity or relational errors

### Examples

* `sqlite3.IntegrityError (UNIQUE)` → `DuplicateEntityError`
* `sqlite3.IntegrityError (FK)` → persistence/state error (never domain)
* `OperationalError: database is locked` → `ConcurrentUpdateError`

Never translate errors in:

* Domain layer
* Application services
* CLI

---

## 9. Transaction Granularity

| Operation Type               | Transaction Scope  |
| ---------------------------- | ------------------ |
| Add / Get / List             | Single transaction |
| Enrollment / Assignment      | Single transaction |
| Remove Course (with cleanup) | Single transaction |

Hard rule:

> A repository method may not start a transaction if one is already active.

---

## 10. Testing Strategy (Mandatory)

1. **Repository Contract Tests**

   * Same behavioral tests as in-memory repositories
   * Run against a temporary SQLite DB

2. **System Tests**

   * Existing system tests must pass unchanged
   * Only repository implementation swapped

If tests fail, the persistence layer is incorrect — not the tests.

---

## 11. CLI Integration

* CLI remains stateless
* `create_sms()` becomes the composition root
* UnitOfWork created per command
* SQLite repositories injected

No CLI logic changes required.

---

## 11. SQLite Operational Constraints (Locked)

The following constraints are **authoritative** for all SQLite usage in this system:

* `PRAGMA journal_mode = WAL;` must be executed for the database

  * This operation is **idempotent** and **database-wide**
  * It is safe to execute on each connection
* `PRAGMA foreign_keys = ON;` must be executed for every connection
* `PRAGMA busy_timeout = <configured ms>;` must be executed for every connection
* Exactly **one SQLite connection per UnitOfWork**
* No connection pooling
* No shared or global connections
* No cross-thread connection sharing
* No long-running UnitOfWork instances

These rules exist to prevent corruption, deadlocks, and undefined concurrency behavior.

---

## 12. Final Outcome

When implemented correctly, this plan yields:

* A fully persistent SMS
* Strict Clean Architecture compliance
* Domain invariants always enforced
* SQLite used as a replaceable detail
* Zero test rewrites
* Clear upgrade path to other databases or APIs

---

## 13. Canonical Next Step

**Design and implement `UnitOfWork` first.**

All repository and transaction semantics depend on it.
