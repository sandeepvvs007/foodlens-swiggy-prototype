from __future__ import annotations

from agent.state import FoodLensState
from agent.utils import trace


def hidden_cost_analysis(state: FoodLensState) -> FoodLensState:
    costs = state["grounding"].get("hidden_costs", [])
    fee_cost = next((item for item in costs if item.get("name") == "Delivery fees"), {})
    add_on_cost = next((item for item in costs if item.get("name") == "Dessert/drink add-ons"), {})
    high_order_cost = next((item for item in costs if item.get("name") == "Rs 450+ orders"), {})
    findings = [
        f"Delivery fees account for Rs {fee_cost.get('amount', 0):,}.",
        f"Dessert/drink add-ons are estimated at Rs {add_on_cost.get('amount', 0):,}.",
        f"Rs 450+ orders account for Rs {high_order_cost.get('amount', 0):,}.",
    ]
    suggestion = state["grounding"].get("swiggy_one_suggestion")
    if suggestion:
        findings.append(suggestion.get("detail", "Swiggy One savings check is applicable."))
    return {
        **state,
        "hidden_cost_findings": findings,
        "workflow_trace": trace(state, "hidden_cost_analysis", "mapped hidden costs"),
    }
