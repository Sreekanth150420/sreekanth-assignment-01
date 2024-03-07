from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("DepartureDelays").getOrCreate()

schema = StructType([
    StructField("date", DateType(), True),
    StructField("delay", IntegerType(), True),
    StructField("distance", IntegerType(), True),
    StructField("origin", StringType(), True),
    StructField("destination", StringType(), True),
])

df = spark.read.csv("/home/vagrant/LearningSparkV2/databricks-datasets/learning-spark-v2/flights/departuredelays.csv", schema=schema, header=True)
df.write.mode("overwrite").json("path/to/departuredelays.json")
df.write.mode("overwrite").parquet("path/to/departuredelays.parquet")

import lz4.frame
import json

json_data = df.toJSON().collect()
compressed_data = lz4.frame.compress(json.dumps(json_data).encode('utf-8'))

with open("path/to/departuredelays.json.lz4", "wb") as compressed_file:
    compressed_file.write(compressed_data)
import lz4.frame
import json


json_data = df.toJSON().collect()
compressed_data = lz4.frame.compress(json.dumps(json_data).encode('utf-8'))

with open("path/to/departuredelays.json.lz4", "wb") as compressed_file:
    compressed_file.write(compressed_data)


