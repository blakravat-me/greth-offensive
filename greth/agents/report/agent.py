"""Report agent."""

from __future__ import annotations

from greth.agents.base import AgentBase


class ReportAgent(AgentBase):
    name = "report"

    def trigger(self, finding) -> bool:
        return finding.kind in {"TARGET_REGISTERED", "VULNERABILITY", "CAMPAIGN_COMPLETE"}

    def handle(self, finding):
        return {
            "status": "reported",
            "target": finding.target,
            "agent": self.name,
            "summary": f"Report generated for {finding.target}",
        }
