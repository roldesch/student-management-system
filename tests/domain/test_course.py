#test_course.py
import pytest
from exceptions.domain_exceptions import EnrollmentError, TeacherAssignmentError
from tests.conftest import make_course


def test_assigning_a_teacher_to_a_course_that_has_no_teacher_assigned_succeeds(make_course, make_teacher):
    # Arrange
    course = make_course()
    teacher = make_teacher()
    assert course.teacher is None

    # Act
    course.assign_teacher(teacher)

    # Assert
    assert course.teacher is teacher
    assert course in teacher.courses

def test_assigning_a_teacher_to_a_course_that_already_has_a_teacher_assigned_raises_teacherassignmenterror(make_course, make_teacher):
    # Arrange
    course = make_course()
    teacher1 = make_teacher()
    teacher2 = make_teacher()

    # Act
    course.assign_teacher(teacher1)

    # Assert
    with pytest.raises(TeacherAssignmentError):
        course.assign_teacher(teacher2)

def test_unassigning_a_teacher_from_a_course_that_already_has_a_teacher_assigned_succeeds(make_course, make_teacher):
    # Arrange
    course = make_course()
    teacher = make_teacher()
    course.assign_teacher(teacher)
    assert course.teacher is teacher # sanity check

    # Act
    course.unassign_teacher()

    # Assert
    assert course.teacher is None
    assert course not in teacher.courses

def test_unassigning_a_teacher_from_a_course_that_has_no_teacher_assigned_raises_teacherassignmenterror(make_course):
    # Arrange
    course = make_course()
    assert  course.teacher is None  # precondition

    # Act / Assert
    with pytest.raises(TeacherAssignmentError):
        course.unassign_teacher()
