from contextlib import contextmanager

from pyspark.sql import Column, DataFrame, SparkSession
from pyspark.sql import functions as f


@contextmanager
def spark_session() -> SparkSession:
    spark = SparkSession.builder.appName(f"app").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    yield spark
    spark.stop()


def read(spark: SparkSession) -> DataFrame:
    return spark.read \
        .csv("data/raw", header=True, inferSchema=True)


def info(df: DataFrame, title: str) -> None:
    print(title)
    print(f"Records: {df.count()}")
    df.printSchema()
    df.show(5, truncate=False)


def pre_processing(data: DataFrame) -> DataFrame:
    return (
        data
        .select(f.col("nameOrig").alias("name_origin"),
                f.col("type"),
                f.col("amount"),
                f.col("isFraud").alias("is_fraud"))
        .groupBy("name_origin")
        .agg(f.count("*").alias("n_transactions"),
             f.sum("is_fraud").alias("n_frauds"),
             f.collect_list(f.struct("type", "amount", "is_fraud")).alias("transactions"))
        .filter(f.col("n_frauds") > 0)
        .filter(f.col("n_transactions") != f.col("n_frauds"))
        .orderBy(f.desc("n_transactions"), f.col("name_origin"))
    )


def update_struct_field(column: Column) -> Column:
    return column.withField(
        "is_fraud",
        column.getField("is_fraud") == 1
    )


def not_fraud(column: Column) -> Column:
    return ~column.getField("is_fraud")


def calculate_transactions(data: DataFrame) -> DataFrame:
    return (
        data
        .withColumn("transactions", f.transform("transactions", update_struct_field))
        .withColumn("transactions", f.filter("transactions", not_fraud))
    )


if __name__ == "__main__":
    with spark_session() as ss:

        df = read(ss)
        info(df, "🥩 Raw Dataset")

        df = pre_processing(df)
        info(df, "🧹 Pre Processing")

        df = calculate_transactions(df)
        info(df, "🤘 Let's Rock")
