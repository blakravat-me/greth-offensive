"""Defense agent."""

from __future__ import annotations

from greth.agents.base import AgentBase


class DefenseAgent(AgentBase):
    name = "defense"

    def trigger(self, finding) -> bool:
        return finding.kind in {"SESSION", "AGENT_ERROR"}

    def handle(self, finding):
        return {"status": "defensive_response", "agent": self.name, "target": finding.target}
