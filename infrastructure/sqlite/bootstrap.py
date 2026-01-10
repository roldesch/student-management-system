# infrastructure/sqlite/bootstrap.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sqlite3


@dataclass(frozen=True, slots=True)
class SqliteBootstrapConfig:
    """
    Infrastructure-only configuration for SQLite initialization.
    """
    busy_timeout_ms: int = 5000


def initialize_sqlite_database(
    db_path: str | Path,
    *,
    config: SqliteBootstrapConfig = SqliteBootstrapConfig(),
) -> None:
    """
    Idempotently initializes the SQLite database and enforces required pragmas.

    Guardrails:
    - Infrastructure-only (no domain imports, no repositories, no application logic)
    - Deterministic schema application
    - No migrations or version branching
    """
    db_path = Path(db_path)

    schema_path = Path(__file__).with_name("schema.sql")
    schema_sql = schema_path.read_text(encoding="utf-8")

    conn = sqlite3.connect(db_path)
    try:
        _apply_required_pragmas(conn, config=config)
        _apply_schema(conn, schema_sql)
    finally:
        conn.close()


def _apply_required_pragmas(
    conn: sqlite3.Connection,
    *,
    config: SqliteBootstrapConfig,
) -> None:
    # 1) Enforce WAL journal mode
    journal_mode = conn.execute("PRAGMA journal_mode = WAL;").fetchone()
    if not journal_mode or str(journal_mode[0]).lower() != "wal":
        raise RuntimeError(f"Failed to enable WAL journal_mode. Got: {journal_mode!r}")

    # 2) Enforce foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON;")
    fk_status = conn.execute("PRAGMA foreign_keys;").fetchone()
    if not fk_status or int(fk_status[0]) != 1:
        raise RuntimeError(f"Failed to enable foreign_keys. Got: {fk_status!r}")

    # 3) Configure busy timeout
    if config.busy_timeout_ms < 0:
        raise ValueError("busy_timeout_ms must be >= 0")
    conn.execute(f"PRAGMA busy_timeout = {int(config.busy_timeout_ms)};")


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
