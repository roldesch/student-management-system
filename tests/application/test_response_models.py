# tests/application/test_response_models.py

import pytest
from dataclasses import FrozenInstanceError

from application.responses.student_response import StudentResponse
from application.responses.teacher_response import TeacherResponse
from application.responses.course_response import CourseResponse


# -------------------------------------------------------------------
# StudentResponse
# -------------------------------------------------------------------

def test_studentresponse_holds_correct_fields():
    response = StudentResponse(
        student_id="S01",
        name="Alice",
        enrolled_courses=["C01", "C02"],
        grades={"C01": 9.0, "C02": 7.5},
    )

    assert response.student_id == "S01"
    assert response.name == "Alice"
    assert set(response.enrolled_courses) == {"C01", "C02"}
    assert response.grades == {"C01": 9.0, "C02": 7.5}


def test_studentresponse_is_immutable():
    response = StudentResponse(
        student_id="S01",
        name="Alice",
        enrolled_courses=["C01"],
        grades={"C01": 9.0},
    )

    with pytest.raises(FrozenInstanceError):
        response.student_id = "NEW-ID"

    with pytest.raises(TypeError):
        response.enrolled_courses.append("C02")

    with pytest.raises(TypeError):
        response.grades["C01"] = 10.0


def test_studentresponse_does_not_expose_domain_objects():
    response = StudentResponse(
        student_id="S01",
        name="Alice",
        enrolled_courses=["C01"],
        grades={"C01": 8.0},
    )

    forbidden = ("courses", "students", "teacher", "_grades")
    assert all(not hasattr(response, attr) for attr in forbidden)


# -------------------------------------------------------------------
# TeacherResponse
# -------------------------------------------------------------------

def test_teacherresponse_holds_correct_fields():
    response = TeacherResponse(
        teacher_id="T01",
        name="Dr. Smith",
        course_codes=["C01", "C99"],
    )

    assert response.teacher_id == "T01"
    assert response.name == "Dr. Smith"
    assert set(response.course_codes) == {"C01", "C99"}


def test_teacherresponse_is_immutable():
    response = TeacherResponse(
        teacher_id="T01",
        name="Dr. Smith",
        course_codes=["C01"],
    )

    with pytest.raises(FrozenInstanceError):
        response.teacher_id = "NEW-ID"

    with pytest.raises(TypeError):
        response.course_codes.append("C02")


def test_teacherresponse_does_not_expose_domain_objects():
    response = TeacherResponse(
        teacher_id="T01",
        name="Dr. Smith",
        course_codes=["C01"],
    )

    assert not hasattr(response, "courses")


# -------------------------------------------------------------------
# CourseResponse
# -------------------------------------------------------------------

def test_courseresponse_holds_correct_fields():
    response = CourseResponse(
        course_code="C01",
        name="Math",
        teacher_id="T01",
        student_ids=["S01", "S02"],
    )

    assert response.course_code == "C01"
    assert response.name == "Math"
    assert response.teacher_id == "T01"
    assert set(response.student_ids) == {"S01", "S02"}


def test_courseresponse_allows_teacher_id_none():
    response = CourseResponse(
        course_code="C01",
        name="Math",
        teacher_id=None,
        student_ids=[],
    )

    assert response.teacher_id is None
    assert response.student_ids == ()


def test_courseresponse_is_immutable():
    response = CourseResponse(
        course_code="C01",
        name="Math",
        teacher_id="T01",
        student_ids=["S01"],
    )

    with pytest.raises(FrozenInstanceError):
        response.course_code = "NEW"

    with pytest.raises(TypeError):
        response.student_ids.append("S99")


def test_courseresponse_does_not_expose_domain_objects():
    response = CourseResponse(
        course_code="C01",
        name="Math",
        teacher_id="T01",
        student_ids=["S01"],
    )

    forbidden = ("students", "teacher")
    assert all(not hasattr(response, attr) for attr in forbidden)


# -------------------------------------------------------------------
# Snapshot behavior
# -------------------------------------------------------------------

def test_response_models_are_immutable_snapshots_not_affected_by_later_changes():
    courses = ["C01"]
    grades = {"C01": 8.0}

    response = StudentResponse(
        student_id="S01",
        name="Alice",
        enrolled_courses=list(courses),
        grades=dict(grades),
    )

    courses.append("C02")
    grades["C01"] = 10.0

    assert response.enrolled_courses == ("C01",)
    assert response.grades == {"C01": 8.0}
