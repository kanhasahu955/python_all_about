"""Parse JSON objects from LLM responses (strip markdown fences)."""

import json
import re
from typing import Any


def strip_json_fence(raw: str) -> str:
    text = raw.strip()
    m = re.match(r"^```(?:json)?\s*\n?(.*)\n?```\s*$", text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return text


def parse_llm_json_object(content: str) -> dict[str, Any]:
    return json.loads(strip_json_fence(content))
