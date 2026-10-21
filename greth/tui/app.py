"""Terminal UI for Greth mission intake and swarm monitoring."""

from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from greth.core.blackboard import Blackboard
from greth.core.config import GrethConfig
from greth.core.models import Finding

console = Console()


class GrethTUI:
    """Simple terminal-based control surface for the swarm."""

    def __init__(self, blackboard: Blackboard, config: GrethConfig) -> None:
        self.blackboard = blackboard
        self.config = config

    def render_campaign_banner(self, target: str) -> None:
        console.print(
            Panel.fit(
                f"[bold cyan]Greth Offensive[/bold cyan]\n[green]Target:[/] {target}\n[green]Mission:[/] {self.config.mission}",
                title="Swarm Control",
                border_style="cyan",
            )
        )

    def render_summary(self, findings: list[Finding]) -> None:
        table = Table(title="Blackboard Findings")
        table.add_column("Agent")
        table.add_column("Kind")
        table.add_column("Target")
        table.add_column("Confidence")
        table.add_column("Summary")

        for finding in findings[-10:]:
            table.add_row(
                finding.agent,
                finding.kind,
                finding.target,
                f"{finding.confidence:.2f}",
                finding.summary[:80],
            )

        console.print(table)

    def prompt_mission(self) -> str:
        console.print(Panel.fit("Type your mission and press Enter.", title="Mission Intake"))
        mission = console.input("[bold yellow]Mission > [/bold yellow]")
        mission = mission.strip()
        if mission:
            self.config.mission = mission
        return mission or self.config.mission

    def render_status(self, status: str) -> None:
        console.print(f"[bold blue]Campaign status:[/] {status}")
