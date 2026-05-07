from __future__ import annotations

from agent.contracts import merge_structured_node_output
from agent.state import FoodLensState


def _priority(label: str, title: str, detail: str, impact: str, confidence: str, score: int) -> dict:
    return {
        "label": label,
        "title": title,
        "detail": detail,
        "impact": impact,
        "confidence": confidence,
        "score": score,
    }


def insight_prioritizer(state: FoodLensState) -> FoodLensState:
    grounding = state["grounding"]
    quality = state.get("data_quality", {})
    subscription = state.get("subscription_value", {})
    confidence = quality.get("confidence_label", "Moderate signal")
    budget_burn = grounding.get("budget_burn", {})
    weekly_goal = grounding.get("weekly_goal", {})

    insights = [
        _priority(
            "Budget",
            "Keep this month under control",
            f"Projected spend is Rs {grounding.get('projected_monthly_spend', 0):,} against a Rs {grounding.get('monthly_budget', 0):,} budget.",
            f"{budget_burn.get('budget_used_percent', 0)}% budget pace",
            confidence,
            96,
        ),
        _priority(
            "Fees",
            "Reduce invisible delivery leakage",
            f"Delivery fees account for Rs {grounding.get('delivery_fee_total', 0):,} in this period.",
            "Immediate savings lever",
            confidence,
            90 if grounding.get("delivery_fee_total", 0) >= 300 else 70,
        ),
        _priority(
            "Timing",
            "Plan around your strongest ordering window",
            f"Your peak pattern is {grounding.get('peak_meal_window')} around {grounding.get('peak_hour')}.",
            "Better pre-order decisions",
            confidence,
            82,
        ),
    ]
    if subscription.get("status") == "worth checking":
        insights.append(
            _priority(
                "Membership",
                subscription.get("title", "Check membership value"),
                subscription.get("detail", "Compare recent fees against membership savings."),
                "Could reduce fee pressure",
                confidence,
                78,
            )
        )
    if weekly_goal:
        insights.append(
            _priority(
                "Goal",
                "Use one weekly cap instead of daily guilt",
                f"This week's suggested cap is Rs {weekly_goal.get('budget', 0):,}.",
                "Simple behavior change",
                confidence,
                76,
            )
        )
    insights = sorted(insights, key=lambda item: item["score"], reverse=True)[:5]
    return merge_structured_node_output(
        state,
        "insight_prioritizer",
        "ranked highest impact insights",
        {"prioritized_insights": insights},
    )
