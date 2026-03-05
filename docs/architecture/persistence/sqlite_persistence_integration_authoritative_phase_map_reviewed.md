# SQLite Persistence Integration — Authoritative Phase Map (Reviewed)

This document is the **merged, authoritative phase map** for SQLite persistence integration in the Student Management System (SMS).

It incorporates:
- The original canonical phase map
- The subsequent architectural review
- All accepted corrections, guardrails, and refinements

This document is **normative**. Deviations require explicit architectural justification.

---

## Phase 0 — Foundation (Completed)

**Status:** ✅ Completed

### Purpose
Establish the transactional and error-handling backbone for all persistence.

### Deliverables
- `infrastructure/sqlite/connection.py`
- `infrastructure/sqlite/errors.py`
- `infrastructure/sqlite/unit_of_work.py`

### Guarantees
- Exactly one SQLite connection per use case
- Explicit ownership of BEGIN / COMMIT / ROLLBACK
- Rollback on **any** exception (not only SQLite errors)
- Centralized persistence error taxonomy
- No transaction logic exposed to repositories or application services

### Non‑Responsibilities
- No persistence logic in application services
- No transaction control in repositories

This phase is a **hard prerequisite** for all others.

---

## Phase 1 — SQLite Schema & Bootstrap

**Status:** ⏭ Next

### Purpose
Define and initialize the physical database structure in a deterministic, infrastructure-only manner.

### Deliverables
- `infrastructure/sqlite/schema.sql`
- `infrastructure/sqlite/bootstrap.py`

### Responsibilities
- Define all tables, primary keys, foreign keys, and uniqueness constraints
- Enforce mandatory SQLite pragmas:
  - `journal_mode = WAL`
  - `foreign_keys = ON`
  - `busy_timeout = <configured>`
- Provide **idempotent** schema initialization

### Guardrails (Normative)
- Schema SQL SHOULD be a verbatim copy of `reference_schema.sql`
- Any deviation requires explicit review and justification
- Prevents silent drift (indexes, NOT NULL tweaks, constraint changes)

### Explicit Non‑Responsibilities
- No domain imports
- No repository imports
- No application logic
- No migrations or version branching

### Outcome
A database that is always in a known-correct state before any UnitOfWork begins.

---

## Phase 2 — Row Mappers (Primitive‑Only, Lossy)

**Status:** Planned

### Purpose
Provide a controlled translation layer between raw SQL rows and repository reconstruction logic.

### Deliverables
```
infrastructure/sqlite/row_mappers/
  ├── student_rows.py
  ├── teacher_rows.py
  └── course_rows.py
```

### Rules
- Input: `sqlite3.Row`
- Output: primitive structures only (`dict`, tuples)
- No domain entities
- No constructor-shaped data
- No defaults, inference, or relationship assembly

### Additional Guardrails
- Row mappers must be **total but not validating**
- Missing or malformed columns MUST raise immediately
- No silent coercion or fallback values

### Outcome
Row mappers remain dumb and lossy, preventing hidden factories or domain coupling.

---

## Phase 3 — Repository Implementations

**Status:** Planned

### Purpose
Implement persistence behind domain repository interfaces while preserving domain authority.

### Deliverables
```
infrastructure/sqlite/repositories/
  ├── sqlite_student_repository.py
  ├── sqlite_teacher_repository.py
  └── sqlite_course_repository.py
```

### General Repository Rules
- Accept a transaction-bound connection from UnitOfWork
- Never open or close connections
- Never manage transactions
- Explicitly map SQLite exceptions to repository/state errors only

### StudentRepository / TeacherRepository
- Shallow CRUD only
- No relationship loading
- No business logic

### CourseRepository (Aggregate Root)
- Load full aggregate (Course + Teacher + Students)
- Rebuild relationships using **domain methods only**
- Aggregate state is authoritative on save

### Critical Precision Rule
- Repositories MUST NOT call domain mutator methods **except during aggregate reconstruction**
- Reconstruction is allowed only to reach a previously valid state
- Repositories must never become workflow engines

---

## Phase 4 — Infrastructure Contract Tests

**Status:** Planned

### Purpose
Verify persistence correctness independently of business logic.

### Deliverables
```
tests/infrastructure/sqlite/
  ├── test_student_repository_contract.py
  ├── test_teacher_repository_contract.py
  └── test_course_repository_contract.py
```

### Rules
- Same contract tests must run against:
  - In-memory repositories
  - SQLite repositories
- Fresh schema per test scope
- Assert persistence/state semantics only
- No business-rule assertions

### Outcome
Persistence correctness without changing existing system tests.

---

## Phase 5 — Composition Root Wiring

**Status:** Planned

### Purpose
Integrate SQLite persistence as a drop-in implementation detail.

### Deliverables
- Updated `create_sms()` composition root
- Conditional wiring for SQLite repositories
- UnitOfWork creation hidden from application layer

### Hard Rules
- In-memory repositories remain the default
- SQLite is opt-in via configuration
- No configuration flag may alter application service behavior
- Persistence choice affects wiring only

### Outcome
Application services remain persistence-agnostic and stable.

---

## Phase 6 — System Verification

**Status:** Final

### Purpose
Confirm SQLite persistence is a true drop-in replacement.

### Success Criteria
- All existing system tests pass unchanged
- CLI behavior is identical
- Error semantics are preserved

### Outcome
A fully persistent SMS with zero architectural drift.

---

## Canonical Execution Rule

> **Never advance to the next phase until the current phase is implemented, reviewed, and committed.**

SQLite persistence is a high-risk area for silent architectural erosion. This rule is binding and non-negotiable.

