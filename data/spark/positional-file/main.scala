import org.apache.spark.sql.{SparkSession, DataFrame, Column}
import org.apache.spark.sql.functions._
import spark.implicits._


def read(spark: SparkSession, file: String): DataFrame = {
    println(s"Reading file '$file'...")
    spark.read
        .option("header", "true")
        .option("delimiter", ",")
        .csv(file)   
}


def save(df: DataFrame, path: String): Unit = {
    println(s"Writing data to '$path'...")
    df.coalesce(1)
        .write
        .mode("overwrite")
        .text(path)
}


def toText(column: Column, size: Int, character: String): Column = {
    lpad(trim(regexp_replace(column, "\\D", "")), size, character)
}


def prepare(df: DataFrame): DataFrame = {
    // Parsing Data
    val parsed = df.orderBy($"Date", $"region")
        .select(
            toText($"Date",              8,  "0"),
            toText($"AveragePrice",      12, "0"),
            toText($"Total Volume",      10, "0"),
            lpad(upper(trim($"region")), 25, " ")
        )
    // To Single Column
    parsed.select(concat(parsed.columns.map(col(_)):_*))
}



//  ______     __  __     __   __    
// /\  == \   /\ \/\ \   /\ "-.\ \   
// \ \  __<   \ \ \_\ \  \ \ \-.  \  
//  \ \_\ \_\  \ \_____\  \ \_\\"\_\ 
//   \/_/ /_/   \/_____/   \/_/ \/_/ 

val BUCKET = "./data"

val df = read(spark, s"$BUCKET/avocado.csv")
println(s"This file has ${df.count()} records.")
df.printSchema()

save(prepare(df), s"$BUCKET/avocado")

println("That's all folks o/")
sys.exit(0)
