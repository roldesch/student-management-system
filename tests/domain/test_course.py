import pytest

from exceptions.domain_exceptions import EnrollmentError, TeacherAssignmentError

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
