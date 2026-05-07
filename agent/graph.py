from __future__ import annotations

import warnings
from typing import Any

warnings.filterwarnings("ignore")

from langgraph.graph import END, START, StateGraph

from agent.nodes.budget_burn_analysis.node import budget_burn_analysis
from agent.nodes.data_quality_check.node import data_quality_check
from agent.nodes.final_response.node import final_response
from agent.nodes.goal_analysis.node import goal_analysis
from agent.nodes.ground_context.node import ground_context
from agent.nodes.guardrail_review.node import guardrail_review
from agent.nodes.habit_analysis.node import habit_analysis
from agent.nodes.hidden_cost_analysis.node import hidden_cost_analysis
from agent.nodes.insight_prioritizer.node import insight_prioritizer
from agent.nodes.next_best_action_selector.node import next_best_action_selector
from agent.nodes.nutrition_confidence_estimator.node import nutrition_confidence_estimator
from agent.nodes.recommendation_drafter.node import recommendation_drafter
from agent.nodes.risk_detection.node import risk_detection
from agent.nodes.spend_analysis.node import spend_analysis
from agent.nodes.subscription_value_check.node import subscription_value_check
from agent.state import FoodLensState


def build_foodlens_graph():
    graph = StateGraph(FoodLensState)
    graph.add_node("ground_context", ground_context)
    graph.add_node("data_quality_check", data_quality_check)
    graph.add_node("spend_analysis", spend_analysis)
    graph.add_node("budget_burn_analysis", budget_burn_analysis)
    graph.add_node("hidden_cost_analysis", hidden_cost_analysis)
    graph.add_node("subscription_value_check", subscription_value_check)
    graph.add_node("habit_analysis", habit_analysis)
    graph.add_node("nutrition_confidence_estimator", nutrition_confidence_estimator)
    graph.add_node("goal_analysis", goal_analysis)
    graph.add_node("risk_detection", risk_detection)
    graph.add_node("recommendation_drafter", recommendation_drafter)
    graph.add_node("guardrail_review", guardrail_review)
    graph.add_node("insight_prioritizer", insight_prioritizer)
    graph.add_node("next_best_action_selector", next_best_action_selector)
    graph.add_node("final_response", final_response)

    graph.add_edge(START, "ground_context")
    graph.add_edge("ground_context", "data_quality_check")
    graph.add_edge("data_quality_check", "spend_analysis")
    graph.add_edge("spend_analysis", "budget_burn_analysis")
    graph.add_edge("budget_burn_analysis", "hidden_cost_analysis")
    graph.add_edge("hidden_cost_analysis", "subscription_value_check")
    graph.add_edge("subscription_value_check", "habit_analysis")
    graph.add_edge("habit_analysis", "nutrition_confidence_estimator")
    graph.add_edge("nutrition_confidence_estimator", "goal_analysis")
    graph.add_edge("goal_analysis", "risk_detection")
    graph.add_edge("risk_detection", "recommendation_drafter")
    graph.add_edge("recommendation_drafter", "guardrail_review")
    graph.add_edge("guardrail_review", "insight_prioritizer")
    graph.add_edge("insight_prioritizer", "next_best_action_selector")
    graph.add_edge("next_best_action_selector", "final_response")
    graph.add_edge("final_response", END)
    return graph.compile()


FOODLENS_GRAPH = build_foodlens_graph()


def run_foodlens_agent(analysis: dict[str, Any]) -> dict[str, Any]:
    state = FOODLENS_GRAPH.invoke({"analysis": analysis, "workflow_trace": []})
    return {
        "agent_summary": state.get("agent_summary", []),
        "agent_recommendations": state.get("agent_recommendations", []),
        "agent_risks": state.get("risk_findings", []),
        "data_quality": state.get("data_quality", {}),
        "subscription_value": state.get("subscription_value", {}),
        "nutrition_confidence": state.get("nutrition_confidence", {}),
        "prioritized_insights": state.get("prioritized_insights", []),
        "next_best_actions": state.get("next_best_actions", []),
        "guardrails": state.get("guardrails", {}),
        "workflow_trace": state.get("workflow_trace", []),
        "prompt_grounding": {
            "system": state.get("prompts", {}).get("ground_context", {}).get("system", ""),
            "grounding": state.get("grounding", {}),
            "node_prompts": state.get("prompts", {}),
        },
    }
