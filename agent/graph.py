from __future__ import annotations

import warnings
from typing import Any

warnings.filterwarnings("ignore")

from langgraph.graph import END, START, StateGraph

from agent.nodes.budget_burn_analysis.node import budget_burn_analysis
from agent.nodes.final_response.node import final_response
from agent.nodes.goal_analysis.node import goal_analysis
from agent.nodes.ground_context.node import ground_context
from agent.nodes.guardrail_review.node import guardrail_review
from agent.nodes.habit_analysis.node import habit_analysis
from agent.nodes.hidden_cost_analysis.node import hidden_cost_analysis
from agent.nodes.recommendation_drafter.node import recommendation_drafter
from agent.nodes.risk_detection.node import risk_detection
from agent.nodes.spend_analysis.node import spend_analysis
from agent.state import FoodLensState


def build_foodlens_graph():
    graph = StateGraph(FoodLensState)
    graph.add_node("ground_context", ground_context)
    graph.add_node("spend_analysis", spend_analysis)
    graph.add_node("budget_burn_analysis", budget_burn_analysis)
    graph.add_node("hidden_cost_analysis", hidden_cost_analysis)
    graph.add_node("habit_analysis", habit_analysis)
    graph.add_node("goal_analysis", goal_analysis)
    graph.add_node("risk_detection", risk_detection)
    graph.add_node("recommendation_drafter", recommendation_drafter)
    graph.add_node("guardrail_review", guardrail_review)
    graph.add_node("final_response", final_response)

    graph.add_edge(START, "ground_context")
    graph.add_edge("ground_context", "spend_analysis")
    graph.add_edge("spend_analysis", "budget_burn_analysis")
    graph.add_edge("budget_burn_analysis", "hidden_cost_analysis")
    graph.add_edge("hidden_cost_analysis", "habit_analysis")
    graph.add_edge("habit_analysis", "goal_analysis")
    graph.add_edge("goal_analysis", "risk_detection")
    graph.add_edge("risk_detection", "recommendation_drafter")
    graph.add_edge("recommendation_drafter", "guardrail_review")
    graph.add_edge("guardrail_review", "final_response")
    graph.add_edge("final_response", END)
    return graph.compile()


FOODLENS_GRAPH = build_foodlens_graph()


def run_foodlens_agent(analysis: dict[str, Any]) -> dict[str, Any]:
    state = FOODLENS_GRAPH.invoke({"analysis": analysis, "workflow_trace": []})
    return {
        "agent_summary": state.get("agent_summary", []),
        "agent_recommendations": state.get("agent_recommendations", []),
        "agent_risks": state.get("risk_findings", []),
        "guardrails": state.get("guardrails", {}),
        "workflow_trace": state.get("workflow_trace", []),
        "prompt_grounding": {
            "system": state.get("prompts", {}).get("ground_context", {}).get("system", ""),
            "grounding": state.get("grounding", {}),
            "node_prompts": state.get("prompts", {}),
        },
    }
