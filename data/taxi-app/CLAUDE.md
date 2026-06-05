# Project Context & Purpose

End-to-end demo: NYC taxi data pipeline → REST API → single-page frontend, all on Databricks.
Specs in `.docs/spec-docs/` are the source of truth — check `status` frontmatter before implementing.

## Tech Stack & Dependencies

- **API:** Python, FastAPI, Databricks SQL Connector
- **Testing:** pytest, httpx
- **Frontend:** Alpine.js (CDN), no build step, no test step
- **Pipeline:** Databricks SQL, Delta Lake, Unity Catalog

## Project Structure

- Restful API
  - `main.py` — FastAPI App
  - `api/` — Database Connection / Endopoints
  - `static/` — HTML, CSS and JS Files
  - `tests/` — Unit Tests
- `scripts/`
  — `*.sql` - Data Pipelines
  — `*.sh` - DevOps Scripts
- `app.yaml` - Databricks Apps Configuration

## Development Guidelines

1. **API:** Auth is inherited automatically from Databricks Apps runtime — no token handling needed
2. **Testing:** Always run the unit tests inside the venv before declaring done; never commit failing tests

## Commands

```bash
uv sync                           # install all deps (creates/updates .venv)
uv run pytest tests/              # run tests
./scripts/deploy.sh               # deploy to Databricks Apps via git source
databricks apps run-local --prepare-environment --debug  # run locally (--prepare-environment only if .venv doesn't exist)
databricks apps run-local --debug                        # run locally (subsequent runs)
```
