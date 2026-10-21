"""Greth swarm runtime entrypoint."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from greth.agents.registry import AGENT_REGISTRY
from greth.core.blackboard import Blackboard
from greth.core.config import GrethConfig, build_config
from greth.core.models import CampaignState, Finding
from greth.tui.app import ConsoleUI


class CampaignScheduler:
    """Trigger-driven swarm scheduler."""

    def __init__(self, *, config: GrethConfig, blackboard: Blackboard | None = None, ui: Any | None = None) -> None:
        self.config = config
        self.board = blackboard or Blackboard()
        self.ui = ui or ConsoleUI()
        self.state = CampaignState(target=config.target)
        self.agents: list[Any] = []

    def register_agent(self, agent: Any) -> None:
        self.agents.append(agent)

    def build_agents(self) -> list[Any]:
        self.agents.clear()
        for name in self.config.effective_agents():
            factory = AGENT_REGISTRY.get(name)
            if factory is None:
                continue
            agent = factory(blackboard=self.board, config=self.config)
            self.register_agent(agent)
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
                    except Exception as exc:  # pragma: no cover - defensive fallback
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
        self.state.summary = (
            f"Campaign completed against {self.config.target} with {len(self.state.findings)} findings "
            f"using {len(self.agents)} active agents."
        )
        self.ui.render_summary(self.state.findings)
        return self.state


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Greth Offensive Swarm Campaign")
    parser.add_argument("--target", type=str, default=None, help="Target URL or host")
    parser.add_argument("--mode", choices=["recon", "offense", "full", "monitoring", "defense"], default=None)
    parser.add_argument("--config", type=str, default=str(Path.home() / ".greth_offensive" / "config.yml"))
    parser.add_argument("--json", action="store_true", help="Print JSON summary to stdout")
    return parser.parse_args()


def run() -> int:
    args = _parse_args()
    config = build_config()
    if args.target:
        config.target = args.target
    if args.mode:
        config.mode = args.mode
    scheduler = CampaignScheduler(config=config, ui=ConsoleUI())
    state = scheduler.run()
    if args.json:
        payload = {
            "campaign_id": state.campaign_id,
            "target": state.target,
            "status": state.status,
            "summary": state.summary,
            "findings": [
                {
                    "kind": finding.kind,
                    "target": finding.target,
                    "agent": finding.agent,
                    "severity": finding.severity,
                    "confidence": finding.confidence,
                    "summary": finding.summary,
                }
                for finding in state.findings
            ],
        }
        print(json.dumps(payload, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
