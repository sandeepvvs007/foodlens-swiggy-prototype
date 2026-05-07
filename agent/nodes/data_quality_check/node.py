from __future__ import annotations

from agent.contracts import merge_structured_node_output
from agent.state import FoodLensState


def _status(score: int) -> str:
    if score >= 80:
        return "strong"
    if score >= 55:
        return "moderate"
    return "limited"


def data_quality_check(state: FoodLensState) -> FoodLensState:
    grounding = state["grounding"]
    order_count = int(grounding.get("order_count") or 0)
    days_observed = int(grounding.get("days_observed") or 0)
    period_days = int(grounding.get("period_days") or days_observed or 0)
    has_delivery_fees = grounding.get("delivery_fee_total") is not None
    has_macros = bool(grounding.get("macro_breakdown"))

    score = 30
    score += 30 if order_count >= 20 else 20 if order_count >= 8 else 8
    score += 20 if days_observed >= min(period_days, 21) else 10 if days_observed >= 7 else 4
    score += 10 if has_delivery_fees else 0
    score += 10 if has_macros else 0
    score = min(score, 100)
    status = _status(score)

    checks = [
        {
            "name": "Order sample",
            "status": "strong" if order_count >= 20 else "moderate" if order_count >= 8 else "limited",
            "detail": f"{order_count} orders are available for this period.",
        },
        {
            "name": "History coverage",
            "status": "strong" if days_observed >= min(period_days, 21) else "moderate" if days_observed >= 7 else "limited",
            "detail": f"The selected period covers {days_observed} observed days.",
        },
        {
            "name": "Cost fields",
            "status": "strong" if has_delivery_fees else "limited",
            "detail": "Delivery fee data is present." if has_delivery_fees else "Delivery fee data is missing.",
        },
        {
            "name": "Nutrition estimate",
            "status": "estimated" if has_macros else "limited",
            "detail": "Macro split is estimated from dish names, not verified restaurant nutrition.",
        },
    ]
    output = {
        "data_quality": {
            "status": status,
            "score": score,
            "confidence_label": f"{status.title()} signal",
            "summary": (
                f"{status.title()} confidence based on {order_count} orders over "
                f"{days_observed} observed days."
            ),
            "checks": checks,
        }
    }
    return merge_structured_node_output(
        state,
        "data_quality_check",
        "scored analysis confidence",
        output,
    )
