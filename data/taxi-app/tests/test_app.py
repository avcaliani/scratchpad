from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

import api.db
from app import app

VALID_ID = "3eed23d2881bf5c439c98b379eb0d79f5597668b22a1f6c821d06a7a9de0e7c0"

_MOCK_ROW = {
    "trip_id": VALID_ID,
    "tpep_pickup_datetime": datetime(2024, 1, 15, 10, 30, 0),
    "tpep_dropoff_datetime": datetime(2024, 1, 15, 11, 0, 0),
    "trip_distance": 5.2,
    "fare_amount": 18.5,
    "pickup_zip": 10001,
    "dropoff_zip": 10002,
    "ingestion_timestamp": datetime(2024, 6, 1, 12, 0, 0),
    "record_quality_status": "VALID",
    "flag_invalid_fare": False,
    "flag_invalid_distance": False,
    "flag_invalid_timestamp": False,
    "flag_null_critical_fields": False,
    "flag_unrealistic_distance": False,
    "flag_unrealistic_fare": False,
    "flag_zero_distance_paid": False,
}


def _make_conn(row_data: dict | None) -> MagicMock:
    cols = list(_MOCK_ROW.keys())
    mock_cursor = MagicMock()
    mock_cursor.description = [(c,) for c in cols]
    mock_cursor.fetchone.return_value = list(row_data.values()) if row_data else None
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn


@pytest.fixture(autouse=True)
def databricks_env(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "mock-host")
    monkeypatch.setenv("DATABRICKS_HTTP_PATH", "/sql/mock")


@pytest.fixture(autouse=True)
def reset_db_conn():
    api.db._state["conn"] = None
    yield
    api.db._state["conn"] = None


@pytest.fixture
def client():
    return TestClient(app)


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


@patch("api.db.dbsql.connect")
def test_get_trip_success(mock_connect, client):
    mock_connect.return_value = _make_conn(_MOCK_ROW)
    resp = client.get(f"/api/trips/{VALID_ID}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["trip_id"] == VALID_ID
    assert body["trip_distance"] == 5.2
    assert body["fare_amount"] == 18.5
    assert body["pickup_zip"] == 10001
    assert body["data_quality_checks"]["status"] == "VALID"
    assert body["data_quality_checks"]["invalid_fare"] is False


@patch("api.db.dbsql.connect")
def test_get_trip_datetime_iso8601(mock_connect, client):
    mock_connect.return_value = _make_conn(_MOCK_ROW)
    resp = client.get(f"/api/trips/{VALID_ID}")
    body = resp.json()
    assert body["tpep_pickup_datetime"] == "2024-01-15T10:30:00"
    assert body["tpep_dropoff_datetime"] == "2024-01-15T11:00:00"
    assert body["ingestion_timestamp"] == "2024-06-01T12:00:00"


@pytest.mark.parametrize("bad_id", [
    "abc123",
    "3EED23D2881BF5C439C98B379EB0D79F5597668B22A1F6C821D06A7A9DE0E7C0",
    "3eed23d2881bf5c439c98b379eb0d79f5597668b22a1f6c821d06a7a9de0e7cZ",
    "3eed23d2881bf5c439c98b379eb0d79f5597668b22a1f6c821d06a7a9de0e7c",
])
def test_get_trip_invalid_id_returns_400(bad_id, client):
    resp = client.get(f"/api/trips/{bad_id}")
    assert resp.status_code == 400


@patch("api.db.dbsql.connect")
def test_get_trip_not_found_returns_404(mock_connect, client):
    mock_connect.return_value = _make_conn(None)
    resp = client.get(f"/api/trips/{VALID_ID}")
    assert resp.status_code == 404


@patch("api.db.dbsql.connect")
def test_get_trip_warehouse_error_returns_503(mock_connect, client):
    mock_connect.side_effect = Exception("Connection refused")
    resp = client.get(f"/api/trips/{VALID_ID}")
    assert resp.status_code == 503
