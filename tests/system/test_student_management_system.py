# tests/system/test_student_management_system.py

import pytest
from domain.exceptions.domain_exceptions import (
    EnrollmentError,
    TeacherAssignmentError,
    GradeError,
)


# -------------------------------------------------------------------
# 1. Create entities
# -------------------------------------------------------------------

def test_create_entities(sms):
    s1 = sms.add_student("S01", "Alice")
    t1 = sms.add_teacher("T01", "Dr. Smith")
    c1 = sms.add_course("C01", "Math")

    # Re-query via the service (snapshots)
    s = sms.get_student("S01")
    t = sms.get_teacher("T01")
    c = sms.get_course("C01")

    assert s.student_id == "S01"
    assert t.teacher_id == "T01"
    assert c.course_code == "C01"

    # No relationships yet
    assert s.enrolled_courses == ()
    assert t.course_codes == ()
    assert c.student_ids == ()
    assert c.teacher_id is None


# -------------------------------------------------------------------
# 2. Assign teacher to course
# -------------------------------------------------------------------

def test_assign_teacher_to_course(sms):
    sms.add_teacher("T01", "Dr. Smith")
    sms.add_course("C01", "Math")

    sms.assign_teacher_to_course("T01", "C01")

    teacher = sms.get_teacher("T01")
    course = sms.get_course("C01")

    assert course.teacher_id == "T01"
    assert "C01" in teacher.course_codes

    # Assign again should fail
    with pytest.raises(TeacherAssignmentError):
        sms.assign_teacher_to_course("T01", "C01")


# -------------------------------------------------------------------
# 3. Enroll students in course
# -------------------------------------------------------------------

def test_enroll_students(sms):
    sms.add_student("S01", "Alice")
    sms.add_student("S02", "Bob")
    sms.add_course("C01", "Math")

    sms.enroll_student_in_course("S01", "C01")
    sms.enroll_student_in_course("S02", "C01")

    course = sms.get_course("C01")
    s1 = sms.get_student("S01")

    assert set(course.student_ids) == {"S01", "S02"}
    assert "C01" in s1.enrolled_courses

    # Enrolling the same student again raises EnrollmentError
    with pytest.raises(EnrollmentError):
        sms.enroll_student_in_course("S01", "C01")


# -------------------------------------------------------------------
# 4. Assign and retrieve grades
# -------------------------------------------------------------------

def test_assign_and_get_grades(sms):
    sms.add_student("S01", "Alice")
    sms.add_course("C01", "Math")

    # Must enroll before grading
    sms.enroll_student_in_course("S01", "C01")

    sms.assign_grade_to_student("S01", "C01", 9.0)
    assert sms.get_student_grade("S01", "C01") == 9.0

    # Invalid grade (e.g., > 10 or < 0)
    with pytest.raises(GradeError):
        sms.assign_grade_to_student("S01", "C01", 11.0)

    # Grade requires enrollment
    sms.add_student("S02", "Bob")
    with pytest.raises(GradeError):
        sms.assign_grade_to_student("S02", "C01", 8.0)


# -------------------------------------------------------------------
# 5. Removing a course cleans up relationships
# -------------------------------------------------------------------

def test_remove_course_cleanup(sms):
    sms.add_student("S01", "Alice")
    sms.add_teacher("T01", "Dr. Smith")
    sms.add_course("C01", "Math")

    sms.assign_teacher_to_course("T01", "C01")
    sms.enroll_student_in_course("S01", "C01")

    sms.remove_course("C01")

    student = sms.get_student("S01")
    teacher = sms.get_teacher("T01")

    assert "C01" not in [c.code_code for c in sms.list_courses()]
    assert student.enrolled_courses == ()
    assert teacher.course_codes == ()


# -------------------------------------------------------------------
# 6. Removing a student cleans up
# -------------------------------------------------------------------

def test_remove_student_cleanup(sms):
    sms.add_student("S01", "Alice")
    sms.add_course("C01", "Math")

    sms.enroll_student_in_course("S01", "C01")
    sms.remove_student("S01")

    course = sms.get_course("C01")

    assert "S01" not in course.student_ids


# -------------------------------------------------------------------
# 7. Removing a teacher cleans up relationships
# -------------------------------------------------------------------

def test_remove_teacher_cleanup(sms):
    sms.add_teacher("T01", "Dr. Smith")
    sms.add_course("C01", "Math")
    sms.assign_teacher_to_course("T01", "C01")

    sms.remove_teacher("T01")
    course = sms.get_course("C01")

    assert course.teacher_id is None