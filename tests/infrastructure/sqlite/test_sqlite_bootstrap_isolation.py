from pathlib import Path

from infrastructure.sqlite.bootstrap import initialize_sqlite_database
from infrastructure.sqlite.sqlite_transactional_sms import (
    SqliteTransactionalStudentManagementSystem,
)


def test_sqlite_transactional_proxy_instantiation_does_not_create_db_file(
    tmp_path: Path,
) -> None:
    """
    Instantiating the transactional proxy must NOT create a database file.

    Bootstrap ownership belongs exclusively to the composition root.
    """

    db_path = tmp_path / "should_not_exist.db"
    assert not db_path.exists()

    # Act — instantiate only
    _ = SqliteTransactionalStudentManagementSystem(sqlite_path=db_path)

    # Assert — file must still not exist
    assert not db_path.exists()


def test_bootstrap_creates_database_file_explicitly(tmp_path: Path) -> None:
    """
    Database file must be created only when bootstrap is invoked explicitly.
    """

    db_path = tmp_path / "created_by_bootstrap.db"
    assert not db_path.exists()

    # Act
    initialize_sqlite_database(db_path)

    # Assert
    assert db_path.exists()
    assert db_path.is_file()