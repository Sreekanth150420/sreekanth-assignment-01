from pyspark.sql import SparkSession
import sys

def main(file_path):

    spark = SparkSession.builder.appName("Departure Delays Analysis").getOrCreate()


    flight_data = spark.read.option("header", "true").csv(file_path)


    flight_data.createOrReplaceTempView("flight_data")


    sql_query_1 = """
    SELECT origin, destination, count(*) AS total_flights
    FROM flight_data
    GROUP BY origin, destination
    """
    spark.sql(sql_query_1).show(10)

    # Spark SQL to run the second query
    sql_query_2 = """
    SELECT origin, AVG(delay) AS avg_delay
    FROM flight_data
    WHERE delay > 0
    GROUP BY origin
    """
    spark.sql(sql_query_2).show(10)


    flight_data.groupBy("origin", "destination").count().withColumnRenamed("count", "total_flights").show(10)


    flight_data.filter(flight_data.delay > 0).groupBy("origin").avg("delay").withColumnRenamed("avg(delay)", "avg_delay").show(10)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: assignment_03.py <file_path>")
        sys.exit(-1)
    main(sys.argv[1])

