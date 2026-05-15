<div align="center">
  <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExam9ydzY0eW5vZm0yYnhyamYxeGQyN3M4ZjM5NjczOThsNGxpMmZ2OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/oqGDRaWA5Wz8mfLC5e/giphy.gif" width="160px" />
  <h1>NYC Taxi App</h1>
  <p>End-to-end data pipeline demo — from raw NYC taxi data to a searchable web app, fully deployed on Databricks.</p>
</div>

<div align="center">

![#](https://img.shields.io/badge/python-3.11.x-yellow.svg)
![#](https://img.shields.io/badge/fastapi-0.136.1-009688.svg)
![#](https://img.shields.io/badge/databricks-apps-FF3621.svg)
![License](https://img.shields.io/github/license/avcaliani/deep-dive-fast-api?logo=apache&color=lightseagreen)

</div>

## Quick Start

Create a virtual environment and install dependencies.

```bash
# 👇 Setting PyEnv version
pyenv local 3.11.0

# 👇 Virtual Environment
python -m venv .venv \
  && source .venv/bin/activate \
  && pip install -r requirements.txt
```

Start the API server.

```bash
uvicorn main:app --reload
```

The app is now running at `http://127.0.0.1:8000`.

## Pipeline

Run the gold table script directly in Databricks SQL.

```
pipelines/gold_nyctaxi_trips.sql
```

It reads from `samples.nyctaxi.trips` and writes to `workspace.gold.nyctaxi_trips` with deterministic trip IDs, 6 quality flags, and Liquid Clustering.

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/api/trips/{trip_id}` | Fetch a trip by ID |

`trip_id` is a 64-character SHA256 hex string. Returns all 15 gold columns as JSON.

### Sample Trip IDs

<!-- Add real trip IDs here after running the pipeline -->
| trip_id | Description |
|---|---|
| `...` | ... |

### Example

```bash
curl http://127.0.0.1:8000/api/trips/<trip_id>
```

```json
{
  "trip_id": "a3f1...",
  "tpep_pickup_datetime": "2024-01-15T08:23:00",
  "tpep_dropoff_datetime": "2024-01-15T08:41:00",
  "trip_distance": 3.2,
  "fare_amount": 14.5,
  "pickup_zip": 10001,
  "dropoff_zip": 10003,
  "ingestion_timestamp": "2024-01-15T10:00:00",
  "record_quality_status": "VALID",
  "flag_invalid_fare": false,
  "flag_invalid_distance": false,
  "flag_invalid_timestamp": false,
  "flag_unrealistic_distance": false,
  "flag_unrealistic_fare": false,
  "flag_zero_distance_paid": false
}
```

## Deploy

```bash
./scripts/deploy.sh
```

> 💡 Warm up the SQL Warehouse before demoing — first query after auto-stop takes 30–60s.

## References

- [FastAPI docs](https://fastapi.tiangolo.com/)
- [Databricks SQL Connector](https://docs.databricks.com/en/dev-tools/python-sql-connector.html)
- [Databricks Apps](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html)
- [Alpine.js](https://alpinejs.dev/)
- [TailwindCSS](https://tailwindcss.com/)
