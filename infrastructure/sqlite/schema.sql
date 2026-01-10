-- ============================================================
-- Student Management System — Reference Relational Schema
-- ============================================================
-- This schema is the authoritative relational representation
-- of the SMS domain model.
--
-- It MUST remain aligned with:
--   - domain_model.md
--   - relational_mapping.md
--
-- Any deviation is a breaking architectural change.
-- ============================================================


-- ------------------------------------------------------------
-- 1. Students
-- ------------------------------------------------------------
-- Domain entity: Student
-- Identity: student_id
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS students (
    student_id VARCHAR(64) PRIMARY KEY,
    name       VARCHAR(255) NOT NULL
);


-- ------------------------------------------------------------
-- 2. Teachers
-- ------------------------------------------------------------
-- Domain entity: Teacher
-- Identity: teacher_id
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS teachers (
    teacher_id VARCHAR(64) PRIMARY KEY,
    name       VARCHAR(255) NOT NULL
);


-- ------------------------------------------------------------
-- 3. Courses
-- ------------------------------------------------------------
-- Domain entity: Course (AGGREGATE ROOT)
-- Identity: course_code
-- Teacher assignment is owned by Course
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS courses (
    course_code VARCHAR(64) PRIMARY KEY,
    name         VARCHAR(255) NOT NULL,

    -- Nullable by domain rule: a course may be unassigned
    teacher_id  VARCHAR(64) NULL,

    CONSTRAINT fk_courses_teacher
        FOREIGN KEY (teacher_id)
        REFERENCES teachers (teacher_id)
        ON DELETE SET NULL
);


-- ------------------------------------------------------------
-- 4. Enrollments
-- ------------------------------------------------------------
-- Domain concept: Enrollment (Course ↔ Student)
-- Owned by Course
-- Also owns Grade (embedded attribute)
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS enrollments (
    course_code VARCHAR(64) NOT NULL,
    student_id  VARCHAR(64) NOT NULL,

    -- Grade is not an entity; it exists only via enrollment
    grade       DECIMAL(4,2) NULL,

    CONSTRAINT pk_enrollments
        PRIMARY KEY (course_code, student_id),

    CONSTRAINT fk_enrollments_course
        FOREIGN KEY (course_code)
        REFERENCES courses (course_code)
        ON DELETE CASCADE,

    CONSTRAINT fk_enrollments_student
        FOREIGN KEY (student_id)
        REFERENCES students (student_id)
        ON DELETE CASCADE,

    -- Optional domain-aligned constraint (may vary by DB engine)
    CONSTRAINT chk_grade_range
        CHECK (
            grade IS NULL
            OR (grade >= 0.0 AND grade <= 10.0)
        )
);


-- ------------------------------------------------------------
-- 5. Indexes (Performance, Non-Behavioral)
-- ------------------------------------------------------------
-- Indexes MUST NOT encode business meaning.
-- ------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_courses_teacher
    ON courses (teacher_id);

CREATE INDEX IF NOT EXISTS idx_enrollments_student
    ON enrollments (student_id);

CREATE INDEX IF NOT EXISTS idx_enrollments_course
    ON enrollments (course_code);


-- ------------------------------------------------------------
-- 6. Explicit Non-Features (Documented by Absence)
-- ------------------------------------------------------------
-- The following are INTENTIONALLY NOT PRESENT:
--
-- - No grades table
-- - No student_teacher relationship
-- - No triggers
-- - No stored procedures
-- - No denormalized summary tables
--
-- All business behavior is enforced in the domain layer.
-- ------------------------------------------------------------
