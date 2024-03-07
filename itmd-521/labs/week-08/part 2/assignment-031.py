from pyspark.sql import SparkSession
import sys

def main(file_path):

    spark = SparkSession.builder \
        .appName("US Delay Flights Analysis") \
        .config("spark.sql.catalogImplementation", "hive") \
        .enableHiveSupport() \
        .getOrCreate()


    flight_data = spark.read.option("header", "true").csv(file_path)


    flight_data.write.saveAsTable("us_delay_flights_tbl")


    filtered_flights = spark.sql("""
    SELECT *
    FROM us_delay_flights_tbl
    WHERE origin = 'ORD'
    AND to_date(date, 'MMdd') BETWEEN '2024-03-01' AND '2024-03-15'
    """)


    filtered_flights.createOrReplaceTempView("chicago_flights_temp_view")


    spark.sql("SELECT * FROM chicago_flights_temp_view").show(5)

    columns = spark.catalog.listColumns("us_delay_flights_tbl")
    print("Columns in us_delay_flights_tbl:")
    for column in columns:
        print(column.name)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: assignment-031.py <file_path>")
        sys.exit(-1)
    main(sys.argv[1])
