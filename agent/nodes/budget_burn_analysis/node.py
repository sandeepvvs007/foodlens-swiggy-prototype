from __future__ import annotations

from agent.state import FoodLensState
from agent.utils import trace


def budget_burn_analysis(state: FoodLensState) -> FoodLensState:
    burn = state["grounding"].get("budget_burn", {})
    findings = [
        f"Budget burn status is {burn.get('status', 'unknown')}.",
        f"Projected spend uses {burn.get('budget_used_percent', 0)}% of the monthly budget.",
        burn.get("detail", "Budget burn detail is unavailable."),
    ]
    return {
        **state,
        "burn_findings": findings,
        "workflow_trace": trace(state, "budget_burn_analysis", "grounded budget burn rate"),
    }
