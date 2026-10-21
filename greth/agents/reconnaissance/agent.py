"""Reconnaissance agent."""

from __future__ import annotations

from greth.agents.base import AgentBase


class ReconnaissanceAgent(AgentBase):
    name = "reconnaissance"

    def trigger(self, finding) -> bool:
        return finding.kind in {"TARGET_REGISTERED", "PORT_OPEN", "HTTP_ENDPOINT"}

    def handle(self, finding):
        return {
            "status": "recon_complete",
            "target": finding.target,
            "agent": self.name,
            "summary": f"Reconnaissance completed for {finding.target}",
        }
