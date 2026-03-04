# tests/contracts/application/test_sqlite_proxy_write_classification.py

import inspect

from application.services.student_management_system import StudentManagementSystem
from infrastructure.sqlite.sqlite_transactional_sms import (
    SqliteTransactionalStudentManagementSystem,
)


def _extract_public_methods(cls):
    """
    Extract public methods defined directly on the class body.
    """

    methods = {}

    for name, member in cls.__dict__.items():

        if name.startswith("_"):
            continue

        if inspect.isfunction(member):
            fn = member
        elif isinstance(member, staticmethod):
            fn = member.__func__
        elif isinstance(member, classmethod):
            fn = member.__func__
        else:
            continue

        fn = inspect.unwrap(fn)
        methods[name] = fn

    return methods


def test_write_methods_reference_valid_operations():
    """
    Ensure every method listed in _WRITE_METHODS exists
    in the StudentManagementSystem public API.
    """

    # -------------------------------------------------
    # Arrange
    # -------------------------------------------------
    public_methods = set(_extract_public_methods(StudentManagementSystem))
    write_methods = SqliteTransactionalStudentManagementSystem.__dict__["_WRITE_METHODS"]
    # -------------------------------------------------
    # Act
    # -------------------------------------------------
    missing = write_methods - public_methods

    # -------------------------------------------------
    # Assert
    # -------------------------------------------------
    assert not missing, (
        "\n_WRITE_METHODS references methods that do not exist "
        "in StudentManagementSystem:\n"
        f"{sorted(missing)}"
    )


def test_command_methods_are_explicitly_classified_as_writes():
    """
    Ensure command methods (those returning None)
    are explicitly listed in _WRITE_METHODS.

    This prevents new mutating operations from silently
    defaulting to read transactions.
    """

    # -------------------------------------------------
    # Arrange
    # -------------------------------------------------
    public_methods = _extract_public_methods(StudentManagementSystem)
    write_methods = SqliteTransactionalStudentManagementSystem.__dict__["_WRITE_METHODS"]
    commands = set()

    for name, fn in public_methods.items():

        sig = inspect.signature(fn)
        return_annotation = sig.return_annotation

        if return_annotation is inspect.Signature.empty:
            continue

        if return_annotation in (None, type(None)):
            commands.add(name)

    # -------------------------------------------------
    # Act
    # -------------------------------------------------
    unclassified = commands - write_methods

    # -------------------------------------------------
    # Assert
    # -------------------------------------------------
    assert not unclassified, (
        "\nCommand methods returning None must be listed "
        "in _WRITE_METHODS:\n"
        f"{sorted(unclassified)}"
    )