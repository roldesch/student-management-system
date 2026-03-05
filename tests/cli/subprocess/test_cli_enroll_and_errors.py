# tests/cli/subprocess/test_cli_enroll_and_errors.py

from tests.cli.subprocess._cli_runner import run_cli


def test_student_add_validation_error(tmp_path):
    db_path = tmp_path / "sms.db"

    result = run_cli(
        "student", "add",
        "--id", "",
        "--name", "Alice",
        backend="sqlite",
        sqlite_path=db_path,
    )

    assert result.returncode == 2

    combined = (result.stdout + result.stderr).lower()
    assert "invalid input" in combined


def test_enroll_fails_when_entities_do_not_exist(tmp_path):
    db_path = tmp_path / "sms.db"

    result = run_cli(
        "enroll",
        "--student", "S01",
        "--course", "C01",
        backend="sqlite",
        sqlite_path=db_path,
    )

    assert result.returncode == 4

    combined = (result.stdout + result.stderr).lower()
    assert "state" in combined or "not found" in combined
