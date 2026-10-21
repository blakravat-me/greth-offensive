"""Scheduler and campaign orchestration."""

from __future__ import annotations

from typing import Any

from greth.agents.registry import AGENT_REGISTRY
from greth.core.blackboard import Blackboard
from greth.core.config import GrethConfig, load_config
from greth.core.models import CampaignState, Finding
from greth.tui.app import GrethTUI


class CampaignScheduler:
    """Reactive swarm scheduler using a blackboard + trigger loop."""

    def __init__(self, *, config: GrethConfig, blackboard: Blackboard | None = None, ui: Any | None = None) -> None:
        self.config = config
        self.board = blackboard or Blackboard()
        self.ui = ui
        self.state = CampaignState(target=config.target)
        self.agents: list[Any] = []

    def register_agent(self, agent: Any) -> None:
        self.agents.append(agent)

    def build_agents(self) -> list[Any]:
        for name in self.config.enabled_agents:
            factory = AGENT_REGISTRY.get(name)
            if factory is None:
                continue
            agent = factory(blackboard=self.board, config=self.config)
            self.register_agent(agent)
        return self.agents

    def run(self) -> CampaignState:
        self.state.status = "running"
        self.build_agents()

        mission_text = self.config.mission
        if self.ui is not None:
            mission_text = self.ui.prompt_mission()
            self.config.mission = mission_text

        bootstrap = Finding(
            campaign_id=self.state.campaign_id,
            agent="system",
            kind="MISSION_SUBMITTED",
            target=self.config.target,
            payload={"mission": mission_text},
            confidence=1.0,
            summary=f"Mission received: {mission_text}",
        )
        self.board.write(bootstrap, topic="MISSION_SUBMITTED")

        if self.ui is not None:
            self.ui.render_campaign_banner(self.config.target)

        depth = 0
        while depth < self.config.max_depth:
            changed = False
            current_results = list(self.board.all())
            for finding in current_results:
                for agent in self.agents:
                    if hasattr(agent, "trigger") and agent.trigger(finding):
                        try:
                            result = agent.handle(finding)
                        except Exception as exc:  # pragma: no cover - defensive runtime guard
                            self.board.write(
                                Finding(
                                    campaign_id=self.state.campaign_id,
                                    agent=agent.name,
                                    kind="AGENT_ERROR",
                                    target=finding.target,
                                    payload={"error": str(exc), "kind": finding.kind},
                                    confidence=0.2,
                                    summary=f"Agent {agent.name} failed on {finding.kind}",
                                ),
                                topic="AGENT_ERROR",
                            )
                            continue
                        if isinstance(result, Finding):
                            self.board.write(result, topic=result.kind)
                            changed = True
                        elif isinstance(result, list):
                            for item in result:
                                if isinstance(item, Finding):
                                    self.board.write(item, topic=item.kind)
                            if result:
                                changed = True
            if not changed:
                break
            depth += 1

        self.state.status = "completed"
        self.state.findings = list(self.board.all())
        if self.ui is not None:
            self.ui.render_summary(self.state.findings)
        return self.state


def run() -> CampaignState:
    config = load_config()
    board = Blackboard()
    ui = GrethTUI(board, config)
    return CampaignScheduler(config=config, blackboard=board, ui=ui).run()
