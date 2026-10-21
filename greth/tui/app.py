"""Terminal dashboard for the swarm."""

from __future__ import annotations

from collections import Counter

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from greth.core.models import Finding


class ConsoleUI:
    """Text-based dashboard for swarm state and findings."""

    def __init__(self) -> None:
        self.console = Console()

    def render_campaign_banner(self, target: str) -> None:
        self.console.print(Panel.fit(f"[bold green]Greth Offensive[/bold green]\nTarget: {target}", title="Campaign"))

    def render_blackboard(self, findings: list[Finding]) -> None:
        table = Table(title="Blackboard Feed")
        table.add_column("Agent", style="cyan")
        table.add_column("Kind", style="magenta")
        table.add_column("Severity", style="yellow")
        table.add_column("Target")
        table.add_column("Summary")
        for finding in findings[-10:]:
            table.add_row(finding.agent, finding.kind, finding.severity, finding.target, finding.summary)
        self.console.print(table)

    def render_summary(self, findings: list[Finding]) -> None:
        severity_counts = Counter(finding.severity for finding in findings)
        table = Table(title="Campaign Overview")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Total findings", str(len(findings)))
        table.add_row("Critical", str(severity_counts.get("critical", 0)))
        table.add_row("High", str(severity_counts.get("high", 0)))
        table.add_row("Medium", str(severity_counts.get("medium", 0)))
        table.add_row("Low", str(severity_counts.get("low", 0)))
        self.console.print(table)
        self.render_blackboard(findings)
