"""Engineering agent."""

from __future__ import annotations

from greth.agents.base import AgentBase


class EngineeringAgent(AgentBase):
    name = "engineering"

    def trigger(self, finding) -> bool:
        return finding.kind in {"TARGET_REGISTERED", "REPORT"}

    def handle(self, finding):
        return {"status": "engineered", "agent": self.name, "target": finding.target}
