from __future__ import annotations

from typing import Any

from agent.state import FoodLensState


def trace(state: FoodLensState, node: str, status: str) -> list[dict[str, str]]:
    workflow_trace = list(state.get("workflow_trace", []))
    workflow_trace.append({"node": node, "status": status})
    return workflow_trace


def first(items: list[dict], fallback: str = "Not enough data") -> str:
    if not items:
        return fallback
    return str(items[0].get("name", fallback))


def metric(analysis: dict[str, Any], key: str, fallback: int = 0) -> int | float:
    return analysis.get("metrics", {}).get(key, fallback)
