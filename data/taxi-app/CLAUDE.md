# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

End-to-end demo: NYC taxi data pipeline → REST API → single-page frontend, all running on Databricks.

Specs live in `.spec-docs/`. They are the source of truth. Check status frontmatter before implementing — `todo` means not started, update to `in progress` / `done` as work proceeds.

## Architecture

```
app.py                # FastAPI — all routes, DB query function, Pydantic models
app.yaml              # Databricks Apps startup config
requirements.txt      # Pinned dependencies
pipeline/
  gold_nyctaxi_trips.sql  # Databricks SQL — builds the gold table
static/
  index.html          # Single-page UI — Alpine.js + TailwindCSS via CDN
scripts/
  deploy.sh           # databricks apps deploy
```

## Commands

```bash
# Run locally
uvicorn app:app --reload

# Deploy to Databricks Apps
./scripts/deploy.sh
```

## Key Decisions

**Data pipeline (`pipeline/gold_nyctaxi_trips.sql`)**
- `trip_id` = SHA256 of 6 concatenated fields (see spec `002` for exact expression) — never use `monotonically_increasing_id()`
- Dedup after computing `trip_id`: `ROW_NUMBER() OVER (PARTITION BY trip_id ORDER BY tpep_pickup_datetime DESC) = 1`
- Load strategy: full overwrite; table uses Liquid Clustering on `trip_id`

**API (`app.py`)**
- Auth: OAuth/managed identity — Databricks Apps runtime credentials inherited automatically, no token handling
- `trip_id` validation: must be a 64-character lowercase hex string; reject with `400` before querying
- Error codes: `400` (bad format), `404` (not found), `503` (warehouse failure)
- Query inlined using `%s` placeholder (DB-API 2.0) — never interpolate `trip_id` into the SQL string
- `StaticFiles` mount at `/` must be declared **last** in `app.py` — it swallows all unmatched routes

**Frontend (`static/index.html`)**
- No build step; Alpine.js and TailwindCSS loaded from CDN
- Quality flags rendered as colored badges; `record_quality_status` as a prominent VALID/INVALID badge

**Observability**
- Every request logs structured JSON: `endpoint`, `trip_id`, `status_code`, `query_duration_ms`
- Warehouse errors log full exception + stack trace
