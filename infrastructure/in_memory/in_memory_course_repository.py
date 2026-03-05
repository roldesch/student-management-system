# infrastructure/in_memory/in_memory_course_repository.py

from __future__ import annotations
from typing import Iterable, Optional

from domain.models.course import Course
from domain.models.student import Student
from domain.models.teacher import Teacher
from domain.repositories.course_repository import CourseRepository
from domain.exceptions.domain_exceptions import (
    DuplicateEntityError,
    EntityNotFoundError,
)

from infrastructure.sqlite.errors import PersistenceError

from infrastructure.in_memory.in_memory_store import (
    InMemoryStore,
    CourseSnapshot,
    EnrollmentSnapshot,
)


class InMemoryCourseRepository(CourseRepository):
    """
    In-memory implementation of CourseRepository with detached semantics.

    Parity with SQLite CourseRepository.get():
      - Reconstructs Course aggregate root
      - Restores optional teacher
      - Restores enrollments and optional grades
      - Uses domain methods to restore bidirectional links (assign_teacher, enroll, assign_grade)
    """

    def __init__(self, store: InMemoryStore) -> None:
        self._store = store


    def add(self, course: Course) -> None:
        code = course.code

        if code in self._store.courses:
            raise DuplicateEntityError(f"Course '{code}' already exists.")
        self._store.courses[code] = self._to_snapshot(course)


    def get(self, course_code: str) -> Course:
        snap = self._store.courses.get(course_code)

        if snap is None:
            raise EntityNotFoundError(f"Course '{course_code}' not found.")

        return self._from_snapshot(snap)


    def remove(self, course_code: str) -> None:
        if course_code not in self._store.courses:
            raise EntityNotFoundError(f"Course '{course_code}' not found.")
        del self._store.courses[course_code]


    def list_all(self) -> Iterable[Course]:
        return tuple(self._from_snapshot(s) for s in self._store.courses.values())


    def update(self, course: Course) -> None:
        course_code = course.code
        if course_code not in self._store.courses:
            raise EntityNotFoundError(f"Course '{course_code}' not found.")
        self._store.courses[course_code] = self._to_snapshot(course)


    # Test utility - not part of domain interface
    def clear(self) -> None:
        self._store.courses.clear()


    def _from_snapshot(self, snap: CourseSnapshot) -> Course:
        # 1) Instantiate aggregate root
        course = Course(code=snap.code, name=snap.name)

        # 2) Restore teacher (optional)
        if snap.assigned_teacher_id is not None:
            teacher_snap = self._store.teachers.get(snap.assigned_teacher_id)
            if teacher_snap is None:
                raise PersistenceError(
                    f"Teacher '{snap.assigned_teacher_id}' referenced by course "
                    f"'{course.code}' not found."
                )

            teacher = Teacher(
                teacher_id=teacher_snap.teacher_id,
                name=teacher_snap.name,
            )
            course.assign_teacher(teacher)

        # 3) Restore enrollments and grades
        for enrollment in snap.enrollments:
            student_snap = self._store.students.get(enrollment.student_id)
            if student_snap is None:
                raise PersistenceError(
                    f"Student '{enrollment.student_id}' referenced by course "
                    f"'{course.code}' not found."
                )

            student = Student(
                student_id=student_snap.student_id,
                name=student_snap.name,
            )

            course.enroll(student)

            if enrollment.grade is not None:
                student.assign_grade(course, enrollment.grade)

        return course


    @staticmethod
    def _to_snapshot(course: Course) -> CourseSnapshot:
        teacher_id: Optional[str] = course.teacher.id if course.teacher is not None else None

        enrollments: list[EnrollmentSnapshot] = []
        for student in course.students:
            grade = student.get_grade(course)
            enrollments.append(
                EnrollmentSnapshot(
                    student_id=student.id,
                    grade=grade,
                )
            )

        return CourseSnapshot(
            code=course.code,
            name=course.name,
            assigned_teacher_id=teacher_id,
            enrollments=tuple(enrollments),
        )


