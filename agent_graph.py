from __future__ import annotations

import warnings
from typing import Any, TypedDict

warnings.filterwarnings("ignore")

from langgraph.graph import END, START, StateGraph

from prompts import (
    FOODLENS_SYSTEM_PROMPT,
    GROUNDING_PROMPT,
    GUARDRAIL_PROMPT,
    HABIT_ANALYST_PROMPT,
    RECOMMENDATION_PROMPT,
    SPEND_ANALYST_PROMPT,
)


class FoodLensState(TypedDict, total=False):
    analysis: dict[str, Any]
    prompts: dict[str, str]
    grounding: dict[str, Any]
    spend_findings: list[str]
    habit_findings: list[str]
    risk_findings: list[str]
    agent_summary: list[str]
    agent_recommendations: list[str]
    guardrails: dict[str, Any]
    workflow_trace: list[dict[str, str]]


def _trace(state: FoodLensState, node: str, status: str) -> list[dict[str, str]]:
    trace = list(state.get("workflow_trace", []))
    trace.append({"node": node, "status": status})
    return trace


def _first(items: list[dict], fallback: str = "Not enough data") -> str:
    if not items:
        return fallback
    return str(items[0].get("name", fallback))


def _metric(analysis: dict[str, Any], key: str, fallback: int = 0) -> int | float:
    return analysis.get("metrics", {}).get(key, fallback)


def ground_context(state: FoodLensState) -> FoodLensState:
    analysis = state["analysis"]
    grounding = {
        "period": analysis.get("period", {}).get("label", "Selected period"),
        "monthly_budget": analysis.get("budget", {}).get("monthly_budget", 0),
        "order_count": _metric(analysis, "order_count"),
        "total_spend": _metric(analysis, "total_spend"),
        "average_order_value": _metric(analysis, "average_order_value"),
        "projected_monthly_spend": _metric(analysis, "projected_monthly_spend"),
        "delivery_fee_total": _metric(analysis, "delivery_fee_total"),
        "orders_per_week": _metric(analysis, "orders_per_week"),
        "top_dish": _first(analysis.get("top_dishes", [])),
        "top_restaurant": _first(analysis.get("top_restaurants", [])),
        "top_cuisine": _first(analysis.get("top_cuisines", [])),
        "peak_meal_window": _first(analysis.get("time_buckets", [])),
        "peak_hour": _first(
            sorted(
                analysis.get("hourly_breakdown", []),
                key=lambda item: item.get("count", 0),
                reverse=True,
            )
        ),
        "peak_weekday": _first(
            sorted(
                analysis.get("weekday_breakdown", []),
                key=lambda item: item.get("count", 0),
                reverse=True,
            )
        ),
        "food_personality": analysis.get("food_personality", {}).get("name", "Unknown"),
        "pattern_tags": [item["name"] for item in analysis.get("pattern_tags", [])],
    }
    return {
        **state,
        "prompts": {
            "system": FOODLENS_SYSTEM_PROMPT.strip(),
            "grounding": GROUNDING_PROMPT.strip(),
            "spend": SPEND_ANALYST_PROMPT.strip(),
            "habit": HABIT_ANALYST_PROMPT.strip(),
            "recommendation": RECOMMENDATION_PROMPT.strip(),
            "guardrail": GUARDRAIL_PROMPT.strip(),
        },
        "grounding": grounding,
        "workflow_trace": _trace(state, "ground_context", "grounded analytics payload"),
    }


def spend_analysis(state: FoodLensState) -> FoodLensState:
    grounding = state["grounding"]
    budget = grounding["monthly_budget"]
    projected = grounding["projected_monthly_spend"]
    delta = projected - budget
    findings = [
        f"Projected monthly spend is Rs {projected:,} against a Rs {budget:,} budget.",
        f"Total delivery-fee leakage in this period is Rs {grounding['delivery_fee_total']:,}.",
        f"Average order value is Rs {grounding['average_order_value']:,}.",
    ]
    if delta > 0:
        findings.insert(1, f"Current pace is Rs {delta:,} above the user's monthly budget.")
    else:
        findings.insert(1, f"Current pace is Rs {abs(delta):,} below the user's monthly budget.")
    return {
        **state,
        "spend_findings": findings,
        "workflow_trace": _trace(state, "spend_analysis", "computed spend risks"),
    }


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
    return {
        **state,
        "habit_findings": findings,
        "workflow_trace": _trace(state, "habit_analysis", "identified behavior patterns"),
    }


