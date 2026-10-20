from __future__ import annotations

from typing import Any, List


def normalize_payload(payload: Any) -> List[Any]:
    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, list):
            return data
        return [payload]

    return [{"value": payload}]
