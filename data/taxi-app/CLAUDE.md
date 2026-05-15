# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

End-to-end demo: NYC taxi data pipeline → REST API → single-page frontend, all running on Databricks.

Specs live in `.spec-docs/`. They are the source of truth. Check status frontmatter before implementing — `todo` means not started, update to `in progress` / `done` as work proceeds.

## Architecture

```
main.py               # FastAPI app, router registration, StaticFiles mount
app.yaml              # Databricks Apps startup config
requirements.txt      # Pinned dependencies
requirements-dev.txt  # Test dependencies (pytest, httpx) — not deployed
api/
  db.py               # SQL query, lazy singleton connection
  routes.py           # APIRouter, trip_id validation, structured JSON logging
pipelines/
  gold_nyctaxi_trips.sql  # Databricks SQL — builds the gold table
static/
  index.html          # Single-page UI — Alpine.js + TailwindCSS via CDN
scripts/
  deploy.sh           # databricks apps deploy
tests/
  test_app.py         # Unit tests — DB calls mocked via api.db.dbsql.connect
```

## Commands

```bash
# Run tests (inside venv, from data/taxi-app/)
cd data/taxi-app && pytest tests/

# Run locally (inside venv; needs DATABRICKS_HOST + DATABRICKS_HTTP_PATH set)
uvicorn main:app --reload

# Deploy to Databricks Apps
./scripts/deploy.sh
```

## Key Decisions

**Data pipeline (`pipelines/gold_nyctaxi_trips.sql`)**
- `trip_id` = SHA256 of 6 concatenated fields (see spec `002` for exact expression) — never use `monotonically_increasing_id()`
- No dedup step — `trip_id` is derived from all 6 fields, so identical `trip_id` means identical row
- `flag_null_critical_fields` was merged into `flag_invalid_timestamp` (null timestamps are a subset of invalid timestamps)
- Load strategy: full overwrite; table uses Liquid Clustering on `trip_id`

**API (`api/`)**
- Auth: OAuth/managed identity — Databricks Apps runtime credentials inherited automatically, no token handling
- `trip_id` validation: must be a 64-character lowercase hex string; reject with `400` before querying
- Error codes: `400` (bad format), `404` (not found), `503` (warehouse failure)
- Query inlined in `api/db.py` using `%s` placeholder (DB-API 2.0) — never interpolate `trip_id` into the SQL string
- Connection singleton: `_state["conn"]` in `api/db.py` — lazy-initialized, reset to `None` on exception to trigger reconnect
- Raw dict returned directly from `find_trip()` — no model layer, frontend consumes DB column names as-is
- `StaticFiles` mount at `/` must be declared **last** in `app.py` — it swallows all unmatched routes
- Mock patch target for tests: `api.db.dbsql.connect`; reset `api.db._state["conn"] = None` between tests

**Frontend (`static/index.html`)**
- No build step; Alpine.js and TailwindCSS loaded from CDN
- Quality flags rendered as colored badges; `record_quality_status` as a prominent VALID/INVALID badge

**Observability**
- Every request logs structured JSON: `endpoint`, `trip_id`, `status_code`, `query_duration_ms`
- Warehouse errors log full exception + stack trace
