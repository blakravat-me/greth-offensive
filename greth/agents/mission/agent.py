"""Mission intake agent that receives user text and posts it to the board."""

from __future__ import annotations

from greth.agents.base import AgentBase
from greth.core.models import Finding


class MissionAgent(AgentBase):
    """Accept mission text from UI and push it to the swarm blackboard."""

    name = "mission"

    def trigger(self, finding: Finding) -> bool:
        return finding.kind in {"TARGET_REGISTERED", "MISSION_SUBMITTED"}

    def handle(self, finding: Finding):
        target = finding.target
        mission_text = str(finding.payload.get("mission", "")).strip()
        if not mission_text:
            mission_text = "Assess the target and identify likely attack paths."
        return self.publish(
            kind="MISSION_ACCEPTED",
            target=target,
            payload={"mission": mission_text, "source": "ui"},
            confidence=1.0,
            summary=f"Mission accepted for {target}: {mission_text[:140]}",
        )
