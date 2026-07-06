from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("audit_local_spark")
    .getOrCreate()
)

print("Spark version:", spark.version)