"""Terminal execution wrappers with allowlist and safe defaults."""

from __future__ import annotations

import shlex
import subprocess
from typing import Any

from greth.tools.base import BaseTool


class TerminalTool(BaseTool):
    """Structured shell execution adapter with safety constraints."""

    name = "terminal"

    def __init__(self, *, allowed_commands: list[str] | None = None, timeout: int = 30, retries: int = 1) -> None:
        self.allowed_commands = set((allowed_commands or [
            "curl",
            "nmap",
            "ffuf",
            "nuclei",
            "httpx",
            "amass",
            "sqlmap",
            "dnsrecon",
            "gobuster",
            "python",
            "bash",
            "sh",
        ]))
        self.timeout = timeout
        self.retries = retries

    def _validate(self, command: str) -> list[str]:
        if not command or not command.strip():
            raise ValueError("Empty command")
        parts = shlex.split(command)
        if not parts:
            raise ValueError("No executable found in command")
        binary = parts[0]
        if binary not in self.allowed_commands:
            raise ValueError(f"Command not allowed: {binary}")
        if any(token in command for token in (";", "&&", "||", "$(", "`")):
            raise ValueError("Unsafe shell chaining is forbidden")
        return parts

    def run(self, command: str, timeout: int | None = None, retries: int | None = None) -> dict[str, Any]:
        validated = self._validate(command)
        effective_timeout = timeout or self.timeout
        effective_retries = retries if retries is not None else self.retries
        last_result: dict[str, Any] | None = None

        for attempt in range(max(1, effective_retries + 1)):
            completed = subprocess.run(
                validated,
                capture_output=True,
                text=True,
                timeout=effective_timeout,
                check=False,
            )
            last_result = {
                "command": command,
                "argv": validated,
                "returncode": completed.returncode,
                "stdout": completed.stdout.strip(),
                "stderr": completed.stderr.strip(),
                "ok": completed.returncode == 0,
                "attempt": attempt + 1,
            }
            if completed.returncode == 0:
                return last_result
            if attempt < effective_retries:
                continue
        return last_result or {"command": command, "argv": validated, "returncode": 1, "stdout": "", "stderr": "", "ok": False}


TERMINAL = TerminalTool()
