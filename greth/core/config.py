"""Configuration and runtime definitions for Greth."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

CampaignMode = Literal["recon", "offense", "full"]


@dataclass(slots=True)
class GrethConfig:
    """Configuration for a single campaign run."""

    target: str = "https://example.com"
    mode: CampaignMode = "full"
    model: str = "gpt-4o-mini"
    max_agents: int = 8
    pheromone_decay: float = 0.5
    api_key: str | None = None
    llm_provider: str = "openai"
    base_url: str | None = None
    max_depth: int = 4
    verification_required: bool = True
    enabled_agents: list[str] = field(
        default_factory=lambda: [
            "reconnaissance",
            "triage",
            "offense",
            "verification",
            "report",
        ]
    )
