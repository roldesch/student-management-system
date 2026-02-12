# tests/infrastructure/sqlite/test_course_repository_contract.py

from __future__ import annotations

import pytest

from domain.models.course import Course
from domain.models.student import Student
from domain.models.teacher import Teacher

from domain.exceptions.domain_exceptions import (
    DuplicateEntityError,
    EntityNotFoundError,
)

from tests.infrastructure.sqlite.conftest import RepositoryHarness


# -----------------------------------------------------------------------------
# Helpers (Phase-4A temporary enforcement)
# -----------------------------------------------------------------------------
def _xfail_memory_noncompliant(repository_harness: RepositoryHarness) -> None:
    """
    Phase-4A: In-memory repositories are known to violate ADR-00Z / ADR-00R
    by raising domain errors instead of repository/state errors.
    This helper makes that explicit without weakening the contract.
    """
    if repository_harness.kind == "memory":
        pytest.xfail(
            "Phase-4A: in-memory repositories not yet contract-compliant (Phase-4B)."
        )


# -----------------------------------------------------------------------------
# CourseRepository Contract Tests
# -----------------------------------------------------------------------------
# Scope:
# - Persistence semantics only
# - Aggregate reconstruction
# - Identity and existence behavior
# - No business rule assertions
# - No ordering guarantees
# -----------------------------------------------------------------------------

def test_course_repository_add_then_get_returns_course_with_same_identity_and_name(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    course = Course(code="C01", name="Math")

    # Act
    with repository_harness.new_scope() as scope:
        scope.courses.add(course)

    with repository_harness.new_scope() as scope:
        loaded = scope.courses.get("C01")

    # Assert
    assert loaded.code == "C01"
    assert loaded.name == "Math"


def test_course_repository_add_existing_course_identity_raises_duplicate_entity_error(
        repository_harness: RepositoryHarness
) -> None:
    # Arrange
    course = Course(code="C01", name="Math")

    with repository_harness.new_scope() as scope:
        scope.courses.add(course)

    _xfail_memory_noncompliant(repository_harness)    # Phase-4A temporary suspension

    # Act / Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises(DuplicateEntityError):
            scope.courses.add(Course(code="C01", name="Math Clone"))


def test_course_repository_get_missing_course_raises_entity_not_found_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    missing_course_code = "C04"

    _xfail_memory_noncompliant(repository_harness)    # Phase-4A temporary suspension

    # Act / Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises(EntityNotFoundError):
            scope.courses.get(missing_course_code)


def test_course_repository_remove_existing_course_then_get_raises_entity_not_found_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    course = Course(code="C01", name="Math")

    with repository_harness.new_scope() as scope:
        scope.courses.add(course)

    # Act
    with repository_harness.new_scope() as scope:
        scope.courses.remove("C01")

    _xfail_memory_noncompliant(repository_harness)    # Phase-4A temporary suspension

    # Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises(EntityNotFoundError):
            scope.courses.get("C01")


def test_course_repository_remove_missing_course_raises_entity_not_found_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    missing_course_code = "C04"

    _xfail_memory_noncompliant(repository_harness)  # Phase-4A temporary suspension

    # Act / Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises(EntityNotFoundError):
            scope.courses.remove(missing_course_code)


def test_course_repository_get_restores_teacher_and_enrollments(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    teacher = Teacher(teacher_id="T01", name="Dr. Smith")
    student = Student(student_id="S01", name="Alice")

    course = Course(code="C01", name="Math")
    course.assign_teacher(teacher)
    course.enroll(student)
    student.assign_grade(course, 9.5)

    with repository_harness.new_scope() as scope:
        scope.teachers.add(teacher)
        scope.students.add(student)
        scope.courses.add(course)

    # Act
    with repository_harness.new_scope() as scope:
        loaded = scope.courses.get("C01")

    # Assert
    assert loaded.teacher is not None
    assert loaded.teacher.id == "T01"

    enrolled_students = {s.id for s in loaded.students}
    assert enrolled_students == {"S01"}

    restored_student = next(iter(loaded.students))
    assert restored_student.get_grade(loaded) == 9.5


def test_course_repository_list_all_returns_all_courses_regardless_of_order(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    courses = [
        Course(code="C02", name="Physics"),
        Course(code="C01", name="Math"),
        Course(code="C03", name="Chemistry"),
    ]

    with repository_harness.new_scope() as scope:
        for course in courses:
            scope.courses.add(course)

    # Act
    with repository_harness.new_scope() as scope:
        result = list(scope.courses.list_all())

    # Assert
    assert {course.code for course in result} == {"C01", "C02", "C03"}




