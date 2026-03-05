# 🔒 SQLite Course Repository — SQL Contract (Phase 3, Revised)

**Phase:** 3 — Repository Implementations
**Repository Type:** Aggregate Root Repository
**Aggregate Authority:** Course is the aggregate root for enrollment and teacher assignment
**Relationship Awareness:** Required (Course ↔ Teacher, Course ↔ Students)

Enrollment state (including grade) is persisted and restored as **opaque aggregate state**, but grade mutation is **Student-owned** in the current domain model.

This document revises the reconstruction semantics to align the contract with the authoritative domain API, without changing domain code.

---

## 0. Scope Declaration (Binding)

This repository is permitted to interact with **exactly these tables**:

```
courses
teachers
students
enrollments
```

It is **explicitly forbidden** from:

* Accessing any other table
* Encoding business meaning in SQL
* Performing workflow orchestration
* Mutating relationships outside aggregate reconstruction or persistence
* Becoming a substitute for domain logic

---

## 1. Row Mapper Compatibility Contract

All `SELECT` statements that are consumed by row mappers **MUST alias columns exactly** as required by those mappers.

Identifier-only `SELECT` statements used exclusively to obtain aggregate identities
(e.g., the first step of `list_all()`)

* MAY project only identity columns
* MUST NOT be passed through row mappers
* MUST delegate full aggregate reconstruction to `get(identity)`

Failure to alias correctly for mapper-consumed queries is a **repository bug**, not a mapper issue.

---

## 2. Aggregate Reconstruction Contract (Binding)

When loading a Course aggregate, reconstruction **MUST occur only via domain methods** and **MUST fully restore historical state**, including grades.

Reconstruction order is fixed:

1. Instantiate the aggregate root

   ```python
   course = Course(course_code, course_name)
   ```

2. If a teacher exists:

   ```python
   course.assign_teacher(teacher)
   ```

3. For each enrolled student (including grade state):

   ```python
   course.enroll(student)
   if grade is not None:
       student.assign_grade(course, grade)
   ```

### Authority Note (Normative)

Although grade values are conceptually part of enrollment state,
grade mutation is **Student-owned** in the current domain model.

Repositories MUST therefore restore grade state by invoking
`Student.assign_grade(course, value)` **only after** the student
has been enrolled in the course.

Repositories MUST NOT:

* Infer grade semantics
* Validate grade ranges
* Suppress domain exceptions raised during reconstruction

If domain invariants fail during reconstruction, this indicates a **persistence integrity failure**, not a business-rule violation.

---

## 3. SQL — `add(course)`

### Purpose

Persist a **new** Course aggregate, including teacher assignment and enrollments with grades.

### Locked SQL

```sql
INSERT INTO courses (course_code, name, teacher_id)
VALUES (?, ?, ?)
```

```sql
INSERT INTO enrollments (course_code, student_id, grade)
VALUES (?, ?, ?)
```

---

## 4. SQL — `get(course_code)`

### Purpose

Retrieve a **fully reconstructed** Course aggregate, including teacher, students, and grades.

```sql
SELECT
    c.course_code AS course_code,
    c.name        AS course_name,
    c.teacher_id  AS teacher_id
FROM courses c
WHERE c.course_code = ?
```

```sql
SELECT
    t.teacher_id AS teacher_id,
    t.name       AS teacher_name
FROM teachers t
WHERE t.teacher_id = ?
```

```sql
SELECT
    s.student_id AS student_id,
    s.name       AS student_name,
    e.grade      AS grade
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
WHERE e.course_code = ?
ORDER BY s.student_id
```

---

## 5. SQL — `remove(course_code)`

```sql
DELETE FROM courses
WHERE course_code = ?
```

Enrollments are removed via **schema-level cascade**.

---

## 6. SQL — `list_all()`

### Step 1 — list course codes

```sql
SELECT
    c.course_code AS course_code
FROM courses c
ORDER BY c.course_code
```

### Step 2 — for each code, load aggregate using `get(course_code)`

Mega-joins and partial aggregates are **explicitly forbidden**.

---

## 7. Error Semantics (Non-Negotiable)

| Condition                     | Repository Responsibility  |
| ----------------------------- | -------------------------- |
| Duplicate PK on course INSERT | `DuplicateEntityError`     |
| Course not found              | `EntityNotFoundError`      |
| SQLite operational failure    | `PersistenceError`         |
| Domain invariant violation    | ❌ Must not be handled here |

Repositories MUST NOT:

* Catch or translate domain exceptions
* Perform validation
* Encode business meaning

---

## 8. Contract Status

✅ **REVISED — Phase 3 Authoritative**

This revision aligns the SQL contract with the authoritative domain API
while preserving all Phase-3 architectural constraints.
