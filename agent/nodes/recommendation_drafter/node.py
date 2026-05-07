from __future__ import annotations

from agent.contracts import merge_structured_node_output
from agent.state import FoodLensState


def recommendation_drafter(state: FoodLensState) -> FoodLensState:
    grounding = state["grounding"]
    risks = state["risk_findings"]
    recommendations = []
    if "Budget overrun risk" in risks:
        recommendations.append(
            f"Set a soft cap before {grounding['peak_hour']} because that is the strongest ordering slot."
        )
    recommendations.append(
        f"Create a one-tap '{grounding['top_cuisine']}' shortlist with premium, budget, and lighter picks."
    )
    if "Delivery fee leakage" in risks:
        recommendations.append("Prefer nearby restaurants or batch snack/cafe cravings when delivery fee impact is high.")
    if "Membership savings check" in risks:
        recommendations.append("Compare recent delivery fees against Swiggy One savings before subscribing.")
    if "Add-on spend risk" in risks:
        recommendations.append("Show a dessert/drink nudge only after the user confirms they want add-ons.")
    weekly_goal = grounding.get("weekly_goal", {})
    if weekly_goal:
        recommendations.append(f"Use Rs {weekly_goal.get('budget', 0):,} as this week's ordering cap.")
    recommendations.append(
        f"For repeat behavior, compare {grounding['top_restaurant']} against two cheaper similar options."
    )
    return merge_structured_node_output(
        state,
        "recommendation_drafter",
        "drafted grounded actions",
        {"agent_recommendations": recommendations[:5]},
    )
