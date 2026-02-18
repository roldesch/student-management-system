# tests/contracts/repository/test_course_repository_contract.py

from __future__ import annotations

import pytest

from domain.models.course import Course
from domain.models.student import Student
from domain.models.teacher import Teacher

from domain.exceptions.domain_exceptions import (
    DuplicateEntityError,
    EntityNotFoundError,
)

from tests.contracts.repository.conftest import RepositoryHarness


# -----------------------------------------------------------------------------
# CourseRepository Contract Tests
# -----------------------------------------------------------------------------
# Scope:
# - Persistence semantics only
# - Aggregate reconstruction
# - Identity and existence behavior
# - No business rule assertions
# - No ordering guarantees
# - Exact exception identity enforcement
# - Domain entity shape enforcement
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
    assert isinstance(loaded, Course)  # entity shape enforcement
    assert loaded.code == "C01"
    assert loaded.name == "Math"


def test_course_repository_add_existing_course_identity_raises_duplicate_entity_error(
        repository_harness: RepositoryHarness
) -> None:
    # Arrange
    course = Course(code="C01", name="Math")

    with repository_harness.new_scope() as scope:
        scope.courses.add(course)


    # Act / Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises(DuplicateEntityError) as exc_info:
            scope.courses.add(Course(code="C01", name="Math Clone"))

    # Exact type identity enforcement
    assert type(exc_info.value) is DuplicateEntityError


def test_course_repository_get_missing_course_raises_entity_not_found_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    missing_course_code = "C04"


    # Act / Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises(EntityNotFoundError) as exc_info:
            scope.courses.get(missing_course_code)

    # Exact type identity enforcement
    assert type(exc_info.value) is EntityNotFoundError


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


    # Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises(EntityNotFoundError) as exc_info:
            scope.courses.get("C01")

    # Exact type identity enforcement
    assert type(exc_info.value) is EntityNotFoundError


def test_course_repository_remove_missing_course_raises_entity_not_found_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    missing_course_code = "C04"


    # Act / Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises(EntityNotFoundError) as exc_info:
            scope.courses.remove(missing_course_code)

    # Exact type identity enforcement
    assert type(exc_info.value) is EntityNotFoundError


# -----------------------------------------------------------------------------
# Aggregate Reconstruction (Critical for Phase-4B)
# -----------------------------------------------------------------------------

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

    # Assert — aggregate shape enforcement
    assert isinstance(loaded, Course)
    assert loaded.code == "C01"
    assert loaded.name == "Math"

    # Teacher restoration
    assert loaded.teacher is not None
    assert isinstance(loaded.teacher, Teacher)
    assert loaded.teacher.id == "T01"
    assert loaded.teacher.name == "Dr. Smith"

    # Student restoration
    enrolled_students = list(loaded.students)
    assert all(isinstance(s, Student) for s in enrolled_students)
    assert {s.id for s in enrolled_students} == {"S01"}
    assert {s.name for s in enrolled_students} == {"Alice"}


    # Grade restoration
    restored_student = enrolled_students[0]
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
    assert all(isinstance(course, Course) for course in result)
    assert {course.code for course in result} == {"C01", "C02", "C03"}




