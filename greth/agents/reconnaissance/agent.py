"""Agent base classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from greth.core.blackboard import Blackboard
from greth.core.models import Finding


class AgentBase(ABC):
    """Base class for swarm specialists."""

    name: str = "base"

    def __init__(self, *, blackboard: Blackboard | None = None, config: Any | None = None, **kwargs: Any) -> None:
        self.blackboard = blackboard or Blackboard()
        self.config = config
        self.kwargs = kwargs

    def publish(
        self,
        *,
        kind: str,
        target: str,
        payload: dict[str, Any] | None = None,
        confidence: float = 0.5,
        summary: str = "",
        agent: str | None = None,
    ) -> Finding:
        finding = Finding(
            campaign_id="campaign",
            agent=agent or self.name,
            kind=kind,
            target=target,
            payload=payload or {},
            confidence=confidence,
            summary=summary,
            pheromone_base=max(0.0, min(confidence, 1.0)),
            half_life_sec=3600,
        )
        return self.blackboard.write(finding, topic=kind)

    @abstractmethod
    def trigger(self, finding: Any) -> bool:
        return False

    @abstractmethod
    def handle(self, finding: Any) -> Any:
        raise NotImplementedError

    def loop_once(self, findings: list[Any]) -> list[Any]:
        actions: list[Any] = []
        for finding in findings:
            if self.trigger(finding):
                actions.append(self.handle(finding))
        return actions
