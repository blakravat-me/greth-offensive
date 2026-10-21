"""Monitoring agent."""

from __future__ import annotations

from greth.agents.base import AgentBase


class MonitoringAgent(AgentBase):
    name = "monitoring"

    def trigger(self, finding) -> bool:
        return finding.kind in {"TARGET_REGISTERED", "VULNERABILITY", "SESSION", "CAMPAIGN_COMPLETE"}

    def handle(self, finding):
        return self.publish(
            kind="OBSERVATION",
            target=finding.target,
            payload={"observed": finding.kind},
            confidence=0.5,
            summary=f"Monitoring observed {finding.kind} on {finding.target}",
        )
