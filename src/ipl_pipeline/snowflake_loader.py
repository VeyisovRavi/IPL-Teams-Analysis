from __future__ import annotations

import json
import uuid
from typing import Any, Iterable, List, Tuple

import snowflake.connector
from snowflake.connector.connection import SnowflakeConnection

from src.ipl_pipeline.config import Settings


class SnowflakeLoader:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def _connect(self) -> SnowflakeConnection:
        return snowflake.connector.connect(
            account=self._settings.snowflake_account,
            user=self._settings.snowflake_user,
            **{"password": self._settings.snowflake_password},
            role=self._settings.snowflake_role,
            warehouse=self._settings.snowflake_warehouse,
            database=self._settings.snowflake_database,
            schema=self._settings.snowflake_schema,
        )

    def _table_identifier(self) -> str:
        return (
            f'"{self._settings.snowflake_database}".'
            f'"{self._settings.snowflake_schema}".'
            f'"{self._settings.snowflake_table}"'
        )

    def ensure_table(self) -> None:
        statement = f"""
        CREATE TABLE IF NOT EXISTS {self._table_identifier()} (
            ingestion_id STRING,
            source STRING,
            ingested_at TIMESTAMP_TZ,
            payload VARIANT
        )
        """

        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(statement)

    def load_records(self, records: Iterable[Any], source_name: str) -> int:
        rows: List[Tuple[str, str, str]] = [
            (str(uuid.uuid4()), source_name, json.dumps(record, ensure_ascii=False))
            for record in records
        ]

        if not rows:
            return 0

        insert_sql = f"""
        INSERT INTO {self._table_identifier()} (ingestion_id, source, ingested_at, payload)
        SELECT %s, %s, CURRENT_TIMESTAMP(), PARSE_JSON(%s)
        """

        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(insert_sql, rows)

        return len(rows)
