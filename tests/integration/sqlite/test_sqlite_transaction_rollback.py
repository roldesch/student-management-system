# pytest tests/integration/sqlite/test_sqlite_transaction_rollback.py

import pytest
from pathlib import Path

from domain.exceptions.domain_exceptions import EnrollmentError

from infrastructure.sqlite.bootstrap import initialize_sqlite_database
from infrastructure.sqlite.sqlite_transactional_sms import (
    SqliteTransactionalStudentManagementSystem,
)


def test_sqlite_transaction_rolls_back_on_domain_error(tmp_path: Path) -> None:
    """
    Ensure that a failing write operation does not leave partial
    persistence changes in the SQLite database.
    """

    # -------------------------------------------------
    # Arrange
    # -------------------------------------------------

    sqlite_path = tmp_path / "sms.db"

    # Composition root responsibility
    initialize_sqlite_database(sqlite_path)

    sms = SqliteTransactionalStudentManagementSystem(sqlite_path)

    sms.add_student("S01", "Alice")
    sms.add_course("C01", "Math")

    # -------------------------------------------------
    # Act — successful write
    # -------------------------------------------------

    sms.enroll_student_in_course("S01", "C01")

    # -------------------------------------------------
    # Act — failing write
    # -------------------------------------------------

    with pytest.raises(EnrollmentError):
        sms.enroll_student_in_course("S01", "C01")

    # -------------------------------------------------
    # Assert
    # -------------------------------------------------

    course = sms.get_course("C01")

    assert course.student_ids == ("S01",)