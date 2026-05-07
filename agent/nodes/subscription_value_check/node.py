from __future__ import annotations

from agent.contracts import merge_structured_node_output
from agent.state import FoodLensState


def subscription_value_check(state: FoodLensState) -> FoodLensState:
    grounding = state["grounding"]
    delivery_fee_total = int(grounding.get("delivery_fee_total") or 0)
    orders_per_week = float(grounding.get("orders_per_week") or 0)
    suggestion = grounding.get("swiggy_one_suggestion")

    if suggestion:
        status = "worth checking"
        title = "Swiggy One may be worth checking"
        detail = suggestion.get("detail", "Compare recent delivery fees against membership savings before subscribing.")
    elif delivery_fee_total >= 150 and orders_per_week >= 2:
        status = "watch"
        title = "Delivery fees are worth watching"
        detail = "Fees are visible, but this period does not yet make a strong subscription case."
    else:
        status = "low priority"
        title = "Subscription is low priority"
        detail = "Delivery fee pressure is not high enough in this period to make membership the first action."

    output = {
        "subscription_value": {
            "status": status,
            "title": title,
            "detail": detail,
            "evidence": [
                f"Delivery fees: Rs {delivery_fee_total:,}",
                f"Ordering pace: {orders_per_week} orders/week",
            ],
        }
    }
    return merge_structured_node_output(
        state,
        "subscription_value_check",
        "checked membership value",
        output,
    )
