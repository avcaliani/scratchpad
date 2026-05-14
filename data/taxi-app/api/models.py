from pydantic import BaseModel


class DataQualityChecks(BaseModel):
    status: str
    invalid_fare: bool
    invalid_distance: bool
    invalid_timestamp: bool
    null_critical_fields: bool
    unrealistic_distance: bool
    unrealistic_fare: bool
    zero_distance_paid: bool

    @classmethod
    def from_row(cls, row: dict) -> "DataQualityChecks":
        return cls(
            status=row["record_quality_status"],
            invalid_fare=row["flag_invalid_fare"],
            invalid_distance=row["flag_invalid_distance"],
            invalid_timestamp=row["flag_invalid_timestamp"],
            null_critical_fields=row["flag_null_critical_fields"],
            unrealistic_distance=row["flag_unrealistic_distance"],
            unrealistic_fare=row["flag_unrealistic_fare"],
            zero_distance_paid=row["flag_zero_distance_paid"],
        )


class TripResponse(BaseModel):
    trip_id: str
    tpep_pickup_datetime: str
    tpep_dropoff_datetime: str
    trip_distance: float
    fare_amount: float
    pickup_zip: int
    dropoff_zip: int
    ingestion_timestamp: str
    data_quality_checks: DataQualityChecks

    @classmethod
    def from_row(cls, row: dict) -> "TripResponse":
        return cls(
            trip_id=row["trip_id"],
            tpep_pickup_datetime=row["tpep_pickup_datetime"].isoformat(),
            tpep_dropoff_datetime=row["tpep_dropoff_datetime"].isoformat(),
            trip_distance=row["trip_distance"],
            fare_amount=row["fare_amount"],
            pickup_zip=row["pickup_zip"],
            dropoff_zip=row["dropoff_zip"],
            ingestion_timestamp=row["ingestion_timestamp"].isoformat(),
            data_quality_checks=DataQualityChecks.from_row(row),
        )
