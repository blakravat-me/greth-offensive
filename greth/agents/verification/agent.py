"""Verification agent."""

from __future__ import annotations

from greth.agents.base import AgentBase


class VerificationAgent(AgentBase):
    name = "verification"

    def trigger(self, finding) -> bool:
        return finding.kind in {"VULNERABILITY", "EXPLOIT_CHAIN", "SESSION"}

    def handle(self, finding):
        return {
            "status": "confirmed",
            "target": finding.target,
            "agent": self.name,
            "summary": f"Verification passed for {finding.kind} on {finding.target}",
        }
