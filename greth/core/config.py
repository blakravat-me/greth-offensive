"""Configuration and runtime definitions for Greth."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import yaml

CampaignMode = Literal["recon", "offense", "full"]
DEFAULT_CONFIG_PATH = Path.home() / ".greth_offensive" / "config.yml"


@dataclass(slots=True)
class GrethConfig:
    """Configuration for a single campaign run."""

    target: str = "https://example.com"
    mission: str = "Assess the target and identify likely attack paths."
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
            "mission",
            "reconnaissance",
            "triage",
            "offense",
            "verification",
            "report",
            "monitoring",
            "defense",
            "engineering",
            "compaction",
            "chaining",
        ]
    )
    polling_interval: float = 0.5
    ui_mode: str = "console"
    config_path: str = str(DEFAULT_CONFIG_PATH)


def ensure_default_config(path: str | Path | None = None) -> Path:
    config_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH
    config_path.parent.mkdir(parents=True, exist_ok=True)
    if not config_path.exists():
        config_path.write_text(
            yaml.safe_dump(
                {
                    "target": "https://example.com",
                    "mission": "Assess the target and identify likely attack paths.",
                    "mode": "full",
                    "model": "gpt-4o-mini",
                    "max_depth": 4,
                    "verification_required": True,
                    "enabled_agents": [
                        "mission",
                        "reconnaissance",
                        "triage",
                        "offense",
                        "verification",
                        "report",
                        "monitoring",
                        "defense",
                        "engineering",
                        "compaction",
                        "chaining",
                    ],
                    "ui_mode": "console",
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
    return config_path


def load_config(path: str | Path | None = None) -> GrethConfig:
    config_path = ensure_default_config(path)
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return GrethConfig(
        target=str(raw.get("target", "https://example.com")),
        mission=str(raw.get("mission", "Assess the target and identify likely attack paths.")),
        mode=str(raw.get("mode", "full")),
        model=str(raw.get("model", "gpt-4o-mini")),
        max_depth=int(raw.get("max_depth", 4)),
        verification_required=bool(raw.get("verification_required", True)),
        enabled_agents=list(
            raw.get(
                "enabled_agents",
                [
                    "mission",
                    "reconnaissance",
                    "triage",
                    "offense",
                    "verification",
                    "report",
                    "monitoring",
                    "defense",
                    "engineering",
                    "compaction",
                    "chaining",
                ],
            )
        ),
        ui_mode=str(raw.get("ui_mode", "console")),
        config_path=str(config_path),
    )
