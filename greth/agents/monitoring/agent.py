"""Monitoring agent."""

from __future__ import annotations

from greth.agents.base import AgentBase


class MonitoringAgent(AgentBase):
    name = "monitoring"

    def trigger(self, finding) -> bool:
        return True

    def handle(self, finding):
        return {"status": "observed", "agent": self.name, "target": finding.target}
