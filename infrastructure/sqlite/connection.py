# infrastructure/sqlite/connection.py

import sqlite3
from pathlib import Path


def create_connection(db_path: Path) -> sqlite3.Connection:
    """
    Create a raw SQLite connection with required invariants applied.

    This function is low-level infrastructure only.

    Architectural ownership rules (LOCKED):
    - Connection lifecycle is owned by UnitOfWork.
    - Transaction management is owned by UnitOfWork.
    - Repositories must never open or close connections.
    - Repositories must never select transaction modes.
    - Repositories must treat the connection as externally owned and opaque.

    SQLite operational constraints enforced here:
    - Foreign key enforcement enabled (connection-scoped)
    - WAL journal mode asserted (idempotent, database-wide)
    - Busy timeout configured to avoid transient lock failures
    - No cross-thread connection sharing (explicitly enforced)

    Important (by design, DO NOT CHANGE here):
    - No transactions are started here.
    - No isolation levels are selected here.
    - No retry logic is implemented here.
    - No connection pooling is used.
    """

    conn = sqlite3.connect(
        db_path,
        detect_types=sqlite3.PARSE_DECLTYPES,
        check_same_thread=True,  # Explicit: SQLite connections are not shared across threads
    )

    # ------------------------------------------------------------
    # Connection-scoped invariants (must be applied per connection)
    # ------------------------------------------------------------

    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA busy_timeout = 5000;")

    # ------------------------------------------------------------
    # Database-wide invariant (idempotent; safe to execute always)
    # ------------------------------------------------------------

    conn.execute("PRAGMA journal_mode = WAL;")

    # ------------------------------------------------------------
    # Row handling
    # ------------------------------------------------------------

    conn.row_factory = sqlite3.Row

    return conn

