"""Configuration loader for ~/.greth_offensive/config.yml."""

from __future__ import annotations

from pathlib import Path

import yaml

from greth.core.config import GrethConfig

CONFIG_DIR = Path.home() / ".greth_offensive"
CONFIG_PATH = CONFIG_DIR / "config.yml"


def default_config_dict() -> dict:
    return {
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
    }


def ensure_default_config() -> Path:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(yaml.safe_dump(default_config_dict(), sort_keys=False), encoding="utf-8")
    return CONFIG_PATH


def load_config() -> dict:
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
        mission=data.get("mission", "Assess the target and identify likely attack paths."),
        mode=data.get("mode", "full"),
        model=data.get("model", "gpt-4o-mini"),
        max_depth=int(data.get("max_depth", 4)),
        verification_required=bool(data.get("verification_required", True)),
        enabled_agents=list(data.get("enabled_agents", default_config_dict()["enabled_agents"])),
        ui_mode=data.get("ui_mode", "console"),
        config_path=str(CONFIG_PATH),
    )


def load_or_create_default_config() -> GrethConfig:
    ensure_default_config()
    return build_config()