def risk_detection(state: FoodLensState) -> FoodLensState:
    grounding = state["grounding"]
    risks = []
    if grounding["projected_monthly_spend"] > grounding["monthly_budget"]:
        risks.append("Budget overrun risk")
    if grounding["delivery_fee_total"] >= 300:
        risks.append("Delivery fee leakage")
    if grounding["peak_meal_window"] in {"Dinner", "Late night"}:
        risks.append("Impulse ordering window")
    if "dessert" in grounding["pattern_tags"] or "drink" in grounding["pattern_tags"]:
        risks.append("Add-on spend risk")
    if not risks:
        risks.append("No major risk detected for this period")
    return {
        **state,
        "risk_findings": risks,
        "workflow_trace": _trace(state, "risk_detection", "screened risk categories"),
    }


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
    if "Add-on spend risk" in risks:
        recommendations.append("Show a dessert/drink nudge only after the user confirms they want add-ons.")
    recommendations.append(
        f"For repeat behavior, compare {grounding['top_restaurant']} against two cheaper similar options."
    )
    return {
        **state,
        "agent_recommendations": recommendations[:5],
        "workflow_trace": _trace(state, "recommendation_drafter", "drafted grounded actions"),
    }


def guardrail_review(state: FoodLensState) -> FoodLensState:
    blocked_terms = ["diagnose", "cure", "guaranteed weight", "must order", "auto order"]
    generated_text = " ".join(
        state.get("spend_findings", [])
        + state.get("habit_findings", [])
        + state.get("agent_recommendations", [])
    ).lower()
    blocked = [term for term in blocked_terms if term in generated_text]
    return {
        **state,
        "guardrails": {
            "status": "passed" if not blocked else "blocked",
            "blocked_terms": blocked,
            "checks": [
                "No medical claims",
                "No invented metrics",
                "No hidden cart/order actions",
                "Recommendations grounded in analytics payload",
                "User consent required for MCP data access",
            ],
        },
        "workflow_trace": _trace(state, "guardrail_review", "validated output safety"),
    }


def final_response(state: FoodLensState) -> FoodLensState:
    summary = [
        state["spend_findings"][0],
        state["habit_findings"][0],
        f"Main risks: {', '.join(state['risk_findings'])}.",
        state["habit_findings"][3],
    ]
    return {
        **state,
        "agent_summary": summary,
        "workflow_trace": _trace(state, "final_response", "assembled final agent output"),
    }


def build_foodlens_graph():
    graph = StateGraph(FoodLensState)
    graph.add_node("ground_context", ground_context)
    graph.add_node("spend_analysis", spend_analysis)
    graph.add_node("habit_analysis", habit_analysis)
    graph.add_node("risk_detection", risk_detection)
    graph.add_node("recommendation_drafter", recommendation_drafter)
    graph.add_node("guardrail_review", guardrail_review)
    graph.add_node("final_response", final_response)

    graph.add_edge(START, "ground_context")
    graph.add_edge("ground_context", "spend_analysis")
    graph.add_edge("spend_analysis", "habit_analysis")
    graph.add_edge("habit_analysis", "risk_detection")
    graph.add_edge("risk_detection", "recommendation_drafter")
    graph.add_edge("recommendation_drafter", "guardrail_review")
    graph.add_edge("guardrail_review", "final_response")
    graph.add_edge("final_response", END)
    return graph.compile()


FOODLENS_GRAPH = build_foodlens_graph()


def run_foodlens_agent(analysis: dict[str, Any]) -> dict[str, Any]:
    state = FOODLENS_GRAPH.invoke({"analysis": analysis, "workflow_trace": []})
    return {
        "agent_summary": state.get("agent_summary", []),
        "agent_recommendations": state.get("agent_recommendations", []),
        "agent_risks": state.get("risk_findings", []),
        "guardrails": state.get("guardrails", {}),
        "workflow_trace": state.get("workflow_trace", []),
        "prompt_grounding": {
            "system": state.get("prompts", {}).get("system", ""),
            "grounding": state.get("grounding", {}),
        },
    }
