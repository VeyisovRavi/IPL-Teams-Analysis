from __future__ import annotations

from typing import Any, Dict

import requests


def fetch_api_payload(url: str, headers: Dict[str, str], timeout_seconds: int) -> Any:
    response = requests.get(url, headers=headers, timeout=timeout_seconds)
    response.raise_for_status()
    return response.json()
