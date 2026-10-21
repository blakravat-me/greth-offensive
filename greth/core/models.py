"""Shared models used across the Greth ecosystem."""

from __future__ import annotations

import math
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class Finding:
    """A single finding written to the swarm blackboard."""

    campaign_id: str
    agent: str
    kind: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    severity: str = "info"
    status: str = "new"
    pheromone_base: float = 1.0
    half_life_sec: int = 3600
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    superseded_by: str | None = None
    summary: str = ""
    tags: set[str] = field(default_factory=set)
    related_to: list[str] = field(default_factory=list)

    def current_pheromone(self, now: datetime | None = None) -> float:
        if self.half_life_sec <= 0:
            return self.pheromone_base
        reference = now or datetime.now(timezone.utc)
        age = (reference - self.created_at).total_seconds()
        return self.pheromone_base * math.pow(0.5, age / self.half_life_sec)

    def fingerprint(self) -> tuple[str, str, str, str]:
        return (self.kind, self.target, self.summary, self.agent)


@dataclass(slots=True)
class CampaignState:
    """Runtime state for a campaign."""

    campaign_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    target: str = "https://example.com"
    findings: list[Finding] = field(default_factory=list)
    status: str = "initialized"
    summary: str = ""


@dataclass(slots=True)
class ToolResult:
    """Structured result returned by a tool adapter."""

    name: str
    success: bool
    output: Any
    metadata: dict[str, Any] | None = None
