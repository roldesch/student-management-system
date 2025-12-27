# cli/main.py

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    """
    Build the top-level CLI argument parser and register all commands.

    This function defines the complete CLI command tree but does not
    bind any business logic.
    """
    parser = argparse.ArgumentParser(
        prog="sms",
        description="Student Management System CLI",
    )

    subparsers = parser.add_subparsers(
        dest="resource",
        required=True,
    )

    # -------------------------------------------------
    # student commands
    # -------------------------------------------------
    student_parser = subparsers.add_parser("student", help="Student operations")
    student_subparsers = student_parser.add_subparsers(
        dest="action",
        required=True,
    )

    student_add = student_subparsers.add_parser("add", help="Add a new student")
    student_add.add_argument("--id", required=True)
    student_add.add_argument("--name", required=True)

    student_show = student_subparsers.add_parser("show", help="Show a student")
    student_show.add_argument("student_id")

    student_list = student_subparsers.add_parser("list", help="List students")

    student_remove = student_subparsers.add_parser("remove", help="Remove a student")
    student_remove.add_argument("student_id")

    # -------------------------------------------------
    # teacher commands
    # -------------------------------------------------
    teacher_parser = subparsers.add_parser("teacher", help="Teacher operations")
    teacher_subparsers = teacher_parser.add_subparsers(
        dest="action",
        required=True,
    )

    teacher_add = teacher_subparsers.add_parser("add", help="Add a new teacher")
    teacher_add.add_argument("--id", required=True)
    teacher_add.add_argument("--name", required=True)

    teacher_show = teacher_subparsers.add_parser("show", help="Show a teacher")
    teacher_show.add_argument("teacher_id")

    teacher_list = teacher_subparsers.add_parser("list", help="List teachers")

    teacher_remove = teacher_subparsers.add_parser("remove", help="Remove a teacher")
    teacher_remove.add_argument("teacher_id")

    # -------------------------------------------------
    # course commands
    # -------------------------------------------------
    course_parser = subparsers.add_parser("course", help="Course operations")
    course_subparsers = course_parser.add_subparsers(
        dest="action",
        required=True,
    )

    course_add = course_subparsers.add_parser("add", help="Add a new course")
    course_add.add_argument("--code", required=True)
    course_add.add_argument("--name", required=True)

    course_show = course_subparsers.add_parser("show", help="Show a course")
    course_show.add_argument("course_code")

    course_list = course_subparsers.add_parser("list", help="List courses")

    course_remove = course_subparsers.add_parser("remove", help="Remove a course")
    course_remove.add_argument("course_code")

    # -------------------------------------------------
    # cross-resource commands
    # -------------------------------------------------
    enroll = subparsers.add_parser("enroll", help="Enroll a student in a course")
    enroll.add_argument("--student", required=True)
    enroll.add_argument("--course", required=True)

    drop = subparsers.add_parser("drop", help="Drop a student from a course")
    drop.add_argument("--student", required=True)
    drop.add_argument("--course", required=True)

    assign_teacher = subparsers.add_parser(
        "assign-teacher", help="Assign a teacher to a course"
    )
    assign_teacher.add_argument("--teacher", required=True)
    assign_teacher.add_argument("--course", required=True)

    unassign_teacher = subparsers.add_parser(
        "unassign-teacher", help="Unassign the teacher from a course"
    )
    unassign_teacher.add_argument("course_code")

    # -------------------------------------------------
    # grade commands
    # -------------------------------------------------
    grade_parser = subparsers.add_parser("grade", help="Grade operations")
    grade_subparsers = grade_parser.add_subparsers(
        dest="action",
        required=True,
    )

    grade_assign = grade_subparsers.add_parser("assign", help="Assign a grade")
    grade_assign.add_argument("--student", required=True)
    grade_assign.add_argument("--course", required=True)
    grade_assign.add_argument("--value", required=True)

    grade_remove = grade_subparsers.add_parser("remove", help="Remove a grade")
    grade_remove.add_argument("--student", required=True)
    grade_remove.add_argument("--course", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    """
    CLI entry point.

    For now, this function only parses arguments and prints the parsed
    namespace for verification purposes.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    # Placeholder behavior: no command dispatch yet
    print("Parsed arguments:")
    print(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
