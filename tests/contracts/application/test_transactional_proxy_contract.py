# tests/contracts/application/test_transactional_proxy_contract.py

import inspect

from application.services.student_management_system import StudentManagementSystem
from infrastructure.sqlite.sqlite_transactional_sms import (
    SqliteTransactionalStudentManagementSystem,
)


# ---------------------------------------------------------
# Public API extraction
# ---------------------------------------------------------

def _extract_public_methods(cls: type) -> dict[str, inspect.Signature]:
    """
    Extract public methods defined directly on the class.

    Rules:
    - Only inspect cls.__dict__
    - Ignore private methods (_ prefix)
    - Handle function / staticmethod / classmethod
    - Ignore inherited members

    Important:
    Only functions defined directly in the class body are included.
    Descriptors such as properties or cached_property are intentionally
    excluded because the application boundary exposes *methods only*.
    """

    methods: dict[str, inspect.Signature] = {}

    for name, member in cls.__dict__.items():

        if name.startswith("_"):
            continue

        fn = None

        if inspect.isfunction(member):
            fn = member
        elif isinstance(member, staticmethod):
            fn = member.__func__
        elif isinstance(member, classmethod):
            fn = member.__func__

        if fn is None:
            continue

        fn = inspect.unwrap(fn)

        methods[name] = inspect.signature(fn)

    return methods


# ---------------------------------------------------------
# Signature normalization
# ---------------------------------------------------------

def _normalize_signature(sig: inspect.Signature) -> list[tuple]:
    """
    Normalize signature for comparison.

    Rules:
    - Remove first parameter if self or cls
    - Compare name/kind/default only
    - Ignore annotations

    Parameter names are intentionally compared.
    The proxy must mirror the application service signature exactly.
    """

    params = list(sig.parameters.values())

    if params and params[0].name in ("self", "cls"):
        params = params[1:]

    normalized = []

    for p in params:
        normalized.append((p.name, p.kind, p.default))

    return normalized


# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------

def test_sqlite_proxy_api_name_parity():
    """
    Ensure the SQLite proxy exposes exactly the same
    public API as StudentManagementSystem.
    """

    # Arrange
    sms_methods = set(_extract_public_methods(StudentManagementSystem).keys())

    proxy_methods = set(
        _extract_public_methods(SqliteTransactionalStudentManagementSystem).keys()
    )

    # Act
    missing = sms_methods - proxy_methods
    extra = proxy_methods - sms_methods

    # Assert
    assert sms_methods == proxy_methods, (
        "\nAPI parity violation\n"
        "\nMissing methods in SQLite proxy:\n"
        f"{sorted(missing)}\n"
        "\nUnexpected extra proxy methods:\n"
        f"{sorted(extra)}"
    )


def test_sqlite_proxy_api_signature_parity():
    """
    Ensure proxy methods match StudentManagementSystem
    signatures exactly.
    """

    # Arrange
    sms_methods = _extract_public_methods(StudentManagementSystem)

    proxy_methods = _extract_public_methods(
        SqliteTransactionalStudentManagementSystem
    )

    # Act / Assert
    for name in sorted(sms_methods):

        assert name in proxy_methods, (
            f"Proxy missing method '{name}' "
            "(name parity test should have caught this)"
        )

        sms_sig = _normalize_signature(sms_methods[name])
        proxy_sig = _normalize_signature(proxy_methods[name])

        assert sms_sig == proxy_sig, (
            f"\nSignature mismatch for method '{name}'\n"
            f"\nNormalized SMS: {sms_sig}"
            f"\nNormalized Proxy: {proxy_sig}"
            f"\n\nRaw SMS: {sms_methods[name]}"
            f"\nRaw Proxy: {proxy_methods[name]}"
        )