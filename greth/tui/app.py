"""Simple registry of agents."""

from __future__ import annotations

from greth.agents.chaining.agent import ChainingAgent
from greth.agents.compaction.agent import CompactionAgent
from greth.agents.defense.agent import DefenseAgent
from greth.agents.engineering.agent import EngineeringAgent
from greth.agents.monitoring.agent import MonitoringAgent
from greth.agents.offense.agent import OffenseAgent
from greth.agents.reconnaissance.agent import ReconnaissanceAgent
from greth.agents.report.agent import ReportAgent
from greth.agents.triage.agent import TriageAgent
from greth.agents.verification.agent import VerificationAgent


AGENT_REGISTRY = {
    "reconnaissance": ReconnaissanceAgent,
    "triage": TriageAgent,
    "offense": OffenseAgent,
    "verification": VerificationAgent,
    "report": ReportAgent,
    "monitoring": MonitoringAgent,
    "defense": DefenseAgent,
    "engineering": EngineeringAgent,
    "compaction": CompactionAgent,
    "chaining": ChainingAgent,
}


def get_agent(name: str, **kwargs):
    try:
        cls = AGENT_REGISTRY[name]
    except KeyError as exc:  # pragma: no cover - strong guard
        raise ValueError(f"Unsupported agent: {name}") from exc
    return cls(**kwargs)
