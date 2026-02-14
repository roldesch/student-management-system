# tests/cli/subprocess/test_cli_student_commands.py


from tests.cli.subprocess._cli_runner import run_cli


def test_student_add_success(tmp_path):
    db_path = tmp_path / "sms.db"

    result = run_cli(
        "student", "add",
        "--id", "S01",
        "--name", "Alice",
        backend="sqlite",
        sqlite_path=db_path,
    )

    assert result.returncode == 0
    assert "success" in (result.stdout + result.stderr).lower()


def test_student_show_not_found(tmp_path):
    db_path = tmp_path / "sms.db"

    result = run_cli(
        "student", "show", "S01",
        backend="sqlite",
        sqlite_path=db_path,
    )

    assert result.returncode == 4

    combined = (result.stdout + result.stderr).lower()
    assert "state" in combined or "not found" in combined