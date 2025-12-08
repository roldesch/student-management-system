# tests/integration/test_enrollment_flow.py

import pytest

from domain.exceptions.domain_exceptions import (
    EnrollmentError,
    GradeError,
)
from tests.conftest import make_student, make_course


# -------------------------------------------------------------------
# Full enrollment workflow: enroll → grade → remove grade → drop
# -------------------------------------------------------------------
def test_full_enrollment_lifecycle_flow(
    make_student,
    make_course
):
    # Arrange
    student = make_student()
    course = make_course()

    # Initial state checks
    assert course not in student.courses
    assert student not in course.students
    assert student.get_grade(course) is None

    # ---------------------------------------------------------------
    # Step 1: Enroll
    # ---------------------------------------------------------------
    course.enroll(student)

    assert student in course.students
    assert course in student.courses

    # ---------------------------------------------------------------
    # Step 2: Assign a valid grade
    # ---------------------------------------------------------------
    student.assign_grade(course, 9.0)
    assert student.get_grade(course) == 9.0

    # ---------------------------------------------------------------
    # Step 3: Removing grade should succeed
    # ---------------------------------------------------------------
    student.remove_grade(course)
    assert student.get_grade(course) is None

    # ---------------------------------------------------------------
    # Step 4: Drop the student
    # ---------------------------------------------------------------
    course.drop(student)

    assert course not in student.courses
    assert student not in course.students
    assert student.get_grade(course) is None


# -------------------------------------------------------------------
# Enrolling twice raises EnrollmentError
# -------------------------------------------------------------------
def test_enrollment_flow_enrolling_the_same_student_twice_raises_enrollmenterror(
    make_student,
    make_course
):
    # Arrange
    student = make_student()
    course = make_course()

    course.enroll(student)
    assert student in course.students     # precondition

    # Act / Assert
    with pytest.raises(EnrollmentError):
        course.enroll(student)


# -------------------------------------------------------------------
# Assigning a grade when not enrolled raises GradeError
# -------------------------------------------------------------------
def test_enrollment_flow_assigning_grade_to_non_enrolled_student_raises_gradeerror(
    make_student,
    make_course
):
    # Arrange
    student = make_student()
    course = make_course()
    assert course not in student.courses    # precondition

    # Act / Assert
    with pytest.raises(GradeError):
        student.assign_grade(course, 7.0)


# -------------------------------------------------------------------
# Dropping a student who is not enrolled raises EnrollmentError
# -------------------------------------------------------------------
def test_enrollment_flow_dropping_a_student_not_enrolled_raises_enrollmenterror(
    make_student,
    make_course
):
    # Arrange
    student = make_student()
    course = make_course()
    assert student not in course.students    # precondition

    # Act / Assert
    with pytest.raises(EnrollmentError):
        course.drop(student)
