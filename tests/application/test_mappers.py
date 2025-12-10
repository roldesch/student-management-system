# tests/application/test_mappers.py

import pytest

from application.mappers.student_mapper import StudentMapper
from application.mappers.teacher_mapper import TeacherMapper
from application.mappers.course_mapper import CourseMapper

from tests.conftest import make_student, make_teacher, make_course


# -------------------------------------------------------------------
# StudentMapper
# -------------------------------------------------------------------

def test_studentmapper_converts_a_student_with_no_courses_into_a_correct_studentdto(make_student):
    # Arrange
    student = make_student()
    assert student.courses == ()     # precondition
    assert student._grades == {}     # precondition

    # Act
    dto = StudentMapper.to_dto(student)

    # Assert
    assert dto.student_id == student.id
    assert dto.name == student.name
    assert dto.enrolled_courses == []
    assert dto.grades == {}

def test_studentmapper_converts_a_student_with_courses_and_grades_into_a_correct_studentdto(
    make_student,
    make_course
):
    # Arrange
    student = make_student()
    course1 = make_course()
    course2 = make_course()

    # Enroll student in two courses
    course1.enroll(student)
    course2.enroll(student)

    # Assign grades
    student.assign_grade(course1, 9.0)
    student.assign_grade(course2, 7.5)

    # Act
    dto = StudentMapper.to_dto(student)

    # Assert
    assert set(dto.enrolled_courses) == {course1.code, course2.code}
    assert dto.grades == {
        course1.code: 9.0,
        course2.code: 7.5,
    }

    # Ensure immutability expectations
    assert dto.student_id == student.id
    assert dto.name == student.name

# -------------------------------------------------------------------
# TeacherMapper
# -------------------------------------------------------------------


def test_teachermapper_converts_a_teacher_with_no_assigned_courses_into_a_correct_teacherdto(make_teacher):
    # Arrange
    teacher = make_teacher()
    assert teacher.courses == ()    # precondition

    # Act
    dto = TeacherMapper.to_dto(teacher)

    # Assert
    assert dto.teacher_id == teacher.id
    assert dto.name == teacher.name
    assert dto.course_codes == []


def test_teachermapper_converts_a_teacher_with_multiple_assigned_courses_into_a_correct_teacherdto(
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
    dto = TeacherMapper.to_dto(teacher)

    # Assert
    assert set(dto.course_codes) == {course1.code, course2.code}


# -------------------------------------------------------------------
# CourseMapper
# -------------------------------------------------------------------

def test_coursemapper_converts_a_course_with_no_teacher_and_no_students_into_a_correct_coursedto(
    make_course
):
    # Arrange
    course = make_course()
    assert course.teacher is None
    assert course.students == ()

    # Act
    dto = CourseMapper.to_dto(course)

    # Assert
    assert dto.course_code == course.code
    assert dto.name == course.name
    assert dto.teacher_id is None
    assert dto.student_ids == []

def test_coursemapper_converts_a_course_with_a_teacher_and_students_into_a_correct_coursedto(
    make_teacher,
    make_student,
    make_course
):
    # Arrange
    teacher = make_teacher()
    course = make_course()
    student1 = make_student()
    student2 = make_student()

    course.assign_teacher(teacher)
    course.enroll(student1)
    course.enroll(student2)

    assert course.teacher is teacher
    assert set(course.students) == {student1, student2}

    # Act
    dto = CourseMapper.to_dto(course)

    # Assert
    assert dto.teacher_id == teacher.id
    assert set(dto.student_ids) == {student1.id, student2.id}
    assert dto.course_code == course.code
    assert dto.name == course.name


# -------------------------------------------------------------------
# Boundary Enforcement Tests
# Ensures mappers do not leak domain objects across layers.
# -------------------------------------------------------------------

def test_mappers_do_not_return_domain_entities_inside_dtos(
        make_teacher,
        make_student,
        make_course,
):
    teacher = make_teacher()
    student = make_student()
    course = make_course()

    course.assign_teacher(teacher)
    course.enroll(student)

    student_dto = StudentMapper.to_dto(student)
    teacher_dto = TeacherMapper.to_dto(teacher)
    course_dto = CourseMapper.to_dto(course)

    # Domain entities MUST NOT be present in DTOs
    assert all(not hasattr(student_dto, attr) for attr in ("courses", "students", "teacher"))
    assert all(not hasattr(teacher_dto, attr) for attr in ("courses",))
    assert all(not hasattr(course_dto, attr) for attr in ("students", "teacher"))


# -------------------------------------------------------------------
# Immutability (DTOs should not change if domain model later changes)
# -------------------------------------------------------------------

def test_dto_is_immutable_with_respect_to_future_domain_mutations(
    make_student,
    make_course
):
    # Arrange
    student = make_student()
    course = make_course()

    course.enroll(student)
    student.assign_grade(course, 8.0)

    dto = StudentMapper.to_dto(student)

    # Now mutate the domain object AFTER mapping
    student.assign_grade(course, 10.0)
    course.drop(student)

    # Assert DTO snapshot remains frozen in time (structurally)
    assert dto.grades == {course.code: 8.0}
    assert dto.enrolled_courses == [course.code]

