"""Defense agent."""

from __future__ import annotations

from greth.agents.base import AgentBase


class DefenseAgent(AgentBase):
    name = "defense"

    def trigger(self, finding) -> bool:
        return finding.kind in {"AGENT_ERROR", "OBSERVATION"}

    def handle(self, finding):
        return self.publish(
            kind="COUNTERMEASURE",
            target=finding.target,
            payload={"response": "contain and fallback"},
            confidence=0.4,
            summary=f"Defense logic engaged for {finding.target}",
        )
