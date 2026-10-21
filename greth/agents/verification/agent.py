"""Offense agent: converts high-confidence findings into exploit chains."""

from __future__ import annotations

from greth.agents.base import AgentBase


class OffenseAgent(AgentBase):
    name = "offense"

    def trigger(self, finding) -> bool:
        return finding.kind in {"VULNERABILITY", "EXPLOIT_CHAIN"}

    def handle(self, finding):
        payload = finding.payload or {}
        plan = [
            "enumerate input field / auth endpoint",
            "verify error path and response shape",
            "test for auth bypass / parameter tampering",
            "record evidence and prepare verification",
        ]
        return self.publish(
            kind="EXPLOIT_CHAIN",
            target=finding.target,
            payload={
                "plan": plan,
                "evidence": payload,
                "risk": "medium",
            },
            confidence=0.8,
            summary=f"Exploit chain drafted for {finding.target}",
        )
