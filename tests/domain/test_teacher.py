# tests/domain/test_teacher.py

import pytest

from domain.exceptions.domain_exceptions import (
    TeacherAssignmentError,
)
from tests.conftest import make_teacher, make_course

# -------------------------------------------------------------------
# A new teacher starts with no assigned courses
# -------------------------------------------------------------------
def test_creating_a_new_teacher_results_in_a_teacher_with_no_assigned_courses(make_teacher):
    # Arrange
    teacher = make_teacher()

    # Assert
    assert teacher.courses == ()


# -------------------------------------------------------------------
# Assigning a teacher to a course succeeds when no teacher is assigned
# -------------------------------------------------------------------
def test_assigning_a_teacher_to_a_course_that_has_no_teacher_assigned_succeeds(
    make_teacher,
    make_course
):
    # Arrange
    teacher = make_teacher()
    course = make_course()
    assert course.teacher is None          # precondition
    assert course not in teacher.courses   # bidirectional precondition

    # Act
    course.assign_teacher(teacher)

    # Assert
    assert course.teacher is teacher
    assert course in teacher.courses


# -------------------------------------------------------------------
# Assigning a teacher to a course that already has a teacher raises TeacherAssignmentError
# -------------------------------------------------------------------
def test_assigning_a_teacher_to_a_course_that_already_has_a_teacher_assigned_raises_teacherassignmenterror(
    make_teacher,
    make_course
):
    # Arrange
    teacher1 = make_teacher()
    teacher2 = make_teacher()
    course = make_course()
    course.assign_teacher(teacher1)
    assert course.teacher is teacher1    # precondition

    # Act / Assert
    with pytest.raises(TeacherAssignmentError):
        course.assign_teacher(teacher2)


# -------------------------------------------------------------------
# Unassigning a teacher from a course succeeds when the course has that teacher
# -------------------------------------------------------------------
def test_unassigning_a_teacher_from_a_course_that_has_a_teacher_assigned_succeeds(
    make_teacher,
    make_course
):
    # Arrange
    teacher = make_teacher()
    course = make_course()
    course.assign_teacher(teacher)   # precondition

    # Act
    course.unassign_teacher()

    # Assert
    assert course.teacher is None
    assert course not in teacher.courses

# -------------------------------------------------------------------
# Unassigning a teacher from a course with no assigned teacher raises error
# -------------------------------------------------------------------
def test_unassigning_a_teacher_from_a_course_that_has_no_teacher_assigned_raises_teacherassignmenterror(
    make_course
):
    # Arrange
    course = make_course()
    assert course.teacher is None    # precondition

    # Act / Assert
    with pytest.raises(TeacherAssignmentError):
        course.unassign_teacher()


# -------------------------------------------------------------------
# A teacher may be assigned to multiple courses
# -------------------------------------------------------------------
def test_a_teacher_can_be_assigned_to_multiple_courses(
    make_teacher,
    make_course
):
    # Arrange
    teacher = make_teacher()
    course1 = make_course()
    course2 = make_course()

    assert teacher.courses == ()     # precondition

    # Act
    course1.assign_teacher(teacher)
    course2.assign_teacher(teacher)

    # Assert
    assert course1 in teacher.courses
    assert course2 in teacher.courses
    assert len(teacher.courses) == 2


# -------------------------------------------------------------------
# When a teacher is removed from one course, other assignments remain intact
# -------------------------------------------------------------------
def test_unassigning_a_teacher_from_one_course_does_not_affect_other_courses(
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






