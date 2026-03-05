# infrastructure/sqlite/unit_of_work.py

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from infrastructure.sqlite.connection import create_connection
from infrastructure.sqlite.errors import (
    PersistenceError,
    ConcurrentUpdateError,
)


class UnitOfWork:
    """
    SQLite Unit of Work.

    Responsibilities (LOCKED):
    - Own exactly one SQLite connection
    - Own transaction lifecycle (BEGIN / COMMIT / ROLLBACK)
    - Select transaction start mode (read vs write)
    - Guarantee atomicity per application use case

    Architectural constraints:
    - One UnitOfWork per application service invocation
    - No nested UnitOfWork instances
    - Repositories must not manage transaction or connections
    - Repositories must not influence transaction mode

    IMPORTANT:
    A read-only UnitOfWork does NOT enforce immutability at the SQLite level.
    Correctness relies on repository discipline.
    """

    def __init__(self, db_path: Path, *, write: bool) -> None:
        """
        Create a UnitOfWork.

        Args:
            db_path: Path to the SQLite database file.
            write: Whether this UnitOfWork performs write operations.
                - False -> read-oriented (BEGIN)
                - True -> write-capable (BEGIN IMMEDIATE)
        """
        self._db_path = db_path
        self._write = write

        self._connection: Optional[sqlite3.Connection] = None
        self._active: bool = False


    # ------------------------------------------------------------
    # Context manager protocol
    # ------------------------------------------------------------

    def __enter__(self) -> "UnitOfWork":
        if self._active:
            raise PersistenceError(
                "UnitOfWork instances must not be re-entered."
            )

        self._connection = create_connection(self._db_path)

        try:
            self._active = True     # must be true once BEGIN may succeed
            self._begin_transaction()
        except sqlite3.OperationalError as exc:
            self._active = False
            self._safe_close()
            raise self._translate_operational_error(exc) from exc

        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if not self._active or self._connection is None:
            return

        try:
            if exc_type is None:
                try:
                    self._connection.commit()
                except sqlite3.Error as exc:
                    # Commit failure must be treated as rollback-required
                    self._connection.rollback()
                    raise PersistenceError("SQLite commit failed.") from exc
            else:
                self._connection.rollback()
        finally:
            self._safe_close()
            self._active = False

    # ------------------------------------------------------------
    # Public accessors
    # ------------------------------------------------------------

    @property
    def connection(self) -> sqlite3.Connection:
        """
        Access the transaction-bound SQLite connection.

        Repositories receive this connection and must treat is as:
        - externally owned
        - opaque
        - already inside an active transaction
        """
        if not self._active or self._connection is None:
            raise PersistenceError(
                "Connection accessed outside of active UnitOfWork."
            )
        return self._connection


    # ------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------

    def _begin_transaction(self) -> None:
        """
        Explicitly start the SQLite transaction.

        Transaction semantics (LOCKED):
        - Read-oriented UnitOfWork -> BEGIN
        - Write-capable UnitOfWork -> BEGIN IMMEDIATE
        """
        assert self._connection is not None

        if self._write:
            self._connection.execute("BEGIN IMMEDIATE;")
        else:
            self._connection.execute("BEGIN;")


    def _safe_close(self) -> None:
        """
        Close the SQLite connection safely.
        """
        try:
            if self._connection is not None:
                self._connection.close()
        finally:
            self._connection = None


    @staticmethod
    def _translate_operational_error(
            exc: sqlite3.OperationalError,
    ) -> PersistenceError:
        """
        Translate SQLite OperationalError into a stable persistence error.
        """
        message = str(exc).lower()

        if "database is locked" in message or "database is busy" in message:
            return ConcurrentUpdateError(
                "SQLite database is locked or busy."
            )

        return PersistenceError("Unexpected SQLite operational error.")
