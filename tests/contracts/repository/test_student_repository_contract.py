# tests/contracts/repository/test_student_repository_contract.py

from __future__ import annotations

import pytest

from domain.models.student import Student

from domain.exceptions.domain_exceptions import (
    DuplicateEntityError,
    EntityNotFoundError,
)

from tests.contracts.repository.conftest import RepositoryHarness


# -----------------------------------------------------------------------------
# StudentRepository Contract Tests
# -----------------------------------------------------------------------------
# Scope:
# - Persistence semantics only
# - Identity and existence behavior
# - No business rules
# - No ordering guarantees
# - Exact exception identity enforcement
# - Domain entity shape enforcement
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
    assert isinstance(loaded, Student)    # entity shape enforcement
    assert loaded.id == "S01"
    assert loaded.name == "Alice"


def test_student_repository_update_existing_student_persists_state(
    repository_harness: RepositoryHarness,
) -> None:
    student = Student(student_id="S01", name="Alice")

    with repository_harness.new_scope() as scope:
        scope.students.add(student)

    student.name = "Alice Updated"

    with repository_harness.new_scope() as scope:
        scope.students.update(student)

    with repository_harness.new_scope() as scope:
        loaded = scope.students.get("S01")

    assert loaded.name == "Alice Updated"


def test_student_repository_update_is_idempotent(
    repository_harness: RepositoryHarness,
) -> None:
    student = Student(student_id="S01", name="Alice")

    with repository_harness.new_scope() as scope:
        scope.students.add(student)

    with repository_harness.new_scope() as scope:
        scope.students.update(student)
        scope.students.update(student)

    with repository_harness.new_scope() as scope:
        loaded = scope.students.get("S01")

    assert loaded.name == "Alice"


def test_student_repository_update_missing_student_raises_entity_not_found_error(
    repository_harness: RepositoryHarness,
) -> None:
    student = Student(student_id="S01", name="Alice")

    with repository_harness.new_scope() as scope:
        with pytest.raises(EntityNotFoundError) as exc_info:
            scope.students.update(student)

    assert type(exc_info.value) is EntityNotFoundError


def test_student_repository_add_existing_student_identity_raises_duplicate_entity_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    student = Student(student_id="S01", name="Alice")

    with repository_harness.new_scope() as scope:
        scope.students.add(student)


    # Act / Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises(DuplicateEntityError) as exc_info:
            scope.students.add(
                Student(student_id="S01", name="Alice Clone")
            )

    # Exact type identity enforcement
    assert type(exc_info.value) is DuplicateEntityError


def test_student_repository_get_missing_student_raises_entity_not_found_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    missing_student_id = "S04"


    # Act / Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises(EntityNotFoundError) as exc_info:
            scope.students.get(missing_student_id)

    # Exact type identity enforcement
    assert type(exc_info.value) is EntityNotFoundError


def test_student_repository_remove_existing_student_then_get_raises_entity_not_found_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    student = Student(student_id="S01", name="Alice")

    with repository_harness.new_scope() as scope:
        scope.students.add(student)

    with repository_harness.new_scope() as scope:
        scope.students.remove("S01")


    # Act / Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises(EntityNotFoundError) as exc_info:
            scope.students.get("S01")

    # Exact type identity enforcement
    assert type(exc_info.value) is EntityNotFoundError


def test_student_repository_remove_missing_student_raises_entity_not_found_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    missing_student_id = "S04"


    # Act / Assert
    with repository_harness.new_scope() as scope:
       with pytest.raises(EntityNotFoundError) as exc_info:
           scope.students.remove(missing_student_id)

    # Exact type identity enforcement
    assert type(exc_info.value) is EntityNotFoundError


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
    # Domain entity shape enforcement
    assert all(isinstance(student, Student) for student in result)

    # Identity correctness (no ordering guarantees)
    assert {student.id for student in result} == {"S01", "S02", "S03"}





