from __future__ import annotations

from agent.contracts import merge_contract_output
from agent.state import FoodLensState


def goal_analysis(state: FoodLensState) -> FoodLensState:
    goal = state["grounding"].get("weekly_goal", {})
    findings = [
        f"Weekly budget goal is Rs {goal.get('budget', 0):,}.",
        f"Current weekly pace is Rs {goal.get('current_pace', 0):,}.",
    ]
    findings.extend(goal.get("actions", [])[:4])
    return merge_contract_output(
        state,
        "goal_analysis",
        "prepared weekly goal",
        {"goal_findings": findings},
    )
