# cli/main.py

import os
from pathlib import Path

import argparse
import sys
from typing import TYPE_CHECKING

from cli.version import SMS_VERSION
from cli.app_factory import create_sms, PersistenceConfig
from cli.errors import ConfigurationError
from cli.rendering.errors import render_error
from cli.rendering.printers import (
    print_student,
    print_students,
    print_teacher,
    print_teachers,
    print_course,
    print_courses,
)

if TYPE_CHECKING:
    from cli.application_api import StudentManagementSystemAPI

# -------------------------------------------------
# Exit code constants (authoritative)
# -------------------------------------------------
EXIT_SUCCESS = 0
EXIT_USAGE_ERROR = 1
EXIT_VALIDATION_ERROR = 2
EXIT_DOMAIN_ERROR = 3
EXIT_STATE_ERROR = 4
EXIT_SYSTEM_ERROR = 10


# -------------------------------------------------
# Command handlers
# -------------------------------------------------

# -------------------------------------------------
# Student commands handlers
# -------------------------------------------------
def handle_student_add(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    sms.add_student(
        student_id=args.id,
        name=args.name,
    )
    print("Success.")


def handle_student_show(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    student = sms.get_student(args.student_id)
    print_student(student)


def handle_student_list(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    students = sms.list_students()
    print_students(students)


def handle_student_remove(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    sms.remove_student(args.student_id)
    print("Success.")


# -------------------------------------------------
# Teacher commands handlers
# -------------------------------------------------
def handle_teacher_add(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    sms.add_teacher(
        teacher_id=args.id,
        name=args.name,
    )
    print("Success.")


def handle_teacher_show(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    teacher = sms.get_teacher(args.teacher_id)
    print_teacher(teacher)


def handle_teacher_list(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    teachers = sms.list_teachers()
    print_teachers(teachers)


def handle_teacher_remove(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    sms.remove_teacher(args.teacher_id)
    print("Success.")


# -------------------------------------------------
# Course commands handlers
# -------------------------------------------------
def handle_course_add(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    sms.add_course(
        course_code=args.code,
        name=args.name,
    )
    print("Success.")


def handle_course_show(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    course = sms.get_course(args.course_code)
    print_course(course)


def handle_course_list(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    courses = sms.list_courses()
    print_courses(courses)


def handle_course_remove(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    sms.remove_course(args.course_code)
    print("Success.")


# -------------------------------------------------
# Cross-resource commands handlers
# -------------------------------------------------
def handle_enroll(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    sms.enroll_student_in_course(
        student_id=args.student,
        course_code=args.course,
    )
    print("Success.")


def handle_drop(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    sms.drop_student_from_course(
        student_id=args.student,
        course_code=args.course,
    )
    print("Success.")


def handle_assign_teacher(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    sms.assign_teacher_to_course(
        teacher_id=args.teacher,
        course_code=args.course,
    )
    print("Success.")


def handle_unassign_teacher(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    sms.unassign_teacher_from_course(args.course_code)
    print("Success.")


# -------------------------------------------------
# Grade commands handlers
# -------------------------------------------------
def handle_grade_assign(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    sms.assign_grade_to_student(
        student_id=args.student,
        course_code=args.course,
        value=args.value,
    )
    print("Success.")


def handle_grade_remove(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    sms.remove_grade_from_student(
        student_id=args.student,
        course_code=args.course,
    )
    print("Success.")


# -------------------------------------------------
# Dispatcher
# -------------------------------------------------
def dispatch(
        sms: "StudentManagementSystemAPI",
        args: argparse.Namespace,
) -> None:
    """
    Dispatch parsed arguments to the correct command handler.
    """
    match args.resource, getattr(args, "action", None):

        case "student", "add":
            handle_student_add(sms, args)
        case "student", "show":
            handle_student_show(sms, args)
        case "student", "list":
            handle_student_list(sms, args)
        case "student", "remove":
            handle_student_remove(sms, args)

        case "teacher", "add":
            handle_teacher_add(sms, args)
        case "teacher", "show":
            handle_teacher_show(sms, args)
        case "teacher", "list":
            handle_teacher_list(sms, args)
        case "teacher", "remove":
            handle_teacher_remove(sms, args)

        case "course", "add":
            handle_course_add(sms, args)
        case "course", "show":
            handle_course_show(sms, args)
        case "course", "list":
            handle_course_list(sms, args)
        case "course", "remove":
            handle_course_remove(sms, args)

        case "enroll", None:
            handle_enroll(sms, args)
        case "drop", None:
            handle_drop(sms, args)

        case "assign-teacher", None:
            handle_assign_teacher(sms, args)
        case "unassign-teacher", None:
            handle_unassign_teacher(sms, args)

        case "grade", "assign":
            handle_grade_assign(sms, args)
        case "grade", "remove":
            handle_grade_remove(sms, args)

        case _:
            # This should be unreachable if argparse is correct
            raise RuntimeError("Unhandled command")


# -------------------------------------------------
# Parser builder
# -------------------------------------------------

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

    parser.add_argument(
        "--version",
        action="version",
        version=f"sms {SMS_VERSION}",
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
    grade_assign.add_argument("--value", required=True, type=float)

    grade_remove = grade_subparsers.add_parser("remove", help="Remove a grade")
    grade_remove.add_argument("--student", required=True)
    grade_remove.add_argument("--course", required=True)

    return parser


# -------------------------------------------------
# Main entry point with scoped argparse handling
# -------------------------------------------------
def _require_canonical_sqlite_path_from_env() -> Path:
    raw = os.getenv("SMS_SQLITE_PATH")
    if raw is None or raw.strip() == "":
        raise ConfigurationError(
            "SMS_BACKEND=sqlite requires SMS_SQLITE_PATH to be explicitly set."
        )

    expanded = Path(raw).expanduser()

    # Reject relative paths BEFORE resolve()
    if not expanded.is_absolute():
        raise ConfigurationError(
            f"SMS_SQLITE_PATH must be an absolute path, got: {raw!r}"
        )

    # Canonicalize exactly once at the composition boundary
    return expanded.resolve()

def _build_persistence_config() -> PersistenceConfig:
    """
    Runtime persistence selection.

    Phase-6 verification override via environment variables.
    Default remains in-memory.
    """
    backend = os.getenv("SMS_BACKEND", "memory").strip().lower()

    if backend == "sqlite":
        sqlite_path = _require_canonical_sqlite_path_from_env()
        return PersistenceConfig(
            backend="sqlite",
            sqlite_path=sqlite_path,
        )

    return PersistenceConfig()


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()

    try:
        try:
            args = parser.parse_args(argv)

        except SystemExit as e:
            # argparse exits here -> usage error
            return EXIT_USAGE_ERROR if e.code != 0 else EXIT_SUCCESS

        config = _build_persistence_config()
        sms = create_sms(config)

        dispatch(sms, args)
        return EXIT_SUCCESS

    except Exception as exc:
        exit_code, message = render_error(exc)
        print(message)
        return exit_code

if __name__ == "__main__":
    sys.exit(main())



