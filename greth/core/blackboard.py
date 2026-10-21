"""In-memory stigmergic blackboard."""

from __future__ import annotations

from collections import defaultdict
from typing import Callable, Iterable

from greth.core.models import Finding


class Blackboard:
    """Shared state and message bus for swarm agents."""

    def __init__(self) -> None:
        self._findings: list[Finding] = []
        self._subscribers: dict[str, list[Callable[[Finding], None]]] = defaultdict(list)

    def subscribe(self, topic: str, callback: Callable[[Finding], None]) -> None:
        self._subscribers[topic].append(callback)

    def write(self, finding: Finding, topic: str | None = None) -> Finding:
        self._findings.append(finding)
        if topic is None:
            topic = finding.kind
        for callback in self._subscribers.get(topic, []):
            callback(finding)
        return finding

    def query(self, *, kind: str | None = None, target: str | None = None, limit: int | None = None) -> list[Finding]:
        results = list(self._findings)
        if kind is not None:
            results = [item for item in results if item.kind == kind]
        if target is not None:
            results = [item for item in results if item.target == target]
        if limit is not None:
            results = results[-limit:]
        return sorted(results, key=lambda item: item.created_at, reverse=True)

    def latest(self, kind: str | None = None) -> list[Finding]:
        return self.query(kind=kind, limit=10)

    def all(self) -> Iterable[Finding]:
        return list(self._findings)
