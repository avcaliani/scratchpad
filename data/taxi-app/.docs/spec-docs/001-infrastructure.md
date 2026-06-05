---
status: done
created: 2026-05-12
updated: 2026-06-05
---

# 1. Infrastructure

**Stack:** Databricks Apps · Databricks SQL Warehouse · Databricks CLI · Bash · YAML

---

## SQL Warehouse

- Create a SQL Warehouse with Photon enabled
- Configure auto-stop (warm up manually before demos)

---

## Databricks App

- Single Python process — FastAPI serves both API and frontend
- API routes: `/api/*` → query the SQL Warehouse
- Frontend: mount `static/` at `/` using `StaticFiles`
- Startup command: `uvicorn main:app --host 0.0.0.0 --port 8000`
- Auth: OAuth/managed identity — app inherits Databricks Apps runtime credentials, no token required

---

## Permissions

- Grant the app read-only access to `workspace.gold.nyctaxi_trips`
- No write permissions needed

---

## Deployment

- Deployment script using Databricks CLI (`databricks apps deploy`)
- Document local dev setup: how to run FastAPI locally against the warehouse

---

## Observability

Structured JSON log on every request:

| Field | Description |
|---|---|
| `endpoint` | Route path |
| `trip_id` | Input value (if applicable) |
| `status_code` | HTTP response code |
| `query_duration_ms` | Warehouse query time |

Log warehouse errors with full exception message and stack trace.
