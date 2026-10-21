"""In-memory stigmergic blackboard."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Callable, Iterable

from greth.core.models import Finding


class Blackboard:
    """Shared state and event bus for swarm agents."""

    def __init__(self) -> None:
        self._findings: list[Finding] = []
        self._subscribers: dict[str, list[Callable[[Finding], None]]] = defaultdict(list)

    def subscribe(self, topic: str, callback: Callable[[Finding], None]) -> None:
        self._subscribers[topic].append(callback)

    def write(self, finding: Finding, topic: str | None = None) -> Finding:
        if not finding.summary:
            finding.summary = f"{finding.kind} on {finding.target}"

        signature = finding.fingerprint()
        if any(existing.fingerprint() == signature for existing in self._findings):
            return finding

        self._findings.append(finding)
        resolved_topic = topic or finding.kind
        for callback in self._subscribers.get(resolved_topic, []):
            callback(finding)
        return finding

    def query(
        self,
        *,
        kind: str | None = None,
        target: str | None = None,
        limit: int | None = None,
        severity: str | None = None,
    ) -> list[Finding]:
        results = list(self._findings)
        if kind is not None:
            results = [item for item in results if item.kind == kind]
        if target is not None:
            results = [item for item in results if item.target == target]
        if severity is not None:
            results = [item for item in results if item.severity == severity]
        if limit is not None:
            results = results[-limit:]
        return sorted(results, key=lambda item: item.created_at, reverse=True)

    def latest(self, kind: str | None = None, *, limit: int = 10) -> list[Finding]:
        return self.query(kind=kind, limit=limit)

    def all(self) -> Iterable[Finding]:
        return list(self._findings)

    def deduplicated(
        self,
        *,
        kind: str | None = None,
        target: str | None = None,
        severity: str | None = None,
    ) -> list[Finding]:
        seen: set[tuple[str, str, str, str]] = set()
        result: list[Finding] = []
        for item in self._findings:
            if kind is not None and item.kind != kind:
                continue
            if target is not None and item.target != target:
                continue
            if severity is not None and item.severity != severity:
                continue
            signature = item.fingerprint()
            if signature in seen:
                continue
            seen.add(signature)
            result.append(item)
        return sorted(result, key=lambda item: item.created_at, reverse=True)

    def decay_pheromones(self, *, now: datetime | None = None) -> dict[str, float]:
        reference = now or datetime.now(timezone.utc)
        snapshot: dict[str, float] = {}
        for finding in self._findings:
            finding.pheromone_base = max(0.0, finding.current_pheromone(reference))
            snapshot[finding.id] = finding.pheromone_base
        return snapshot

    def pheromone_snapshot(self) -> dict[str, float]:
        return self.decay_pheromones()

    def severity_breakdown(self) -> dict[str, int]:
        breakdown: dict[str, int] = {}
        for finding in self._findings:
            breakdown[finding.severity] = breakdown.get(finding.severity, 0) + 1
        return breakdown
