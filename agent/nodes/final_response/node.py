from __future__ import annotations

from agent.state import FoodLensState
from agent.utils import trace


def final_response(state: FoodLensState) -> FoodLensState:
    summary = [
        state["spend_findings"][0],
        state["burn_findings"][1],
        state["hidden_cost_findings"][0],
        state["habit_findings"][0],
        f"Main risks: {', '.join(state['risk_findings'])}.",
        state["goal_findings"][0],
    ]
    return {
        **state,
        "agent_summary": summary,
        "workflow_trace": trace(state, "final_response", "assembled final agent output"),
    }
