# cli/rendering/printers.py

from collections.abc import Iterable

from application.responses.student_response import StudentResponse
from application.responses.teacher_response import TeacherResponse
from application.responses.course_response import CourseResponse


# ---------------------------------------------------------------------
# Single-entity renderers
# ---------------------------------------------------------------------

def print_student(student: StudentResponse) -> None:
    print("Student")
    print("------")
    print(f"ID: {student.student_id}")
    print(f"Name: {student.name}")
    print()

    print("Enrolled Courses:")
    if student.enrolled_courses:
        for course_code in sorted(student.enrolled_courses):
            print(f"  - {course_code}")
    else:
        print("  (none)")
    print()

    print("Grades:")
    if student.grades:
        for course_code in sorted(student.grades):
            print(f"  {course_code}: {student.grades[course_code]}")
    else:
        print("  (none)")


def print_teacher(teacher: TeacherResponse) -> None:
    print("Teacher")
    print("------")
    print(f"ID: {teacher.teacher_id}")
    print(f"Name: {teacher.name}")
    print()

    print("Assigned Courses:")
    if teacher.course_codes:
        for course_code in sorted(teacher.course_codes):
            print(f"  - {course_code}")
    else:
        print("  (none)")


def print_course(course: CourseResponse) -> None:
    print("Course")
    print("------")
    print(f"Code: {course.course_code}")
    print(f"Name: {course.name}")

    teacher = course.teacher_id if course.teacher_id is not None else "(unassigned)"
    print(f"Teacher: {teacher}")
    print()

    print("Enrolled Students:")
    if course.student_ids:
        for student_id in sorted(course.student_ids):
            print(f"  - {student_id}")
    else:
        print("  (none)")


# ---------------------------------------------------------------------
# Collection renderers
# ---------------------------------------------------------------------

def print_students(students: Iterable[StudentResponse]) -> None:
    print("Students")
    print("--------")

    students = list(students)
    if not students:
        print("(none)")
        return

    for student in sorted(students, key=lambda s: s.student_id):
        print(f"{student.student_id}  {student.name}")


def print_teachers(teachers: Iterable[TeacherResponse]) -> None:
    print("Teachers")
    print("--------")

    teachers = list(teachers)
    if not teachers:
        print("(none)")
        return

    for teacher in sorted(teachers, key=lambda t: t.teacher_id):
        print(f"{teacher.teacher_id}  {teacher.name}")


def print_courses(courses: Iterable[CourseResponse]) -> None:
    print("Courses")
    print("-------")

    courses = list(courses)
    if not courses:
        print("(none)")
        return

    for course in sorted(courses, key=lambda c: c.course_code):
        teacher = course.teacher_id if course.teacher_id is not None else "(unassigned)"
        print(f"{course.course_code}  {course.name}  Teacher: {teacher}")
