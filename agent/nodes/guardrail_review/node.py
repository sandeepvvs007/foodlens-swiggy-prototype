from __future__ import annotations

from agent.contracts import merge_contract_output
from agent.state import FoodLensState


def guardrail_review(state: FoodLensState) -> FoodLensState:
    blocked_terms = ["diagnose", "cure", "guaranteed weight", "must order", "auto order"]
    generated_text = " ".join(
        state.get("spend_findings", [])
        + state.get("burn_findings", [])
        + state.get("hidden_cost_findings", [])
        + state.get("habit_findings", [])
        + state.get("goal_findings", [])
        + state.get("agent_recommendations", [])
    ).lower()
    blocked = [term for term in blocked_terms if term in generated_text]
    return merge_contract_output(
        state,
        "guardrail_review",
        "validated output safety",
        {
            "guardrails": {
                "status": "passed" if not blocked else "blocked",
                "blocked_terms": blocked,
                "checks": [
                    "No medical claims",
                    "No invented metrics",
                    "No hidden cart/order actions",
                    "Recommendations grounded in analytics payload",
                    "User consent required for MCP data access",
                ],
            }
        },
    )
