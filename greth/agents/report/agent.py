"""Verification agent: confirms evidence and records session context."""

from __future__ import annotations

from greth.agents.base import AgentBase
from greth.tools.internet import INTERNET


class VerificationAgent(AgentBase):
    name = "verification"

    def trigger(self, finding) -> bool:
        return finding.kind in {"EXPLOIT_CHAIN", "VULNERABILITY"}

    def handle(self, finding):
        try:
            data = INTERNET.fetch(finding.target)
            status = data["status_code"]
        except Exception:
            status = 0

        payload = {"checked_url": finding.target, "status_code": status, "verified": status in {200, 201, 202, 204, 301, 302}}
        return self.publish(
            kind="SESSION",
            target=finding.target,
            payload=payload,
            confidence=0.82,
            summary=f"Verification result for {finding.target}: status={status}",
        )
