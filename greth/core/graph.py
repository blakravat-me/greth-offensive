"""LangGraph orchestration for the Greth swarm."""

from __future__ import annotations

from typing import Any

from langgraph.graph import END, StateGraph

from greth.core.config import GrethConfig
from greth.core.models import CampaignState


class GraphState(dict):
    """State passed through the LangGraph pipeline."""

    target: str
    campaign: CampaignState


def build_graph(config: GrethConfig):
    """Construct an event-driven swarm graph."""

    def recon_node(state: GraphState) -> GraphState:
        state["campaign"].status = "recon"
        state["campaign"].findings.append(
            {
                "agent": "reconnaissance",
                "kind": "TARGET_REGISTERED",
                "target": state["target"],
                "summary": f"Recon began against {state['target']}",
            }
        )
        return state

    def triage_node(state: GraphState) -> GraphState:
        state["campaign"].status = "triage"
        return state

    def offense_node(state: GraphState) -> GraphState:
        state["campaign"].status = "offense"
        return state

    def verification_node(state: GraphState) -> GraphState:
        state["campaign"].status = "verification"
        return state

    def report_node(state: GraphState) -> GraphState:
        state["campaign"].status = "report"
        return state

    workflow = StateGraph(GraphState)
    workflow.add_node("recon", recon_node)
    workflow.add_node("triage", triage_node)
    workflow.add_node("offense", offense_node)
    workflow.add_node("verification", verification_node)
    workflow.add_node("report", report_node)
    workflow.set_entry_point("recon")
    workflow.add_edge("recon", "triage")
    workflow.add_edge("triage", "offense")
    workflow.add_edge("offense", "verification")
    workflow.add_edge("verification", "report")
    workflow.add_edge("report", END)
    return workflow.compile()
