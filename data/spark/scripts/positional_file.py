from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from pyspark.sql import Column, DataFrame, SparkSession
from pyspark.sql import functions as f

ROOT = Path(__file__).parent.parent
SAMPLE = ROOT / "samples" / "duff_sales.csv"
BUCKET = ROOT / "data"


@contextmanager
def spark_session() -> Iterator[SparkSession]:
    spark = SparkSession.builder.appName("positional-file").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    yield spark
    spark.stop()


def read(spark: SparkSession, file: str) -> DataFrame:
    print(f"Reading file '{file}'...")
    return spark.read \
        .option("header", "true") \
        .option("delimiter", ",") \
        .csv(file)


def save(df: DataFrame, path: str) -> None:
    print(f"Writing data to '{path}'...")
    df.coalesce(1) \
        .write \
        .mode("overwrite") \
        .text(path)


def to_text(column: Column, size: int, character: str) -> Column:
    return f.lpad(f.trim(f.regexp_replace(column, r"\D", "")), size, character)


def prepare(df: DataFrame) -> DataFrame:
    parsed = df.orderBy(f.col("date"), f.col("bar")).select(
        to_text(f.col("date"), 8, "0"),
        to_text(f.col("unit_price"), 12, "0"),
        to_text(f.col("total_sales"), 10, "0"),
        f.lpad(f.upper(f.trim(f.col("bar"))), 25, " "),
    )
    return parsed.select(f.concat(*[f.col(c) for c in parsed.columns]))


if __name__ == "__main__":
    with spark_session() as ss:

        df = read(ss, str(SAMPLE))
        print(f"This file has {df.count()} records.")
        df.printSchema()

        save(prepare(df), str(BUCKET / "duff_sales"))

        print("That's all folks o/")
