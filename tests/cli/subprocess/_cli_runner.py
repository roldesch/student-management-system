# tests/cli/subprocess/_cli_runner.py

import subprocess
import sys

def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "cli.main", *args],
        capture_output=True,
        text=True,
    )