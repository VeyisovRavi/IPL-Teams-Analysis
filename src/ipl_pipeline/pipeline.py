from __future__ import annotations

from src.ipl_pipeline.api_client import fetch_api_payload
from src.ipl_pipeline.config import get_settings
from src.ipl_pipeline.snowflake_loader import SnowflakeLoader
from src.ipl_pipeline.transform import normalize_payload


def run_pipeline() -> None:
    settings = get_settings()
    payload = fetch_api_payload(
        url=settings.api_url,
        headers=settings.api_headers,
        timeout_seconds=settings.api_timeout_seconds,
    )

    records = normalize_payload(payload)

    loader = SnowflakeLoader(settings)
    loader.ensure_table()
    inserted = loader.load_records(records=records, source_name=settings.api_source_name)

    print(f"Pipeline completed successfully. Inserted {inserted} record(s).")
