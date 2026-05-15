import inspect
import json
import logging
import re

from fastapi import APIRouter, HTTPException

from api.db import find_trip

logger = logging.getLogger(__name__)

TRIP_ID_RE = re.compile(r"^[0-9a-f]{64}$")

router = APIRouter()


def _log(trip_id: str, status_code: int, query_duration_ms: float | None) -> None:
    method_name = inspect.currentframe().f_back.f_code.co_name
    message = {
        "endpoint": method_name,
        "trip_id": trip_id,
        "status_code": status_code,
        "query_duration_ms": (
            round(query_duration_ms) if query_duration_ms is not None else None
        ),
    }
    logger.info(json.dumps(message))


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/api/trips/{trip_id}")
def get_trip(trip_id: str) -> dict:
    if not TRIP_ID_RE.match(trip_id):
        raise HTTPException(status_code=400, detail="Invalid trip_id format")

    try:
        row, duration_ms = find_trip(trip_id)
    except Exception:
        _log(trip_id, 503, None)
        raise HTTPException(status_code=503, detail="Warehouse unavailable")

    if row is None:
        _log(trip_id, 404, duration_ms)
        raise HTTPException(status_code=404, detail="Trip not found")

    _log(trip_id, 200, duration_ms)
    return row
