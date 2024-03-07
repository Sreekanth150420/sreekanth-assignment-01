from pyspark.sql import SparkSession


spark = SparkSession.builder.appName("ORD Departure Delays").getOrCreate()

parturedelays_df = spark.read.parquet("path/to/departuredelays.parquet")

ord_departuredelays_df = departuredelays_df.filter(departuredelays_df["Origin"] == "ORD")

ord_departuredelays_df.show(10)

ord_departuredelays_df.write.parquet("path/to/ord_departuredelays.parquet")

