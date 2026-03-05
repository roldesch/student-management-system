# tests/integration/sqlite/test_sqlite_transaction_partial_write_rollback.py

import pytest
from pathlib import Path

from infrastructure.sqlite.bootstrap import initialize_sqlite_database
from infrastructure.sqlite.sqlite_transactional_sms import (
    SqliteTransactionalStudentManagementSystem,
)

from domain.exceptions.domain_exceptions import EnrollmentError


def test_sqlite_transaction_rolls_back_after_partial_write(tmp_path: Path) -> None:
    """
    Ensure that if an exception occurs after some repository writes
    inside a transaction, the entire transaction is rolled back.

    This protects against partial persistence when multiple writes
    occur within a single application operation.
    """

    # -------------------------------------------------
    # Arrange
    # -------------------------------------------------

    sqlite_path = tmp_path / "sms.db"
    initialize_sqlite_database(sqlite_path)

    sms = SqliteTransactionalStudentManagementSystem(sqlite_path)

    sms.add_student("S01", "Alice")
    sms.add_course("C01", "Math")

    sms.enroll_student_in_course("S01", "C01")

    # -------------------------------------------------
    # Act — failing write sequence
    # -------------------------------------------------

    with pytest.raises(EnrollmentError):
        # Second enrollment triggers domain error
        sms.enroll_student_in_course("S01", "C01")

    # -------------------------------------------------
    # Assert
    # -------------------------------------------------

    course = sms.get_course("C01")

    assert course.student_ids == ("S01",)