"""Compaction agent."""

from __future__ import annotations

from greth.agents.base import AgentBase


class CompactionAgent(AgentBase):
    name = "compaction"

    def trigger(self, finding) -> bool:
        return finding.kind in {"VULNERABILITY", "SESSION"}

    def handle(self, finding):
        return {"status": "compacted", "agent": self.name, "target": finding.target}
