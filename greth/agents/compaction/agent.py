"""Engineering agent."""

from __future__ import annotations

from greth.agents.base import AgentBase


class EngineeringAgent(AgentBase):
    name = "engineering"

    def trigger(self, finding) -> bool:
        return finding.kind in {"TECHNOLOGY", "COUNTERMEASURE"}

    def handle(self, finding):
        return self.publish(
            kind="OPERATIONS",
            target=finding.target,
            payload={"action": "stabilize workflow"},
            confidence=0.45,
            summary=f"Engineering control plan for {finding.target}",
        )
