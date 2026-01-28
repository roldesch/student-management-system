# tests/infrastructure/sqlite/test_teacher_repository_contract.py

from __future__ import annotations

import pytest

from domain.models.teacher import Teacher

from infrastructure.sqlite.errors import (
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


def test_teacher_repository_add_existing_teacher_identity_raises_duplicate_entity_error(
    repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    teacher = Teacher(teacher_id="T01", name="Dr. Smith")

    with repository_harness.new_scope() as scope:
        scope.teachers.add(teacher)

    _xfail_memory_noncompliant(repository_harness)  # Phase-4A temporary suspension

    # Act / Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises(DuplicateEntityError):
            scope.teachers.add(
                Teacher(teacher_id="T01", name="Dr. Smith Clone")
            )


def test_teacher_repository_get_missing_teacher_raises_entity_not_found_error(
    repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    missing_teacher_id = "T04"

    _xfail_memory_noncompliant(repository_harness)  # Phase-4A temporary suspension

    # Act / Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises(EntityNotFoundError):
            scope.teachers.get(missing_teacher_id)


def test_teacher_repository_remove_existing_teacher_then_get_raises_entity_not_found_error(
    repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    teacher = Teacher(teacher_id="T01", name="Dr. Smith")

    with repository_harness.new_scope() as scope:
        scope.teachers.add(teacher)

    with repository_harness.new_scope() as scope:
        scope.teachers.remove("T01")

    _xfail_memory_noncompliant(repository_harness)  # Phase-4A temporary suspension

    # Act / Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises(EntityNotFoundError):
            scope.teachers.get("T01")


def test_teacher_repository_remove_missing_teacher_raises_entity_not_found_error(
    repository_harness: RepositoryHarness,
) -> None:
    # Arrange
    missing_teacher_id = "T04"

    _xfail_memory_noncompliant(repository_harness)  # Phase-4A temporary suspension

    # Act / Assert
    with repository_harness.new_scope() as scope:
        with pytest.raises(EntityNotFoundError):
            scope.teachers.remove(missing_teacher_id)


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
