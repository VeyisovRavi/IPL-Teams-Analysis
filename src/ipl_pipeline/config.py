from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_url: str
    api_source_name: str
    api_timeout_seconds: int
    api_headers: Dict[str, str]
    snowflake_account: str
    snowflake_user: str
    snowflake_password: str
    snowflake_role: str
    snowflake_warehouse: str
    snowflake_database: str
    snowflake_schema: str
    snowflake_table: str


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _load_headers() -> Dict[str, str]:
    raw_headers = os.getenv("API_HEADERS_JSON", "{}")
    try:
        parsed = json.loads(raw_headers)
    except json.JSONDecodeError as exc:
        raise ValueError("API_HEADERS_JSON must be valid JSON") from exc

    if not isinstance(parsed, dict):
        raise ValueError("API_HEADERS_JSON must be a JSON object")

    return {str(key): str(value) for key, value in parsed.items()}


def get_settings() -> Settings:
    load_dotenv()

    timeout = int(os.getenv("API_TIMEOUT_SECONDS", "30"))

    return Settings(
        api_url=_required_env("API_URL"),
        api_source_name=os.getenv("API_SOURCE_NAME", "ipl_api"),
        api_timeout_seconds=timeout,
        api_headers=_load_headers(),
        snowflake_account=_required_env("SNOWFLAKE_ACCOUNT"),
        snowflake_user=_required_env("SNOWFLAKE_USER"),
        snowflake_password=_required_env("SNOWFLAKE_PASSWORD"),
        snowflake_role=_required_env("SNOWFLAKE_ROLE"),
        snowflake_warehouse=_required_env("SNOWFLAKE_WAREHOUSE"),
        snowflake_database=_required_env("SNOWFLAKE_DATABASE"),
        snowflake_schema=_required_env("SNOWFLAKE_SCHEMA"),
        snowflake_table=os.getenv("SNOWFLAKE_TABLE", "RAW_IPL_API_DATA"),
    )
