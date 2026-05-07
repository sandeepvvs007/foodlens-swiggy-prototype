from __future__ import annotations

from agent.contracts import merge_contract_output
from agent.state import FoodLensState


def budget_burn_analysis(state: FoodLensState) -> FoodLensState:
    burn = state["grounding"].get("budget_burn", {})
    findings = [
        f"Budget burn status is {burn.get('status', 'unknown')}.",
        f"Projected spend uses {burn.get('budget_used_percent', 0)}% of the monthly budget.",
        burn.get("detail", "Budget burn detail is unavailable."),
    ]
    return merge_contract_output(
        state,
        "budget_burn_analysis",
        "grounded budget burn rate",
        {"burn_findings": findings},
    )
