from __future__ import annotations

from typing import Any, TypedDict


class FoodLensState(TypedDict, total=False):
    analysis: dict[str, Any]
    prompts: dict[str, dict[str, Any]]
    grounding: dict[str, Any]
    spend_findings: list[str]
    habit_findings: list[str]
    burn_findings: list[str]
    hidden_cost_findings: list[str]
    goal_findings: list[str]
    risk_findings: list[str]
    agent_summary: list[str]
    agent_recommendations: list[str]
    guardrails: dict[str, Any]
    workflow_trace: list[dict[str, str]]
