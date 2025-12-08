# tests/domain/test_student.py

import pytest

from domain.exceptions.domain_exceptions import (
    EnrollmentError,
    GradeError,
)
from tests.conftest import make_student, make_course


# -------------------------------------------------------------------
# A new student has no courses and no grades
# -------------------------------------------------------------------
def test_creating_a_new_student_results_in_a_student_with_no_courses_and_no_grades(make_student):
    # Arrange
    student = make_student()

    # Assert
    assert student.courses == ()
    assert student._grades == {}  # internal state allowed in domain-level tests later


# -------------------------------------------------------------------
# Enrolling a student succeeds when the student is not yet enrolled
# -------------------------------------------------------------------
def test_enrolling_a_student_in_a_course_when_the_student_is_not_yet_enrolled_succeeds(
    make_student,
    make_course
):
    # Arrange
    student = make_student()
    course = make_course()
    assert course not in student.courses    # precondition
    assert student not in course.students   # bidirectional precondition

    # Act
    course.enroll(student)

    # Assert
    assert course in student.courses
    assert student in course.students


# -------------------------------------------------------------------
# Enrolling a student in a course when the student is already enrolled raises EnrollmentError
# -------------------------------------------------------------------
def test_enrolling_a_student_in_a_course_when_the_student_is_already_enrolled_raises_enrollmenterror(
    make_student,
    make_course
):
    # Arrange
    student = make_student()
    course = make_course()
    course.enroll(student)
    assert course in student.courses      # precondition
    assert student in course.students     # bidirectional precondition

    # Act / Assert
    with pytest.raises(EnrollmentError):
        course.enroll(student)


# -------------------------------------------------------------------
# Assigning a valid grade to a student enrolled in the course succeeds
# -------------------------------------------------------------------
def test_assigning_a_valid_grade_to_a_student_enrolled_in_a_course_succeeds(
    make_student,
    make_course
):
    # Arrange
    student = make_student()
    course = make_course()
    course.enroll(student)     # must be enrolled first
    assert student.get_grade(course) is None  # precondition: no grade yet

    # Act
    student.assign_grade(course, 9.5)

    # Assert
    assert student.get_grade(course) == 9.5


# -------------------------------------------------------------------
# Assigning a grade to a non-enrolled student raises GradeError
# -------------------------------------------------------------------
def test_assigning_a_grade_to_a_student_for_a_course_the_student_is_not_enrolled_in_raises_gradeerror(
    make_student,
    make_course
):
    # Arrange
    student = make_student()
    course = make_course()
    assert course not in student.courses  # precondition

    # Act / Assert
    with pytest.raises(GradeError):
        student.assign_grade(course, 8.0)


# -------------------------------------------------------------------
# Assigning an invalid grade (outside allowed range) raises GradeError
# -------------------------------------------------------------------
@pytest.mark.parametrize("invalid_value", [-1, -10, 11, 25])
def test_assigning_an_invalid_grade_value_raises_gradeerror(
    make_student,
    make_course,
    invalid_value
):
    # Arrange
    student = make_student()
    course = make_course()
    course.enroll(student)    # must be enrolled first

    # Act / Assert
    with pytest.raises(GradeError):
        student.assign_grade(course, invalid_value)


# -------------------------------------------------------------------
# Removing an existing grade succeeds
# -------------------------------------------------------------------
def test_removing_an_existing_grade_from_a_student_for_a_course_succeeds(
    make_student,
    make_course
):
    # Arrange
    student = make_student()
    course = make_course()
    course.enroll(student)   # must be enrolled first

    student.assign_grade(course, 7.0)
    assert student.get_grade(course) == 7.0   # sanity check

    #Act
    student.remove_grade(course)

    # Assert
    assert student.get_grade(course) is None


# -------------------------------------------------------------------
# Removing a grade from a course the student is not enrolled in raises
# -------------------------------------------------------------------
def test_removing_a_grade_from_a_course_the_student_is_not_enrolled_in_raises_gradeerror(
    make_student,
    make_course
):
    # Arrange
    student = make_student()
    course = make_course()
    assert course not in student.courses   # precondition

    # Act / Assert
    with pytest.raises(GradeError):
        student.remove_grade(course)
