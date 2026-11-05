# Scratchpad

Quick experiments and spikes. Each folder is self-contained.

**NEVER run Python commands outside the virtual env.**
Use `uv run ...` from the folder that owns the `pyproject.toml`.

## Back-end

| Path | Stack | What it is |
| ---- | ----- | ---------- |
| `back-end/fast-api/web-sockets` | Python, FastAPI | WebSockets snippet: intercom chat + ticker, own README |

## Data

| Path | Stack | What it is |
| ---- | ----- | ---------- |
| `data/spark` | Python, PySpark | Spark snippets sharing one uv project, see its README |
| `data/taxi-app` | Python, FastAPI | Taxi data API app — has its own `CLAUDE.md` |

## Front-end

| Path | Stack | What it is |
| ---- | ----- | ---------- |
| `front-end/dag-visualizer` | HTML, JS | Dynamic DAG in the browser using vis-network + Alpine.js |

## Misc

| Path | Stack | What it is |
| ---- | ----- | ---------- |
| `misc/elk-app` | Python, Docker, ELK | Elasticsearch + Logstash + Kibana stack via Docker Compose |
| `misc/python` | Python | Standalone snippets: decorator pattern, venv detection |
