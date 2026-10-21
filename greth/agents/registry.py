"""Chaining agent."""

from __future__ import annotations

from greth.agents.base import AgentBase


class ChainingAgent(AgentBase):
    name = "chaining"

    def trigger(self, finding) -> bool:
        return finding.kind in {"NORMALIZED_FINDING", "VULNERABILITY", "EXPLOIT_CHAIN"}

    def handle(self, finding):
        return self.publish(
            kind="CHAINED_ACTION",
            target=finding.target,
            payload={"chain": [finding.kind, "follow-up-check"]},
            confidence=0.7,
            summary=f"Chain assembled for {finding.target}",
        )
