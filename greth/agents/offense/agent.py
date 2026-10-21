"""Offense agent."""

from __future__ import annotations

from greth.agents.base import AgentBase


class OffenseAgent(AgentBase):
    name = "offense"

    def trigger(self, finding) -> bool:
        return finding.kind in {"VULNERABILITY", "EXPLOIT_CHAIN"}

    def handle(self, finding):
        return {
            "status": "exploit_path_ready",
            "target": finding.target,
            "agent": self.name,
            "summary": f"Offense actor prepared an exploitation path for {finding.target}",
        }
