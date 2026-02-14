# tests/cli/subprocess/_cli_runner.py

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

def run_cli(
    *args: str,
    backend: str,
    sqlite_path: Optional[Path] = None,
) -> subprocess.CompletedProcess[str]:
    """
    Hermetic CLI subprocess runner.

    - Does NOT inherit ambient environment.
    - Requires explicit backend selection.
    - Requires explicit SQLite path when backend="sqlite".
    """
    if backend not in {"memory", "sqlite"}:
        raise ValueError(f"Unsupported backend: {backend}")

    # Minimal required environment
    env = {
        "SMS_BACKEND": backend,
        "PYTHONIOENCODING": "utf-8",
    }

    for key in ("PATH", "SYSTEMROOT", "COMSPEC"):
        if key in os.environ:
            env[key] = os.environ[key]

    # Preserve PYTHONPATH only if needed for module resolution
    if "PYTHONPATH" in os.environ:
        env["PYTHONPATH"] = os.environ["PYTHONPATH"]

    if backend == "sqlite":
        if sqlite_path is None:
            raise ValueError("sqlite_path is required when backend='sqlite'")
        env["SMS_SQLITE_PATH"] = str(sqlite_path)

    return subprocess.run(
        [sys.executable, "-m", "cli.main", *args],
        capture_output=True,
        text=True,
        env=env,
    )