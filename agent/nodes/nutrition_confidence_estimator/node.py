from __future__ import annotations

from agent.contracts import merge_structured_node_output
from agent.state import FoodLensState


def nutrition_confidence_estimator(state: FoodLensState) -> FoodLensState:
    macros = state["grounding"].get("macro_breakdown", [])
    total = sum(int(item.get("count") or 0) for item in macros)
    has_signal = bool(macros and total)
    output = {
        "nutrition_confidence": {
            "status": "estimated" if has_signal else "limited",
            "score": 45 if has_signal else 10,
            "summary": (
                "Macro split is useful for pattern awareness, but it is estimated from dish names."
                if has_signal
                else "Nutrition signal is too weak for this period."
            ),
            "do_not_use_for": [
                "medical advice",
                "diagnosis",
                "guaranteed weight loss",
                "precise calorie tracking",
            ],
        }
    }
    return merge_structured_node_output(
        state,
        "nutrition_confidence_estimator",
        "qualified nutrition estimates",
        output,
    )
