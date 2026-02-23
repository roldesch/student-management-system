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
    Hermetic CLI subprocess runner (Safe Environment Merge).

    Characteristics:
    - Starts from a copy of the ambient environment (required for Windows stability).
    - Overrides only SMS-specific variables.
    - Requires explicit backend selection.
    - Requires explicit SQLite path when backend="sqlite".
    - Does not rely on implicit environment defaults for SMS configuration.
    """
    if backend not in {"memory", "sqlite"}:
        raise ValueError(f"Unsupported backend: {backend}")

    # ------------------------------------------------------------------
    # SAFE ENVIRONMENT BASELINE
    # ------------------------------------------------------------------
    #
    # We copy the full OS environment to preserve required system
    # variables (e.g., SystemDrive, TEMP, USERPROFILE on Windows).
    #
    # Starting from {} causes Windows path expansion issues and may
    # create literal directories like "%SystemDrive%".
    #
    # This preserves OS stability while still enforcing explicit
    # SMS configuration.
    # ------------------------------------------------------------------

    env = os.environ.copy()

    # ------------------------------------------------------------------
    # Explicit SMS configuration (override only what we control)
    # ------------------------------------------------------------------

    env["SMS_BACKEND"] = backend
    env["PYTHONIOENCODING"] = "utf-8"

    if backend == "sqlite":
        if sqlite_path is not None:
            # Pass path exactly as given (relative allowed for testing rejection)
            env["SMS_SQLITE_PATH"] = str(sqlite_path)
        else:
            # Explicitly ensure it is not set
            env.pop("SMS_SQLITE_PATH", None)
    else:
        # Ensure no accidental carry-over from outer environment
        env.pop("SMS_SQLITE_PATH", None)

    # ------------------------------------------------------------------
    # Execute CLI module
    # ------------------------------------------------------------------

    return subprocess.run(
        [sys.executable, "-m", "cli.main", *args],
        capture_output=True,
        text=True,
        env=env,
    )