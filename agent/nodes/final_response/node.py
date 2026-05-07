from __future__ import annotations

from agent.contracts import merge_structured_node_output
from agent.state import FoodLensState


def final_response(state: FoodLensState) -> FoodLensState:
    prioritized = state.get("prioritized_insights", [])
    next_actions = state.get("next_best_actions", [])
    quality = state.get("data_quality", {})
    top_insight = prioritized[0] if prioritized else {}
    top_action = next_actions[0] if next_actions else {}
    summary = [
        state["spend_findings"][0],
        state["burn_findings"][1],
        state["hidden_cost_findings"][0],
        f"Top priority: {top_insight.get('title', state['habit_findings'][0])}.",
        f"Next best action: {top_action.get('title', state['goal_findings'][0])}.",
        f"Analysis confidence: {quality.get('confidence_label', 'Signal check')}.",
    ]
    return merge_structured_node_output(
        state,
        "final_response",
        "assembled final agent output",
        {"agent_summary": summary},
    )
