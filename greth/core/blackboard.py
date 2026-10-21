"""In-memory stigmergic blackboard."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
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
        if not finding.summary:
            finding.summary = f"{finding.kind} on {finding.target}"
        if finding not in self._findings:
            self._findings.append(finding)
        resolved_topic = topic or finding.kind
        for callback in self._subscribers.get(resolved_topic, []):
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

    def deduplicated(self, *, kind: str | None = None, target: str | None = None) -> list[Finding]:
        seen: set[tuple[str, str, str]] = set()
        result: list[Finding] = []
        for item in self._findings:
            if kind is not None and item.kind != kind:
                continue
            if target is not None and item.target != target:
                continue
            signature = (item.kind, item.target, item.summary)
            if signature in seen:
                continue
            seen.add(signature)
            result.append(item)
        return sorted(result, key=lambda item: item.created_at, reverse=True)

    def pheromone_snapshot(self) -> dict[str, float]:
        now = datetime.now(timezone.utc)
        value: dict[str, float] = {}
        for finding in self._findings:
            value[finding.id] = finding.current_pheromone(now)
        return value
