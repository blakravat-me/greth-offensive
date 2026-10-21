"""Agent base classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from greth.core.blackboard import Blackboard


class AgentBase(ABC):
    """Base class for swarm specialists."""

    name: str = "base"

    def __init__(self, *, blackboard: Blackboard | None = None, **kwargs: Any) -> None:
        self.blackboard = blackboard or Blackboard()
        self.config = kwargs

    @abstractmethod
    def trigger(self, finding: Any) -> bool:
        return False

    @abstractmethod
    def handle(self, finding: Any) -> Any:
        raise NotImplementedError

    def run_loop(self) -> None:
        """Convenience loop for event-driven polling."""
        return None
