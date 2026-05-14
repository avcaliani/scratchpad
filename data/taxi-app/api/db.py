import os
import time

import databricks.sql as dbsql

_state: dict = {"conn": None}

_QUERY = (
    "SELECT trip_id, tpep_pickup_datetime, tpep_dropoff_datetime, "
    "trip_distance, fare_amount, pickup_zip, dropoff_zip, "
    "flag_invalid_fare, flag_invalid_distance, flag_invalid_timestamp, "
    "flag_null_critical_fields, flag_unrealistic_distance, "
    "flag_unrealistic_fare, flag_zero_distance_paid, "
    "record_quality_status, ingestion_timestamp "
    "FROM workspace.gold.nyctaxi_trips WHERE trip_id = %s"
)


def _get_conn() -> dbsql.client.Connection:
    if _state["conn"] is None:
        _state["conn"] = dbsql.connect(
            server_hostname=os.environ["DATABRICKS_HOST"],
            http_path=os.environ["DATABRICKS_HTTP_PATH"],
        )
    return _state["conn"]


def query_trip(trip_id: str) -> tuple[dict | None, float]:
    try:
        cursor = _get_conn().cursor()
        t0 = time.monotonic()
        cursor.execute(_QUERY, (trip_id,))
        row = cursor.fetchone()
        duration_ms = (time.monotonic() - t0) * 1000
        if row is None:
            return None, duration_ms
        return {col[0]: val for col, val in zip(cursor.description, row)}, duration_ms
    except Exception:
        _state["conn"] = None
        raise
