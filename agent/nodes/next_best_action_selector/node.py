from __future__ import annotations

from agent.contracts import merge_structured_node_output
from agent.state import FoodLensState


def next_best_action_selector(state: FoodLensState) -> FoodLensState:
    grounding = state["grounding"]
    weekly_goal = grounding.get("weekly_goal", {})
    subscription = state.get("subscription_value", {})
    top_restaurant = grounding.get("top_restaurant", "your top restaurant")
    peak_hour = grounding.get("peak_hour", "your peak hour")

    actions = [
        {
            "title": "Set this week's Swiggy cap",
            "detail": f"Use Rs {weekly_goal.get('budget', 0):,} as the limit before placing more orders.",
            "impact": "Budget control",
            "confidence": state.get("data_quality", {}).get("confidence_label", "Moderate signal"),
        },
        {
            "title": "Put a pause before peak-hour orders",
            "detail": f"Show the budget nudge before {peak_hour}, your strongest ordering slot.",
            "impact": "Impulse reduction",
            "confidence": state.get("data_quality", {}).get("confidence_label", "Moderate signal"),
        },
        {
            "title": "Compare repeat alternatives",
            "detail": f"When {top_restaurant} appears, compare it with two cheaper similar options.",
            "impact": "Repeat spend optimization",
            "confidence": state.get("data_quality", {}).get("confidence_label", "Moderate signal"),
        },
    ]
    if subscription.get("status") == "worth checking":
        actions.insert(
            1,
            {
                "title": "Check Swiggy One before subscribing",
                "detail": subscription.get("detail", "Compare delivery fees against membership savings."),
                "impact": "Fee savings check",
                "confidence": state.get("data_quality", {}).get("confidence_label", "Moderate signal"),
            },
        )
    return merge_structured_node_output(
        state,
        "next_best_action_selector",
        "selected next best actions",
        {"next_best_actions": actions[:4]},
    )
