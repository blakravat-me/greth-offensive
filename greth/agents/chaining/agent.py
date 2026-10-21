"""Chaining agent."""

from __future__ import annotations

from greth.agents.base import AgentBase


class ChainingAgent(AgentBase):
    name = "chaining"

    def trigger(self, finding) -> bool:
        return finding.kind in {"VULNERABILITY", "EXPLOIT_CHAIN"}

    def handle(self, finding):
        return {"status": "chain_built", "agent": self.name, "target": finding.target}
