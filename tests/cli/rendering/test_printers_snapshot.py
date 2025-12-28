# tests/cli/rendering/test_printers_snapshot.py

import io
import sys

from application.responses.student_response import StudentResponse
from application.responses.teacher_response import TeacherResponse
from application.responses.course_response import CourseResponse

from cli.rendering.printers import (
    print_student,
    print_teacher,
    print_course,
    print_students,
    print_teachers,
    print_courses,
)


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def capture_stdout(func, *args):
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer
    try:
        func(*args)
    finally:
        sys.stdout = old_stdout
    return buffer.getvalue()


# ------------------------------------------------------------
# Single-entity snapshots
# ------------------------------------------------------------

def test_print_student_snapshot():
    student = StudentResponse(
        student_id="S01",
        name="Alice",
        enrolled_courses=["C02", "C01"],
        grades={"C01": 9.5, "C02": 8.0},
    )

    output = capture_stdout(print_student, student)

    expected = (
        "Student\n"
        "------\n"
        "ID: S01\n"
        "Name: Alice\n"
        "\n"
        "Enrolled Courses:\n"
        "  - C01\n"
        "  - C02\n"
        "\n"
        "Grades:\n"
        "  C01: 9.5\n"
        "  C02: 8.0\n"
    )

    assert output == expected


def test_print_teacher_snapshot():
    teacher = TeacherResponse(
        teacher_id="T01",
        name="Dr. Smith",
        course_codes=["C02", "C01"],
    )

    output = capture_stdout(print_teacher, teacher)

    expected = (
        "Teacher\n"
        "------\n"
        "ID: T01\n"
        "Name: Dr. Smith\n"
        "\n"
        "Assigned Courses:\n"
        "  - C01\n"
        "  - C02\n"
    )

    assert output == expected


def test_print_course_snapshot():
    course = CourseResponse(
        course_code="C01",
        name="Math",
        teacher_id=None,
        student_ids=["S02", "S01"],
    )

    output = capture_stdout(print_course, course)

    expected = (
        "Course\n"
        "------\n"
        "Code: C01\n"
        "Name: Math\n"
        "Teacher: (unassigned)\n"
        "\n"
        "Enrolled Students:\n"
        "  - S01\n"
        "  - S02\n"
    )

    assert output == expected


# ------------------------------------------------------------
# Collection snapshots
# ------------------------------------------------------------

def test_print_students_list_snapshot():
    students = (
        StudentResponse(
            student_id="S02",
            name="Bob",
            enrolled_courses=[],
            grades={},
        ),
        StudentResponse(
            student_id="S01",
            name="Alice",
            enrolled_courses=[],
            grades={},
        ),
    )

    output = capture_stdout(print_students, students)

    expected = (
        "Students\n"
        "--------\n"
        "S01  Alice\n"
        "S02  Bob\n"
    )

    assert output == expected


def test_print_teachers_list_snapshot():
    teachers = (
        TeacherResponse(
            teacher_id="T02",
            name="Prof. Doe",
            course_codes=[],
        ),
        TeacherResponse(
            teacher_id="T01",
            name="Dr. Smith",
            course_codes=[],
        ),
    )

    output = capture_stdout(print_teachers, teachers)

    expected = (
        "Teachers\n"
        "--------\n"
        "T01  Dr. Smith\n"
        "T02  Prof. Doe\n"
    )

    assert output == expected


def test_print_courses_list_snapshot():
    courses = (
        CourseResponse(
            course_code="C02",
            name="Physics",
            teacher_id=None,
            student_ids=[],
        ),
        CourseResponse(
            course_code="C01",
            name="Math",
            teacher_id="T01",
            student_ids=[],
        ),
    )

    output = capture_stdout(print_courses, courses)

    expected = (
        "Courses\n"
        "-------\n"
        "C01  Math  Teacher: T01\n"
        "C02  Physics  Teacher: (unassigned)\n"
    )

    assert output == expected
