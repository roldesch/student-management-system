# tests/cli/system/test_cli_sqlite_teacher_assignment_regression.py

from pathlib import Path

from tests.cli.subprocess._cli_runner import run_cli


def test_cli_sqlite_teacher_assignment_flow_succeeds(tmp_path: Path) -> None:
    # ------------------------------------------------------------------
    # Arrange
    # ------------------------------------------------------------------
    sqlite_path = tmp_path / "sms.db"
    assert not sqlite_path.exists()

    # Precondition setup through CLI
    add_course = run_cli(
        "course",
        "add",
        "--code",
        "C01",
        "--name",
        "Math",
        backend="sqlite",
        sqlite_path=sqlite_path,
    )

    add_teacher = run_cli(
        "teacher",
        "add",
        "--id",
        "T01",
        "--name",
        "Dr. Smith",
        backend="sqlite",
        sqlite_path=sqlite_path,
    )

    assert add_course.returncode == 0, add_course.stderr
    assert add_teacher.returncode == 0, add_teacher.stderr

    # ------------------------------------------------------------------
    # Act
    # ------------------------------------------------------------------
    assign_teacher = run_cli(
        "assign-teacher",
        "--teacher",
        "T01",
        "--course",
        "C01",
        backend="sqlite",
        sqlite_path=sqlite_path,
    )

    # ------------------------------------------------------------------
    # Assert
    # ------------------------------------------------------------------
    assert assign_teacher.returncode == 0, assign_teacher.stderr

    # Verify observable system state through CLI
    show_course = run_cli(
        "course",
        "show",
        "C01",
        backend="sqlite",
        sqlite_path=sqlite_path,
    )

    assert show_course.returncode == 0, show_course.stderr
    assert "T01" in show_course.stdout