"""Compaction agent."""

from __future__ import annotations

from greth.agents.base import AgentBase


class CompactionAgent(AgentBase):
    name = "compaction"

    def trigger(self, finding) -> bool:
        return finding.kind in {"INTELLIGENCE", "OPERATIONS", "COUNTERMEASURE"}

    def handle(self, finding):
        return self.publish(
            kind="NORMALIZED_FINDING",
            target=finding.target,
            payload={"compressed": True},
            confidence=0.66,
            summary=f"Compacted output for {finding.target}",
        )
