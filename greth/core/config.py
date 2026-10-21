"""Configuration and runtime definitions for Greth."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import yaml

CampaignMode = Literal["recon", "offense", "full", "monitoring", "defense"]


@dataclass(slots=True)
class GrethConfig:
    """Configuration for a single campaign run."""

    target: str = "https://example.com"
    mode: CampaignMode = "full"
    model: str = "gpt-4o-mini"
    provider: str = "openai"
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
            "monitoring",
            "defense",
            "engineering",
            "compaction",
            "chaining",
        ]
    )
    allowed_agents: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=lambda: ["internet", "terminal", "httpx", "bash"])
    polling_interval: float = 0.5
    ui_mode: str = "console"
    allowlisted_commands: list[str] = field(
        default_factory=lambda: [
            "curl",
            "nmap",
            "ffuf",
            "nuclei",
            "httpx",
            "amass",
            "sqlmap",
            "dnsrecon",
            "gobuster",
            "python",
            "bash",
        ]
    )
    default_timeout: int = 30
    config_path: str = str(Path.home() / ".greth_offensive" / "config.yml")

    def effective_agents(self) -> list[str]:
        if self.allowed_agents:
            return [agent for agent in self.enabled_agents if agent in self.allowed_agents]
        return list(self.enabled_agents)


CONFIG_DIR = Path.home() / ".greth_offensive"
CONFIG_PATH = CONFIG_DIR / "config.yml"


def default_config_dict() -> dict[str, Any]:
    return {
        "target": "https://example.com",
        "mode": "full",
        "model": "gpt-4o-mini",
        "provider": "openai",
        "max_depth": 4,
        "verification_required": True,
        "enabled_agents": [
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
        "tools": ["internet", "terminal", "httpx", "bash"],
        "ui_mode": "console",
        "allowlisted_commands": [
            "curl",
            "nmap",
            "ffuf",
            "nuclei",
            "httpx",
            "amass",
            "sqlmap",
            "dnsrecon",
            "gobuster",
            "python",
            "bash",
        ],
        "default_timeout": 30,
    }


def ensure_default_config() -> Path:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(yaml.safe_dump(default_config_dict(), sort_keys=False), encoding="utf-8")
    return CONFIG_PATH


def load_config() -> dict[str, Any]:
    ensure_default_config()
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}
    defaults = default_config_dict()
    defaults.update(loaded)
    return defaults


def build_config() -> GrethConfig:
    data = load_config()
    return GrethConfig(
        target=data.get("target", "https://example.com"),
        mode=data.get("mode", "full"),
        model=data.get("model", "gpt-4o-mini"),
        provider=data.get("provider", "openai"),
        llm_provider=data.get("llm_provider", data.get("provider", "openai")),
        max_depth=int(data.get("max_depth", 4)),
        verification_required=bool(data.get("verification_required", True)),
        enabled_agents=list(data.get("enabled_agents", default_config_dict()["enabled_agents"])),
        allowed_agents=list(data.get("allowed_agents", [])),
        tools=list(data.get("tools", ["internet", "terminal", "httpx", "bash"])),
        ui_mode=data.get("ui_mode", "console"),
        allowlisted_commands=list(data.get("allowlisted_commands", default_config_dict()["allowlisted_commands"])),
        default_timeout=int(data.get("default_timeout", 30)),
        config_path=str(CONFIG_PATH),
    )


def load_or_create_default_config() -> GrethConfig:
    ensure_default_config()
    return build_config()
