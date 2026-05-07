from __future__ import annotations

from agent.contracts import merge_structured_node_output
from agent.state import FoodLensState


def habit_analysis(state: FoodLensState) -> FoodLensState:
    grounding = state["grounding"]
    findings = [
        f"Primary ordering window is {grounding['peak_meal_window']} around {grounding['peak_hour']}.",
        f"Busiest ordering day is {grounding['peak_weekday']}.",
        f"Most repeated restaurant is {grounding['top_restaurant']}; top dish is {grounding['top_dish']}.",
        f"Food personality is {grounding['food_personality']}.",
    ]
    if grounding["pattern_tags"]:
        findings.append(f"Pattern tags: {', '.join(grounding['pattern_tags'][:4])}.")
    badges = [badge.get("name", "") for badge in grounding.get("personal_badges", [])]
    if badges:
        findings.append(f"Personal badges: {', '.join(badges[:5])}.")
    return merge_structured_node_output(
        state,
        "habit_analysis",
        "identified behavior patterns",
        {"habit_findings": findings},
    )
