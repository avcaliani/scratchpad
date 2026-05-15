import logging
import os
import time

import databricks.sql as dbsql
from databricks.sql.client import Connection

logger = logging.getLogger(__name__)

_state: dict = {"conn": None}


def _get_conn() -> Connection:
    if _state["conn"] is None:
        _state["conn"] = dbsql.connect(
            server_hostname=os.environ["DATABRICKS_HOST"],
            http_path=os.environ["DATABRICKS_HTTP_PATH"],
        )
        logger.info("Warehouse connection established")
    return _state["conn"]


def _run_query(query: str, params: tuple) -> tuple[dict | None, float]:
    start = time.monotonic()
    try:
        cursor = _get_conn().cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        duration_ms = (time.monotonic() - start) * 1000
        if row is None:
            return None, duration_ms
        return {col[0]: val for col, val in zip(cursor.description, row)}, duration_ms
    except Exception:
        _state["conn"] = None
        logger.exception("Warehouse connection failed")
        raise


def find_trip(trip_id: str) -> tuple[dict | None, float]:
    return _run_query(
        query="SELECT * FROM workspace.gold.nyctaxi_trips WHERE trip_id = %s",
        params=(trip_id,),
    )
