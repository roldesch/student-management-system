# Locked SQL Contract

## SQLite Teacher Repository — SQL Contract

**Phase:** 3 — Repository Implementations  
**Repository Type:** Shallow CRUD (Non-Aggregate)  
**Aggregate Authority:** ❌ Not an aggregate root  
**Relationship Awareness:** ❌ Forbidden

Governs: `sqlite_teacher_repository` (infrastructure layer)

---

## 0. Scope Declaration (Binding)

This repository is permitted to interact with **exactly one table**:

```
teachers
```

It is **explicitly forbidden** from:

* Joining any other table
* Accessing course / assignment / junction tables
* Loading or inferring relationships
* Encoding business meaning in SQL

This scope is enforced by this SQL contract.

---

## 1. Row Mapper Compatibility Contract

All `SELECT` statements **MUST alias columns exactly** as required by:

```python
teacher_row_to_primitives(row)
```

The row-mapper contract is considered **downstream of this document**.  
Any change to alias requirements **requires updating this contract first**.

### Required Aliases (Frozen)

| Alias Name     | Source Column           |
| -------------- | ----------------------- |
| `teacher_id`   | `teachers.teacher_id`   |
| `teacher_name` | `teachers.name`         |

Failure to alias exactly is a **repository bug**, not a mapper issue.

---

## 2. SQL — `add(teacher)`

### Purpose

Persist a **new** `Teacher` entity.

### Locked SQL

```sql
INSERT INTO teachers (teacher_id, name)
VALUES (?, ?)
```

### Guarantees

* Inserts only teacher-owned fields
* No inference, defaults, or normalization
* Duplicate identity handled by database constraints

### Explicitly Forbidden

* `INSERT OR IGNORE`
* `ON CONFLICT`
* Pre-insert existence checks
* Business-driven upsert logic

---

## 3. SQL — `get(teacher_id)`

### Purpose

Retrieve a **single** `Teacher` by identity.

### Locked SQL

```sql
SELECT
    t.teacher_id AS teacher_id,
    t.name       AS teacher_name
FROM teachers t
WHERE t.teacher_id = ?
```

### Guarantees

* Zero or one row only
* Column aliases match row mapper contract
* No relationship loading
* No derived or computed fields

### Explicitly Forbidden

* `JOIN`
* Course or assignment lookups
* `LIMIT`
* Business filters

---

## 4. SQL — `remove(teacher_id)`

### Purpose

Delete a `Teacher` by identity.

### Locked SQL

```sql
DELETE FROM teachers
WHERE teacher_id = ?
```

### Guarantees

* Single-table operation
* Existence determined by affected row count
* Referential integrity enforced by SQLite

### Explicitly Forbidden

* Cascading deletes in repository code
* Relationship cleanup
* Domain-driven checks

---

## 5. SQL — `list_all()`

### Purpose

Retrieve **all** teachers as independent entities.

### Locked SQL

```sql
SELECT
    t.teacher_id AS teacher_id,
    t.name       AS teacher_name
FROM teachers t
ORDER BY t.teacher_id
```

### Guarantees

* Deterministic ordering
* No filtering, pagination, or joins

### Explicitly Forbidden

* Sorting by business semantics
* Lazy loading
* Relationship hints or joins
* Any SQL not explicitly listed in this document

---

## 6. Error Semantics (Non-Negotiable)

Error types are **infrastructure-level and entity-agnostic**.

| Condition                  | Repository Responsibility    |
| -------------------------- | ---------------------------- |
| Duplicate PK on INSERT     | Raise `DuplicateEntityError` |
| No row on SELECT           | Raise `EntityNotFoundError`  |
| SQLite operational failure | Raise `PersistenceError`     |
| Domain invariant violation | ❌ Must never occur here      |

Repositories **must not**:

* Catch or translate domain exceptions
* Perform validation
* Encode business meaning

---

## 7. Contract Status

✅ **LOCKED — Phase 3 Authoritative**

This SQL contract is authoritative for Phase 3.  
Any deviation requires explicit architectural review.

