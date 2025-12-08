# tests/integration/test_teacher_assignment_flow.py

import pytest

from domain.exceptions.domain_exceptions import (
    TeacherAssignmentError,
)
from tests.conftest import make_teacher, make_course


# -------------------------------------------------------------------
# Full teacher assignment lifecycle: assign → unassign
# -------------------------------------------------------------------
def test_teacher_assignment_full_lifecycle_flow(
    make_teacher,
    make_course
):
    # Arrange
    teacher = make_teacher()
    course = make_course()

    # Initial state
    assert course.teacher is None
    assert teacher.courses == ()

    # ---------------------------------------------------------------
    # Step 1: Assign
    # ---------------------------------------------------------------
    course.assign_teacher(teacher)

    assert course.teacher is teacher
    assert course in teacher.courses

    # ---------------------------------------------------------------
    # Step 2: Unassign
    # ---------------------------------------------------------------
    course.unassign_teacher()

    assert course.teacher is None
    assert course not in teacher.courses


# -------------------------------------------------------------------
# Assigning a teacher to an already assigned course raises error
# -------------------------------------------------------------------
def test_teacher_assignment_assigning_twice_raises_teacherassignmenterror(
    make_teacher,
    make_course
):
    # Arrange
    teacher1 = make_teacher()
    teacher2 = make_teacher()
    course = make_course()

    course.assign_teacher(teacher1)
    assert course.teacher is teacher1     # precondition

    # Act / Assert
    with pytest.raises(TeacherAssignmentError):
        course.assign_teacher(teacher2)


# -------------------------------------------------------------------
# A teacher may be assigned to multiple courses simultaneously
# -------------------------------------------------------------------
def test_teacher_assignment_teacher_can_be_assigned_to_multiple_courses(
    make_teacher,
    make_course
):
    # Arrange
    teacher = make_teacher()
    course1 = make_course()
    course2 = make_course()

    # Act
    course1.assign_teacher(teacher)
    course2.assign_teacher(teacher)

    # Assert
    assert course1 in teacher.courses
    assert course2 in teacher.courses
    assert len(teacher.courses) == 2


# -------------------------------------------------------------------
# Unassigning one course does not affect others
# -------------------------------------------------------------------
def test_teacher_assignment_unassigning_one_course_does_not_affect_others(
    make_teacher,
    make_course
):
    # Arrange
    teacher = make_teacher()
    course1 = make_course()
    course2 = make_course()

    course1.assign_teacher(teacher)
    course2.assign_teacher(teacher)

    assert course1 in teacher.courses
    assert course2 in teacher.courses

    # Act
    course1.unassign_teacher()

    # Assert
    assert course1 not in teacher.courses
    assert course2 in teacher.courses
    assert course2.teacher is teacher



