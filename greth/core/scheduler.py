"""Scheduler and campaign orchestration."""

from __future__ import annotations

from greth.agents.registry import AGENT_REGISTRY
from greth.core.blackboard import Blackboard
from greth.core.config import GrethConfig
from greth.core.models import CampaignState, Finding


class CampaignScheduler:
    """Reactive swarm scheduler using a blackboard and trigger loop."""

    def __init__(self, *, config: GrethConfig, blackboard: Blackboard | None = None, ui: object | None = None) -> None:
        self.config = config
        self.board = blackboard or Blackboard()
        self.ui = ui
        self.state = CampaignState(target=config.target)
        self.agents: list[object] = []

    def register_agent(self, agent: object) -> None:
        self.agents.append(agent)

    def build_agents(self) -> list[object]:
        self.agents.clear()
        for name in self.config.effective_agents():
            factory = AGENT_REGISTRY.get(name)
            if factory is None:
                continue
            self.agents.append(factory(blackboard=self.board, config=self.config))
        return self.agents

    def run(self) -> CampaignState:
        self.state.status = "running"
        self.build_agents()

        bootstrap = Finding(
            campaign_id=self.state.campaign_id,
            agent="system",
            kind="TARGET_REGISTERED",
            target=self.config.target,
            payload={"mode": self.config.mode, "target": self.config.target},
            confidence=1.0,
            severity="critical",
            summary=f"Campaign target registered: {self.config.target}",
        )
        self.board.write(bootstrap, topic="TARGET_REGISTERED")

        if self.ui is not None and hasattr(self.ui, "render_campaign_banner"):
            self.ui.render_campaign_banner(self.config.target)

        depth = 0
        while depth < self.config.max_depth:
            changed = False
            for finding in list(self.board.all()):
                for agent in self.agents:
                    if not hasattr(agent, "trigger") or not agent.trigger(finding):
                        continue
                    try:
                        result = agent.handle(finding)
                    except Exception as exc:  # pragma: no cover - defensive runtime guard
                        self.board.write(
                            Finding(
                                campaign_id=self.state.campaign_id,
                                agent=getattr(agent, "name", "unknown"),
                                kind="AGENT_ERROR",
                                target=finding.target,
                                payload={"error": str(exc), "kind": finding.kind},
                                confidence=0.2,
                                severity="low",
                                summary=f"Agent {getattr(agent, 'name', 'unknown')} failed on {finding.kind}",
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
            self.board.decay_pheromones()
            depth += 1

        self.state.status = "completed"
        self.state.findings = list(self.board.all())
        self.state.summary = self._build_summary()

        if self.ui is not None and hasattr(self.ui, "render_summary"):
            self.ui.render_summary(self.state.findings)
        return self.state

    def _build_summary(self) -> str:
        return (
            f"Campaign completed against {self.config.target} with "
            f"{len(self.state.findings)} findings across {len(self.agents)} active agents."
        )
