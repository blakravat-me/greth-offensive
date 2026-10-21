"""Triage agent: ranks, filters, deduplicates, and escalates relevant evidence."""

from __future__ import annotations

from greth.agents.base import AgentBase


class TriageAgent(AgentBase):
    name = "triage"

    def trigger(self, finding) -> bool:
        return finding.kind in {"HTTP_ENDPOINT", "TECHNOLOGY"}

    def handle(self, finding):
        signal = finding.payload.get("source") or finding.target
        if "login" in signal.lower() or "admin" in signal.lower() or "api" in signal.lower():
            return self.publish(
                kind="VULNERABILITY",
                target=finding.target,
                payload={"candidate": "auth_or_api_surface", "evidence": signal},
                confidence=0.72,
                summary=f"Probable sensitive API surface detected at {finding.target}",
            )
        return self.publish(
            kind="INTELLIGENCE",
            target=finding.target,
            payload={"note": "low-risk surface observed"},
            confidence=0.35,
            summary=f"Observed surface {finding.target} but not escalated",
        )
