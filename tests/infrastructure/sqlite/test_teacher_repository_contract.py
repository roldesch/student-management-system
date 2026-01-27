
# tests/infrastructure/sqlite/test_teacher_repository_contract.py

from __future__ import annotations

import pytest

from domain.models.teacher import Teacher
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
# TeacherRepository Contract Tests
# -----------------------------------------------------------------------------
# Scope:
# - Persistence semantics only
# - Identity and existence behavior
# - No business rules
# - No ordering guarantees
# -----------------------------------------------------------------------------

def test_teacher_repository_add_then_get_returns_teacher_with_same_identity_and_name(
     repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    teacher = Teacher(teacher_id="T01", name="Dr. Smith")

    # Act
    with repository_harness.new_scope() as scope:
        scope.teachers.add(teacher)

    with repository_harness.new_scope() as scope:
        loaded = scope.teachers.get("T01")

    # Assert
    assert loaded.id == "T01"
    assert loaded.name == "Dr. Smith"


def test_teacher_repository_add_duplicate_identity_raises_duplicate_entity_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    first = Teacher(teacher_id="T01", name="Dr. Smith")
    duplicate = Teacher(teacher_id="T01", name="Dr. Smith")

    # Act
    with repository_harness.new_scope() as scope:
        scope.teachers.add(first)

    # Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises((DuplicateEntityError, DomainDuplicateEntityError)):
            scope.teachers.add(duplicate)


def test_teacher_repository_get_missing_teacher_raises_entity_not_found_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    missing_teacher_id = "T04"

    with repository_harness.new_scope() as scope:
        # Act
        action = lambda: scope.teachers.get(missing_teacher_id)

        # / Assert
        with pytest.raises((EntityNotFoundError, DomainEntityNotFoundError)):
            action()


def test_teacher_repository_remove_existing_teacher_then_get_raises_entity_not_found_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    teacher = Teacher(teacher_id="T01", name="Dr. Smith")

    with repository_harness.new_scope() as scope:
        scope.teachers.add(teacher)

    # Act
    with repository_harness.new_scope() as scope:
        scope.teachers.remove("T01")

    # Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises((EntityNotFoundError, DomainEntityNotFoundError)):
            scope.teachers.get("T01")


def test_teacher_repository_remove_missing_teacher_raises_entity_not_found_error(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    missing_teacher_id = "T04"

    with repository_harness.new_scope() as scope:
        # Act
        action = lambda: scope.teachers.remove(missing_teacher_id)

        # / Assert
        with pytest.raises((EntityNotFoundError, DomainEntityNotFoundError)):
            action()


def test_teacher_repository_list_all_returns_all_teachers_regardless_of_order(
        repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    teachers = [
        Teacher(teacher_id="T02", name="Dr. Brown"),
        Teacher(teacher_id="T01", name="Dr. Smith"),
        Teacher(teacher_id="T03", name="Dr. Taylor"),
    ]

    with repository_harness.new_scope() as scope:
        for teacher in teachers:
            scope.teachers.add(teacher)

    # Act
    with repository_harness.new_scope() as scope:
        result = list(scope.teachers.list_all())

    # Assert
    assert {teacher.id for teacher in result} == {"T01", "T02", "T03"}




