# infrastructure/sqlite/bootstrap.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sqlite3

from infrastructure.sqlite.connection import create_connection


@dataclass(frozen=True, slots=True)
class SqliteBootstrapConfig:
    """
    Infrastructure-only configuration for SQLite initialization.

    Note:
    - create_connection() is the single source of truth for setting invariants.
    - This config is retained to preserve bootstrap-time verification semantics
      and to keep tests explicit and stable.
    """
    busy_timeout_ms: int = 5000


def initialize_sqlite_database(
    db_path: str | Path,
    *,
    config: SqliteBootstrapConfig = SqliteBootstrapConfig(),
) -> None:
    """
    Idempotently initializes the SQLite database and verifies required invariants.

    Guardrails:
    - Infrastructure-only (no domain imports, no repositories, no application logic)
    - Deterministic schema application
    - No migrations or version branching
    - Transaction boundaries owned only for schema application
    - Connection invariants are *set* exclusively by create_connection()
      and *verified* here for deterministic bootstrap behavior.
    """
    # Canonicalize path and ensure parent directory exists
    db_path = Path(db_path).expanduser().resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Load schema
    schema_path = Path(__file__).with_name("schema.sql")
    schema_sql = schema_path.read_text(encoding="utf-8")

    # Use canonical connection factory (must match runtime invariants)
    conn = create_connection(db_path)
    try:
        _verify_required_pragmas(conn, config=config)
        _apply_schema(conn, schema_sql)
    finally:
        conn.close()


def _verify_required_pragmas(
    conn: sqlite3.Connection,
    *,
    config: SqliteBootstrapConfig,
) -> None:
    """
    Verifies invariants that must hold after create_connection().

    Important:
    - This function must not *set* invariants (single ownership belongs to
      create_connection()).
    - It may validate and fail fast to make bootstrap deterministic and to
      satisfy infrastructure tests.
    """
    # 1) Verify WAL journal mode
    journal_mode = conn.execute("PRAGMA journal_mode;").fetchone()
    if not journal_mode or str(journal_mode[0]).lower() != "wal":
        raise RuntimeError(f"Failed to enable WAL journal_mode. Got: {journal_mode!r}")

    # 2) Verify foreign key constraints
    fk_status = conn.execute("PRAGMA foreign_keys;").fetchone()
    if not fk_status or int(fk_status[0]) != 1:
        raise RuntimeError(f"Failed to enable foreign_keys. Got: {fk_status!r}")

    # 3) Verify busy timeout
    if config.busy_timeout_ms < 0:
        raise ValueError("busy_timeout_ms must be >= 0")

    busy = conn.execute("PRAGMA busy_timeout;").fetchone()
    # SQLite returns busy_timeout in milliseconds.
    if not busy or int(busy[0]) != int(config.busy_timeout_ms):
        raise RuntimeError(
            f"Failed to set busy_timeout. Expected: {int(config.busy_timeout_ms)} "
            f"Got: {busy!r}"
        )


def _apply_schema(conn: sqlite3.Connection, schema_sql: str) -> None:
    """
    Applies schema.sql atomically.

    Notes:
    - Transaction boundaries are owned by this function, not by schema.sql.
    - schema.sql must not contain BEGIN or COMMIT statements.
    """
    try:
        conn.executescript(schema_sql)
        conn.commit()
    except Exception:
        try:
            conn.rollback()
        except Exception:
            pass
        raise