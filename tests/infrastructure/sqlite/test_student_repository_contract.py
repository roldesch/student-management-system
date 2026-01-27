
# tests/infrastructure/sqlite/test_student_repository_contract.py

from __future__ import annotations

import pytest

from domain.models.student import Student
from domain.exceptions.domain_exceptions import (
    DuplicateEntityError as DomainDuplicateEntityError,
    EntityNotFoundError as DomainEntityNotFoundError,
)
from infrastructure.sqlite.errors import (
    DuplicateEntityError,
    EntityNotFoundError,
)

from tests.infrastructure.sqlite.conftest import RepositoryHarness


# -----------------------------------------------------------------------------
# StudentRepository Contract Tests
# -----------------------------------------------------------------------------
# Scope:
# - Persistence semantics only
# - Identity and existence behavior
# - No business rules
# - No ordering guarantees
# -----------------------------------------------------------------------------

def test_student_repository_add_then_get_returns_student_with_same_identity_and_name(
     repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    student = Student(student_id="S01", name="Alice")

    # Act
    with repository_harness.new_scope() as scope:
        scope.students.add(student)

    with repository_harness.new_scope() as scope:
        loaded = scope.students.get("S01")

    # Assert
    assert loaded.id == "S01"
    assert loaded.name == "Alice"


def test_student_repository_add_duplicate_identity_raises_duplicate_entity_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    first = Student(student_id="S01", name="Alice")
    duplicate = Student(student_id="S01", name="Alice")

    # Act
    with repository_harness.new_scope() as scope:
        scope.students.add(first)

    # Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises((DuplicateEntityError, DomainDuplicateEntityError)):
            scope.students.add(duplicate)


def test_student_repository_get_missing_student_raises_entity_not_found_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    missing_student_id = "S04"

    with repository_harness.new_scope() as scope:
        # Act
        action = lambda: scope.students.get(missing_student_id)

        # / Assert
        with pytest.raises((EntityNotFoundError, DomainEntityNotFoundError)):
            action()


def test_student_repository_remove_existing_student_then_get_raises_entity_not_found_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    student = Student(student_id="S01", name="Alice")

    with repository_harness.new_scope() as scope:
        scope.students.add(student)

    # Act
    with repository_harness.new_scope() as scope:
        scope.students.remove("S01")

    # Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises((EntityNotFoundError, DomainEntityNotFoundError)):
            scope.students.get("S01")


def test_student_repository_remove_missing_student_raises_entity_not_found_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    missing_student_id = "S04"

    with repository_harness.new_scope() as scope:
        # Act
        action = lambda: scope.students.remove(missing_student_id)

        # / Assert
        with pytest.raises((EntityNotFoundError, DomainEntityNotFoundError)):
            action()


def test_student_repository_list_all_returns_all_students_regardless_of_order(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    students = [
        Student(student_id="S02", name="Bob"),
        Student(student_id="S01", name="Alice"),
        Student(student_id="S03", name="Sarah"),
    ]

    with repository_harness.new_scope() as scope:
        for student in students:
            scope.students.add(student)

    # Act
    with repository_harness.new_scope() as scope:
        result = list(scope.students.list_all())

    # Assert
    assert {student.id for student in result} == {"S01", "S02", "S03"}




