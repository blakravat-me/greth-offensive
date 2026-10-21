"""Bash / command execution capability for Greth."""

from __future__ import annotations

import subprocess
from typing import Any


class TerminalTool:
    """Simple shell wrapper with read-only operational defaults."""

    def run(self, command: str, timeout: int = 30) -> dict[str, Any]:
        completed = subprocess.run(
            ["bash", "-lc", command],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "command": command,
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
            "ok": completed.returncode == 0,
        }


TERMINAL = TerminalTool()
