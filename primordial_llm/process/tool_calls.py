import json
from typing import Dict, Optional


def extract_json_candidate(text: str) -> Optional[str]:
    stripped = text.strip()
    if stripped.startswith("```"):
        parts = stripped.split("```")
        for chunk in parts:
            chunk = chunk.strip()
            if chunk.startswith("json"):
                chunk = chunk[4:].strip()
            if chunk.startswith("{") and chunk.endswith("}"):
                return chunk
    if stripped.startswith("{") and stripped.endswith("}"):
        return stripped
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start != -1 and end != -1 and end > start:
        return stripped[start : end + 1]
    return None


def parse_tool_call(text: str) -> Optional[Dict[str, object]]:
    candidate = extract_json_candidate(text)
    if not candidate:
        return None
    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    if isinstance(payload, dict) and payload.get("tool"):
        return payload
    return None
