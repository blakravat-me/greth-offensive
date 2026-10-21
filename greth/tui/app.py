"""TUI shell placeholder for monitoring."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table


class ConsoleTUI:
    """Minimal console output for local monitoring."""

    def __init__(self) -> None:
        self.console = Console()

    def render(self, findings: list) -> None:
        table = Table(title="Greth Campaign")
        table.add_column("Agent")
        table.add_column("Kind")
        table.add_column("Target")
        for item in findings:
            table.add_row(item.agent, item.kind, item.target)
        self.console.print(table)
