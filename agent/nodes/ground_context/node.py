from __future__ import annotations

from agent.prompt_loader import load_all_prompts
from agent.state import FoodLensState
from agent.utils import first, metric, trace


def ground_context(state: FoodLensState) -> FoodLensState:
    analysis = state["analysis"]
    grounding = {
        "period": analysis.get("period", {}).get("label", "Selected period"),
        "monthly_budget": analysis.get("budget", {}).get("monthly_budget", 0),
        "order_count": metric(analysis, "order_count"),
        "total_spend": metric(analysis, "total_spend"),
        "average_order_value": metric(analysis, "average_order_value"),
        "projected_monthly_spend": metric(analysis, "projected_monthly_spend"),
        "delivery_fee_total": metric(analysis, "delivery_fee_total"),
        "orders_per_week": metric(analysis, "orders_per_week"),
        "top_dish": first(analysis.get("top_dishes", [])),
        "top_restaurant": first(analysis.get("top_restaurants", [])),
        "top_cuisine": first(analysis.get("top_cuisines", [])),
        "peak_meal_window": first(analysis.get("time_buckets", [])),
        "peak_hour": first(
            sorted(
                analysis.get("hourly_breakdown", []),
                key=lambda item: item.get("count", 0),
                reverse=True,
            )
        ),
        "peak_weekday": first(
            sorted(
                analysis.get("weekday_breakdown", []),
                key=lambda item: item.get("count", 0),
                reverse=True,
            )
        ),
        "food_personality": analysis.get("food_personality", {}).get("name", "Unknown"),
        "budget_burn": analysis.get("budget_burn", {}),
        "hidden_costs": analysis.get("hidden_costs", []),
        "weekly_goal": analysis.get("weekly_goal", {}),
        "swiggy_one_suggestion": analysis.get("swiggy_one_suggestion"),
        "personal_badges": analysis.get("personal_badges", []),
        "at_a_glance": analysis.get("at_a_glance", []),
        "macro_breakdown": analysis.get("macro_breakdown", []),
        "pattern_tags": [item["name"] for item in analysis.get("pattern_tags", [])],
    }
    return {
        **state,
        "prompts": load_all_prompts(),
        "grounding": grounding,
        "workflow_trace": trace(state, "ground_context", "grounded analytics payload"),
    }
