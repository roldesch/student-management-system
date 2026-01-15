# 🔒 Locked SQL Contract

## SQLite Course Repository — SQL Contract

**Phase:** 3 — Repository Implementations  
**Repository Type:** Aggregate Root Repository  
**Aggregate Authority:** ✅ Course is the aggregate root  
**Relationship Awareness:** ✅ Required (Course ↔ Teacher, Course ↔ Students)

Enrollment state (grade) is persisted and restored as opaque aggregate state.

Governs: `sqlite_course_repository` (infrastructure layer)

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

This scope is enforced by this SQL contract.

---

## 1. Row Mapper Compatibility Contract

All `SELECT` statements **MUST alias columns exactly** as required by:

```python
course_row_to_primitives(row)
teacher_row_to_primitives(row)
student_row_to_primitives(row)
```

The row-mapper contract is considered **downstream of this document**.  
Any change to alias requirements **requires updating this contract first**.

### Required Aliases (Frozen)

#### Course base row
| Alias Name | Source Column |
|-----------|---------------|
| `course_code` | `courses.course_code` |
| `course_name` | `courses.name` |
| `teacher_id` | `courses.teacher_id` |

#### Teacher row
| Alias Name | Source Column |
|-----------|---------------|
| `teacher_id` | `teachers.teacher_id` |
| `teacher_name` | `teachers.name` |

#### Student enrollment row (with grade)
| Alias Name | Source Column |
|-----------|---------------|
| `student_id` | `students.student_id` |
| `student_name` | `students.name` |
| `grade` | `enrollments.grade` |

Failure to alias exactly is a **repository bug**, not a mapper issue.

---

## 2. Aggregate Reconstruction Contract (Binding)

When loading a Course aggregate, reconstruction **MUST occur only via domain methods** and **must fully restore historical state**, including grades.

Reconstruction order is fixed:

1. Instantiate the aggregate
   ```python
   course = Course(course_code, course_name)
   ```

2. If a teacher exists:
   ```python
   course.assign_teacher(teacher)
   ```

3. For each enrolled student:
   ```python
   course.enroll(student)
   if grade is not None:
       course.assign_grade(student, grade)
   ```

The repository **MUST NOT**:

* Mutate internal fields directly
* Call protected methods on Student or Teacher
* Bypass domain invariants
* Suppress domain exceptions

If domain invariants fail during reconstruction, this indicates a **persistence integrity failure**, not a business-rule violation.

---

## 3. SQL — `add(course)`

### Purpose
Persist a **new** Course aggregate, including teacher assignment and enrollments with grades.

### Locked SQL

#### Insert course
```sql
INSERT INTO courses (course_code, name, teacher_id)
VALUES (?, ?, ?)
```

#### Insert enrollments (0..N)
```sql
INSERT INTO enrollments (course_code, student_id, grade)
VALUES (?, ?, ?)
```

### Guarantees

* Course is authoritative for all relationships
* No inference or defaults
* Duplicate identity handled by database constraints

### Explicitly Forbidden

* `INSERT OR IGNORE`
* `ON CONFLICT`
* Pre-insert existence checks
* Business-driven upsert logic

---

## 4. SQL — `get(course_code)`

### Purpose
Retrieve a **fully reconstructed** Course aggregate, including teacher, students, and grades.

### Locked SQL

#### Load course
```sql
SELECT
    c.course_code AS course_code,
    c.name        AS course_name,
    c.teacher_id  AS teacher_id
FROM courses c
WHERE c.course_code = ?
```

#### Load teacher (optional)
```sql
SELECT
    t.teacher_id AS teacher_id,
    t.name       AS teacher_name
FROM teachers t
WHERE t.teacher_id = ?
```

#### Load enrolled students with grades
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

**Constraint:** The repository MUST NOT filter, sort, or conditionally load based on grade values. Grade is treated as opaque aggregate state.

### Explicitly Forbidden

* Additional joins
* Business filters
* `LIMIT`
* Partial aggregate loading

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

Error types are **infrastructure-level and entity-agnostic**.

| Condition | Repository Responsibility |
|---------|----------------------------|
| Duplicate PK on INSERT | `DuplicateEntityError` |
| Course not found | `EntityNotFoundError` |
| SQLite operational failure | `PersistenceError` |
| Domain invariant violation | ❌ Must not be handled here |

Repositories **must not**:

* Catch or translate domain exceptions
* Perform validation
* Encode business meaning

---

## 8. Contract Status

✅ **LOCKED — Phase 3 Authoritative**

This SQL contract is authoritative for Phase 3.
Any deviation requires explicit architectural review.

