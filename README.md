# IPL FlowForge

A clean Python data pipeline project that:
1. Pulls IPL data from any REST API endpoint.
2. Normalizes the response payload.
3. Loads records into a Snowflake warehouse table as `VARIANT` JSON.

## Project Structure

- `/main.py` — pipeline entrypoint
- `/requirements.txt` — Python dependencies
- `/.env.example` — required environment variables
- `/src/ipl_pipeline/config.py` — environment and runtime settings
- `/src/ipl_pipeline/api_client.py` — API extraction layer
- `/src/ipl_pipeline/transform.py` — payload normalization layer
- `/src/ipl_pipeline/snowflake_loader.py` — Snowflake DDL + DML loader
- `/src/ipl_pipeline/pipeline.py` — end-to-end orchestration

## Setup

1. Create a virtual environment and install dependencies:
   - `python -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -r requirements.txt`
2. Copy environment template:
   - `cp .env.example .env`
3. Fill all Snowflake credentials and API values in `.env`.

## Run

```bash
python main.py
```

On success, the pipeline creates the target table (if needed) and inserts the fetched API records.

## Snowflake Table Schema

The loader creates this table automatically:

- `ingestion_id STRING`
- `source STRING`
- `ingested_at TIMESTAMP_TZ`
- `payload VARIANT`
