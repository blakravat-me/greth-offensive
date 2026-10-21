"""Triage agent."""

from __future__ import annotations

from greth.agents.base import AgentBase


class TriageAgent(AgentBase):
    name = "triage"

    def trigger(self, finding) -> bool:
        return finding.kind in {"TARGET_REGISTERED", "HTTP_ENDPOINT", "TECHNOLOGY"}

    def handle(self, finding):
        return {
            "status": "triaged",
            "target": finding.target,
            "agent": self.name,
            "summary": f"Triage processed {finding.kind} on {finding.target}",
        }
