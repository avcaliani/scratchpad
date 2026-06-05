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
WITH with_flags AS (
  SELECT
    sha2(concat_ws('||',
      cast(tpep_pickup_datetime AS string),
      cast(tpep_dropoff_datetime AS string),
      cast(pickup_zip AS string),
      cast(dropoff_zip AS string),
      cast(trip_distance AS string),
      cast(fare_amount AS string)
    ), 256) AS trip_id,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    trip_distance,
    fare_amount,
    pickup_zip,
    dropoff_zip,
    fare_amount < 0                                               AS flag_invalid_fare,
    trip_distance < 0                                             AS flag_invalid_distance,
    tpep_pickup_datetime IS NULL OR tpep_dropoff_datetime IS NULL
      OR tpep_dropoff_datetime < tpep_pickup_datetime             AS flag_invalid_timestamp,
    trip_distance > 100                                           AS flag_unrealistic_distance,
    fare_amount > 1000                                            AS flag_unrealistic_fare,
    trip_distance = 0 AND fare_amount > 0                         AS flag_zero_distance_paid
  FROM samples.nyctaxi.trips
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
  flag_unrealistic_distance,
  flag_unrealistic_fare,
  flag_zero_distance_paid,
  CASE
    WHEN flag_invalid_fare OR flag_invalid_distance OR flag_invalid_timestamp
      OR flag_unrealistic_distance OR flag_unrealistic_fare OR flag_zero_distance_paid
    THEN 'INVALID'
    ELSE 'VALID'
  END                  AS record_quality_status,
  current_timestamp()  AS ingestion_timestamp
FROM with_flags;


--
-- VALIDATION ✅
--
select 
    format_number(count(*), 0) as n_rows 
from workspace.gold.nyctaxi_trips;

select * from workspace.gold.nyctaxi_trips limit 100;
