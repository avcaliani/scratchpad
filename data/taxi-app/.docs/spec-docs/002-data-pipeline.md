---
status: done
created: 2026-05-12
updated: 2026-05-14
---

# 2. Data Pipeline

**Stack:** Databricks SQL · Delta Lake · Unity Catalog  
**Source:** `samples.nyctaxi.trips`  
**Target:** `workspace.gold.nyctaxi_trips`  
**Deliverable:** `pipeline/gold_nyctaxi_trips.sql`

---

## Trip ID

Generate a deterministic SHA256 hash. Do not use `monotonically_increasing_id()`.

```sql
sha2(concat_ws('||',
  cast(tpep_pickup_datetime as string),
  cast(tpep_dropoff_datetime as string),
  cast(pickup_zip as string),
  cast(dropoff_zip as string),
  cast(trip_distance as string),
  cast(fare_amount as string)
), 256) AS trip_id
```

---

## Quality Flags

| Column | Expression |
|---|---|
| `flag_invalid_fare` | `fare_amount < 0` |
| `flag_invalid_distance` | `trip_distance < 0` |
| `flag_invalid_timestamp` | `tpep_dropoff_datetime < tpep_pickup_datetime` |
| `flag_null_critical_fields` | `tpep_pickup_datetime IS NULL OR tpep_dropoff_datetime IS NULL` |
| `flag_unrealistic_distance` | `trip_distance > 100` |
| `flag_unrealistic_fare` | `fare_amount > 1000` |
| `flag_zero_distance_paid` | `trip_distance = 0 AND fare_amount > 0` |

---

## Record Quality Status

```sql
CASE
  WHEN flag_invalid_fare OR flag_invalid_distance OR flag_invalid_timestamp
    OR flag_null_critical_fields OR flag_unrealistic_distance
    OR flag_unrealistic_fare OR flag_zero_distance_paid
  THEN 'INVALID'
  ELSE 'VALID'
END AS record_quality_status
```

---

## Deduplication

After computing `trip_id`, keep one row per hash before writing. Use the latest pickup timestamp as the tiebreaker.

```sql
ROW_NUMBER() OVER (PARTITION BY trip_id ORDER BY tpep_pickup_datetime DESC) = 1
```

---

## Ingestion Timestamp

```sql
current_timestamp() AS ingestion_timestamp
```

---

## Gold Table

- Create schema `workspace.gold` if not exists
- `CREATE OR REPLACE TABLE workspace.gold.nyctaxi_trips`
- Format: Delta
- Load: full overwrite
- Clustering: `CLUSTER BY (trip_id)` (Liquid Clustering)

---

## Schema

| Column | Type |
|---|---|
| trip_id | STRING |
| tpep_pickup_datetime | TIMESTAMP |
| tpep_dropoff_datetime | TIMESTAMP |
| trip_distance | DOUBLE |
| fare_amount | DOUBLE |
| pickup_zip | INT |
| dropoff_zip | INT |
| flag_invalid_fare | BOOLEAN |
| flag_invalid_distance | BOOLEAN |
| flag_invalid_timestamp | BOOLEAN |
| flag_null_critical_fields | BOOLEAN |
| flag_unrealistic_distance | BOOLEAN |
| flag_unrealistic_fare | BOOLEAN |
| flag_zero_distance_paid | BOOLEAN |
| record_quality_status | STRING |
| ingestion_timestamp | TIMESTAMP |
