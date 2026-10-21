"""Scheduler and campaign orchestration."""

from __future__ import annotations

from typing import Iterable

from greth.core.blackboard import Blackboard
from greth.core.config import GrethConfig
from greth.core.graph import build_graph
from greth.core.models import CampaignState, Finding


class CampaignScheduler:
    """Simple scheduler that boots a LangGraph campaign."""

    def __init__(self, *, graph, config: GrethConfig) -> None:
        self.graph = graph
        self.config = config
        self.blackboard = Blackboard()
        self.state = CampaignState(target=config.target)

    def run(self) -> CampaignState:
        self.state.status = "running"
        bootstrap = Finding(
            campaign_id=self.state.campaign_id,
            agent="system",
            kind="TARGET_REGISTERED",
            target=self.config.target,
            payload={"mode": self.config.mode},
            confidence=1.0,
            summary=f"Campaign target registered: {self.config.target}",
        )
        self.blackboard.write(bootstrap, topic="TARGET_REGISTERED")

        try:
            result = self.graph.invoke({"target": self.config.target, "campaign": self.state})
        except Exception as exc:  # pragma: no cover - runtime safety
            self.state.status = f"error: {exc}"
            raise

        self.state.status = "completed"
        self.state.findings = list(self.blackboard.all())
        return self.state
