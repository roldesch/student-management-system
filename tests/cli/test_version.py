import subprocess
import sys


def test_sms_version():
    """
    Phase 0 contract test:
    - `sms --version` must succeed
    - Must print the current version
    - Must exit with code 0
    """

    result = subprocess.run(
        [sys.executable, "-m", "cli.main", "--version"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "sms 1.0.0" in result.stdout
