from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


NODES_DIR = Path(__file__).resolve().parent / "nodes"


def load_prompt(node_name: str) -> dict[str, Any]:
    prompt_path = NODES_DIR / node_name / "prompt.yaml"
    with prompt_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def load_all_prompts() -> dict[str, dict[str, Any]]:
    prompts: dict[str, dict[str, Any]] = {}
    for prompt_path in sorted(NODES_DIR.glob("*/prompt.yaml")):
        prompts[prompt_path.parent.name] = load_prompt(prompt_path.parent.name)
    return prompts
