# infrastructure/sqlite/repositories/sqlite_course_repository.py

from __future__ import annotations

import sqlite3
from typing import Iterable

from domain.models.course import Course
from domain.models.student import Student
from domain.models.teacher import Teacher
from domain.repositories.course_repository import CourseRepository

from domain.exceptions.domain_exceptions import (
    EntityNotFoundError,
    DuplicateEntityError,
)
from infrastructure.sqlite.errors import (
    PersistenceError,
    ForeignKeyViolationError,
)

from infrastructure.sqlite.row_mappers.course_rows import course_row_to_primitives
from infrastructure.sqlite.row_mappers.student_rows import student_row_to_primitives
from infrastructure.sqlite.row_mappers.teacher_rows import teacher_row_to_primitives


class SQLiteCourseRepository(CourseRepository):
    """
    SQLite Course Repository — Phase 3

    This repository is governed by an authoritative SQL contract:
        SQLite Course Repository — SQL Contract (Phase 3, Revised)

    Rules (binding):
    - Interacts ONLY with the following tables:
        - courses
        - teachers
        - students
        - enrollments
    - Executes ONLY the SQL statements defined in the contract
    - All SELECT statements that are consumed by row mappers MUST alias
      columns exactly as required by those mappers
    - Identifier-only SELECTs (e.g. list_all step 1) MUST project identity
      columns only, MUST NOT be passed through row mappers, and MUST delegate
      full aggregate reconstruction to get(identity)
    - Full aggregate reconstruction MUST delegate to get(identity)
    - Aggregate reconstruction MUST use domain methods only
    - Grade restoration MUST use Student.assign_grade after enrollment
    - No upserts, no workflow logic, no validation
    - Persistence errors only (no domain exception handling)

    Any deviation requires explicit architectural review.
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    # ------------------------------------------------------------------
    # add(course)
    # ------------------------------------------------------------------
    def add(self, course: Course) -> None:
        # Insert course (duplicate course_code -> DuplicateEntityError)
        try:
            self._connection.execute(
                """
                INSERT INTO courses (course_code, name, teacher_id)
                VALUES (?, ?, ?)
                """,
                (
                    course.code,
                    course.name,
                    course.teacher.id if course.teacher else None,
                ),
            )
        except sqlite3.IntegrityError as exc:
            msg = str(exc).lower()

            # Duplicate course identity -> state semantics
            if "unique constraint failed: courses.course_code" in msg:
                raise DuplicateEntityError(str(exc)) from exc

            # Invalid teacher reference -> persistence semantics
            if "foreign key constraint failed" in msg:
                raise ForeignKeyViolationError(str(exc)) from exc

            raise PersistenceError(str(exc)) from exc

        except sqlite3.Error as exc:
            raise PersistenceError(str(exc)) from exc

        # Insert enrollments (0..N)
        try:
            for student in course.students:
                grade = student.get_grade(course)
                self._connection.execute(
                    """
                    INSERT INTO enrollments (course_code, student_id, grade)
                    VALUES (?, ?, ?)
                    """,
                    (course.code, student.id, grade),
                )
        except sqlite3.IntegrityError as exc:
            msg = str(exc).lower()
            if "unique constraint failed: enrollments.course_code" in msg:
                raise DuplicateEntityError(str(exc)) from exc

            # Missing student or course reference
            if "foreign key constraint failed" in msg:
                raise ForeignKeyViolationError(str(exc)) from exc

            raise PersistenceError(str(exc)) from exc

        except sqlite3.Error as exc:
            raise PersistenceError(str(exc)) from exc

    # ------------------------------------------------------------------
    # get(course_code)
    # ------------------------------------------------------------------
    def get(self, course_code: str) -> Course:
        try:
            cursor = self._connection.execute(
                """
                SELECT
                    c.course_code AS course_code,
                    c.name AS course_name,
                    c.teacher_id AS course_teacher_id
                FROM courses c
                WHERE c.course_code = ?
                """,
                (course_code,),
            )
            course_row = cursor.fetchone()
        except sqlite3.Error as exc:
            raise PersistenceError(str(exc)) from exc

        if course_row is None:
            raise EntityNotFoundError(f"Course not found: {course_code}")

        course_primitives = course_row_to_primitives(course_row)

        # 1) Instantiate aggregate root
        course = Course(
            code=course_primitives["course_code"],
            name=course_primitives["course_name"],
        )

        # 2) Restore teacher (optional)
        teacher_id = course_primitives["course_teacher_id"]
        if teacher_id is not None:
            try:
                cursor = self._connection.execute(
                    """
                    SELECT
                        t.teacher_id AS teacher_id,
                        t.name AS teacher_name
                    FROM teachers t
                    WHERE t.teacher_id = ?
                    """,
                    (teacher_id,),
                )
                teacher_row = cursor.fetchone()
            except sqlite3.Error as exc:
                raise PersistenceError(str(exc)) from exc

            if teacher_row is None:
                raise PersistenceError(
                    f"Teacher '{teacher_id}' referenced by course "
                    f"'{course.code}' not found."
                )

            teacher_primitives = teacher_row_to_primitives(teacher_row)
            teacher = Teacher(
                teacher_id=teacher_primitives["teacher_id"],
                name=teacher_primitives["teacher_name"],
            )

            course.assign_teacher(teacher)

        # 3) Restore enrollments and grades
        try:
            cursor = self._connection.execute(
                """
                SELECT
                    s.student_id AS student_id,
                    s.name AS student_name,
                    e.grade AS grade
                FROM enrollments e
                JOIN students s ON s.student_id = e.student_id
                WHERE e.course_code = ?
                ORDER BY s.student_id
                """,
                (course.code,),
            )
            rows = cursor.fetchall()
        except sqlite3.Error as exc:
            raise PersistenceError(str(exc)) from exc

        for row in rows:
            primitives = student_row_to_primitives(row)

            student = Student(
                student_id=primitives["student_id"],
                name=primitives["student_name"],
            )

            course.enroll(student)

            # Grade is enrollment-owned state, not student-owned primitives
            grade = row["grade"]
            if grade is not None:
                student.assign_grade(course, grade)

        return course

    # ------------------------------------------------------------------
    # remove(course_code)
    # ------------------------------------------------------------------
    def remove(self, course_code: str) -> None:
        try:
            cursor = self._connection.execute(
                """
                DELETE FROM courses
                WHERE course_code = ?
                """,
                (course_code,),
            )
        except sqlite3.Error as exc:
            raise PersistenceError(str(exc)) from exc

        if cursor.rowcount == 0:
            raise EntityNotFoundError(f"Course not found: {course_code}")

    # ------------------------------------------------------------------
    # list_all()
    # ------------------------------------------------------------------
    def list_all(self) -> Iterable[Course]:
        try:
            cursor = self._connection.execute(
                """
                SELECT
                   c.course_code AS course_code
                FROM courses c
                ORDER BY c.course_code
                """
            )
            rows = cursor.fetchall()
        except sqlite3.Error as exc:
            raise PersistenceError(str(exc)) from exc

        for row in rows:
            # Identifier-only row; MUST delegate to get()
            yield self.get(row["course_code"])


