from __future__ import annotations

from agent.state import FoodLensState
from agent.utils import trace


def risk_detection(state: FoodLensState) -> FoodLensState:
    grounding = state["grounding"]
    risks = []
    if grounding["projected_monthly_spend"] > grounding["monthly_budget"]:
        risks.append("Budget overrun risk")
    if grounding["delivery_fee_total"] >= 300:
        risks.append("Delivery fee leakage")
    if grounding["peak_meal_window"] in {"Dinner", "Late night"}:
        risks.append("Impulse ordering window")
    if "dessert" in grounding["pattern_tags"] or "drink" in grounding["pattern_tags"]:
        risks.append("Add-on spend risk")
    if grounding.get("budget_burn", {}).get("status") == "over pace":
        risks.append("Budget burn risk")
    if grounding.get("swiggy_one_suggestion"):
        risks.append("Membership savings check")
    if not risks:
        risks.append("No major risk detected for this period")
    return {
        **state,
        "risk_findings": risks,
        "workflow_trace": trace(state, "risk_detection", "screened risk categories"),
    }
