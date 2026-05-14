import json
import logging
import re

from fastapi import APIRouter, HTTPException

from api.db import query_trip
from api.models import TripResponse

logger = logging.getLogger(__name__)

TRIP_ID_RE = re.compile(r"^[0-9a-f]{64}$")

router = APIRouter()


def _log(endpoint: str, trip_id: str, status_code: int, query_duration_ms: float | None) -> None:
    logger.info(json.dumps({
        "endpoint": endpoint,
        "trip_id": trip_id,
        "status_code": status_code,
        "query_duration_ms": round(query_duration_ms) if query_duration_ms is not None else None,
    }))


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/api/trips/{trip_id}")
def get_trip(trip_id: str) -> TripResponse:
    if not TRIP_ID_RE.match(trip_id):
        raise HTTPException(status_code=400, detail="Invalid trip_id format")

    try:
        row, duration_ms = query_trip(trip_id)
    except Exception:
        logger.exception("Warehouse error")
        _log("get_trip", trip_id, 503, None)
        raise HTTPException(status_code=503, detail="Warehouse unavailable")

    if row is None:
        _log("get_trip", trip_id, 404, duration_ms)
        raise HTTPException(status_code=404, detail="Trip not found")

    _log("get_trip", trip_id, 200, duration_ms)
    return TripResponse.from_row(row)
