-- Run this script manually in a Databricks SQL worksheet.

-- 
-- SETUP ⚙️
--

CREATE SCHEMA IF NOT EXISTS workspace.gold;


---
--- GOLD LAYER 👑
---

CREATE OR REPLACE TABLE workspace.gold.nyctaxi_trips
USING DELTA
CLUSTER BY (trip_id)
AS
WITH base AS (
  SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    trip_distance,
    fare_amount,
    pickup_zip,
    dropoff_zip
  FROM samples.nyctaxi.trips
),

with_flags AS (
  SELECT
    sha2(concat_ws('||',
      cast(tpep_pickup_datetime AS string),
      cast(tpep_dropoff_datetime AS string),
      cast(pickup_zip AS string),
      cast(dropoff_zip AS string),
      cast(trip_distance AS string),
      cast(fare_amount AS string)
    ), 256)                                                       AS trip_id,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    trip_distance,
    fare_amount,
    pickup_zip,
    dropoff_zip,
    fare_amount < 0                                               AS flag_invalid_fare,
    trip_distance < 0                                             AS flag_invalid_distance,
    tpep_dropoff_datetime < tpep_pickup_datetime                  AS flag_invalid_timestamp,
    tpep_pickup_datetime IS NULL OR tpep_dropoff_datetime IS NULL  AS flag_null_critical_fields,
    trip_distance > 100                                           AS flag_unrealistic_distance,
    fare_amount > 1000                                            AS flag_unrealistic_fare,
    trip_distance = 0 AND fare_amount > 0                         AS flag_zero_distance_paid
  FROM base
),

with_quality AS (
  SELECT
    *,
    CASE
      WHEN flag_invalid_fare OR flag_invalid_distance OR flag_invalid_timestamp
        OR flag_null_critical_fields OR flag_unrealistic_distance
        OR flag_unrealistic_fare OR flag_zero_distance_paid
      THEN 'INVALID'
      ELSE 'VALID'
    END                  AS record_quality_status,
    current_timestamp()  AS ingestion_timestamp
  FROM with_flags
),

deduped AS (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY trip_id ORDER BY tpep_pickup_datetime DESC) AS rn
  FROM with_quality
)

SELECT
  trip_id,
  tpep_pickup_datetime,
  tpep_dropoff_datetime,
  trip_distance,
  fare_amount,
  pickup_zip,
  dropoff_zip,
  flag_invalid_fare,
  flag_invalid_distance,
  flag_invalid_timestamp,
  flag_null_critical_fields,
  flag_unrealistic_distance,
  flag_unrealistic_fare,
  flag_zero_distance_paid,
  record_quality_status,
  ingestion_timestamp
FROM deduped
WHERE rn = 1;


--
-- VALIDATION ✅
--
select 
    format_number(count(*), 0) as n_rows 
from workspace.gold.nyctaxi_trips;

select * from workspace.gold.nyctaxi_trips limit 100;

-- Sample IDs for testing:
--  1. 3eed23d2881bf5c439c98b379eb0d79f5597668b22a1f6c821d06a7a9de0e7c0 [valid]
--  2. 50019912b8ebac4fefed0f28a290cec5ac3be9bb3b9222136aed189455a03b94 [invalid]
