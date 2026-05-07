from __future__ import annotations

from agent.contracts import merge_contract_output
from agent.state import FoodLensState


def final_response(state: FoodLensState) -> FoodLensState:
    summary = [
        state["spend_findings"][0],
        state["burn_findings"][1],
        state["hidden_cost_findings"][0],
        state["habit_findings"][0],
        f"Main risks: {', '.join(state['risk_findings'])}.",
        state["goal_findings"][0],
    ]
    return merge_contract_output(
        state,
        "final_response",
        "assembled final agent output",
        {"agent_summary": summary},
    )
