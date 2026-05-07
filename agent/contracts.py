from __future__ import annotations

import json
from typing import Any

from agent.state import FoodLensState
from agent.utils import trace


def required_output_keys(prompts: dict[str, dict[str, Any]], node_name: str) -> list[str]:
    contract = prompts.get(node_name, {}).get("output_contract", {})
    return list(contract.get("required_keys", []))


def validate_output_contract(
    node_name: str,
    prompts: dict[str, dict[str, Any]],
    output: dict[str, Any],
) -> dict[str, Any]:
    missing = [key for key in required_output_keys(prompts, node_name) if key not in output]
    if missing:
        missing_keys = ", ".join(missing)
        raise ValueError(f"{node_name} output is missing required key(s): {missing_keys}")
    return output


def parse_structured_output(
    node_name: str,
    prompts: dict[str, dict[str, Any]],
    raw_output: str | dict[str, Any],
) -> dict[str, Any]:
    if isinstance(raw_output, str):
        parsed = json.loads(raw_output)
    else:
        parsed = raw_output
    if not isinstance(parsed, dict):
        raise ValueError(f"{node_name} output must be a JSON object")
    return validate_output_contract(node_name, prompts, parsed)


def merge_contract_output(
    state: FoodLensState,
    node_name: str,
    status: str,
    output: dict[str, Any],
) -> FoodLensState:
    prompts = state.get("prompts", {})
    validated = validate_output_contract(node_name, prompts, output)
    return {
        **state,
        **validated,
        "workflow_trace": trace(state, node_name, status),
    }
