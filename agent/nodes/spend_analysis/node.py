from __future__ import annotations

from agent.state import FoodLensState
from agent.utils import trace


def spend_analysis(state: FoodLensState) -> FoodLensState:
    grounding = state["grounding"]
    budget = grounding["monthly_budget"]
    projected = grounding["projected_monthly_spend"]
    delta = projected - budget
    findings = [
        f"Projected monthly spend is Rs {projected:,} against a Rs {budget:,} budget.",
        f"Total delivery-fee leakage in this period is Rs {grounding['delivery_fee_total']:,}.",
        f"Average order value is Rs {grounding['average_order_value']:,}.",
    ]
    if delta > 0:
        findings.insert(1, f"Current pace is Rs {delta:,} above the user's monthly budget.")
    else:
        findings.insert(1, f"Current pace is Rs {abs(delta):,} below the user's monthly budget.")
    return {
        **state,
        "spend_findings": findings,
        "workflow_trace": trace(state, "spend_analysis", "computed spend risks"),
    }
