from __future__ import annotations

import json
import os
from typing import Any, Protocol, TypedDict

from agent.contracts import parse_structured_output
from agent.state import FoodLensState


class LLMMessage(TypedDict):
    role: str
    content: str


class LLMProvider(Protocol):
    def generate_json(self, messages: list[LLMMessage]) -> str:
        ...


class DisabledLLMProvider:
    def generate_json(self, messages: list[LLMMessage]) -> str:
        raise RuntimeError("LLM calls are disabled. Set FOODLENS_ENABLE_LLM=1 to enable a live provider.")


class OpenAIResponsesProvider:
    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.getenv("FOODLENS_LLM_MODEL", "gpt-4.1-mini")

    def generate_json(self, messages: list[LLMMessage]) -> str:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install the optional openai package before enabling live LLM calls.") from exc

        client = OpenAI()
        response = client.responses.create(
            model=self.model,
            input=[{"role": item["role"], "content": item["content"]} for item in messages],
            text={"format": {"type": "json_object"}},
        )
        return response.output_text


def llm_enabled() -> bool:
    return os.getenv("FOODLENS_ENABLE_LLM", "").strip().lower() in {"1", "true", "yes"}


def llm_strategy_for(node_name: str, state: FoodLensState) -> dict[str, Any]:
    prompt = state.get("prompts", {}).get(node_name, {})
    return prompt.get("llm_strategy", {"mode": "deterministic_only"})


def get_llm_provider() -> LLMProvider:
    if not llm_enabled():
        return DisabledLLMProvider()
    provider_name = os.getenv("FOODLENS_LLM_PROVIDER", "openai").strip().lower()
    if provider_name == "openai":
        return OpenAIResponsesProvider()
    raise RuntimeError(f"Unsupported LLM provider: {provider_name}")


def build_node_messages(node_name: str, state: FoodLensState, deterministic_output: dict[str, Any]) -> list[LLMMessage]:
    prompt = state.get("prompts", {}).get(node_name, {})
    system = state.get("prompts", {}).get("ground_context", {}).get("system", "")
    payload = {
        "node_name": node_name,
        "prompt": prompt,
        "grounding": state.get("grounding", {}),
        "risk_findings": state.get("risk_findings", []),
        "spend_findings": state.get("spend_findings", []),
        "burn_findings": state.get("burn_findings", []),
        "hidden_cost_findings": state.get("hidden_cost_findings", []),
        "habit_findings": state.get("habit_findings", []),
        "goal_findings": state.get("goal_findings", []),
        "agent_recommendations": state.get("agent_recommendations", []),
        "prioritized_insights": state.get("prioritized_insights", []),
        "next_best_actions": state.get("next_best_actions", []),
        "data_quality": state.get("data_quality", {}),
        "subscription_value": state.get("subscription_value", {}),
        "nutrition_confidence": state.get("nutrition_confidence", {}),
        "deterministic_output": deterministic_output,
    }
    return [
        {
            "role": "system",
            "content": system or "You are FoodLens. Return only valid JSON matching the node output contract.",
        },
        {
            "role": "developer",
            "content": (
                "Follow this node's prompt contract exactly. Return only one JSON object. "
                "Do not include markdown, prose, or fields outside the output contract."
            ),
        },
        {
            "role": "user",
            "content": json.dumps(payload, ensure_ascii=True),
        },
    ]


def run_optional_llm_node(
    node_name: str,
    state: FoodLensState,
    deterministic_output: dict[str, Any],
) -> dict[str, Any]:
    strategy = llm_strategy_for(node_name, state)
    if strategy.get("mode") == "deterministic_only":
        return deterministic_output
    if not llm_enabled():
        return deterministic_output

    messages = build_node_messages(node_name, state, deterministic_output)
    raw_output = get_llm_provider().generate_json(messages)
    return parse_structured_output(node_name, state.get("prompts", {}), raw_output)
