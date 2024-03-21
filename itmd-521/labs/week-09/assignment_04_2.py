from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, current_date

spark = SparkSession.builder \
    .appName("Senior Engineer Analysis") \
    .config("spark.jars", "/path/to/mysql-connector-java-8.0.x.jar") \
    .getOrCreate()

query = "(SELECT * FROM titles WHERE title = 'Senior Engineer') AS senior_engineers"
url = "jdbc:mysql://localhost:3306/yourdatabase"
properties = {"user": "yourusername", "password": "yourpassword", "driver": "com.mysql.cj.jdbc.Driver"}

df_senior_engineers = spark.read.jdbc(url=url, query=query, properties=properties)

df_with_status = df_senior_engineers.withColumn(
    "status",
    expr("CASE WHEN to_date = '9999-01-01' THEN 'current' ELSE 'left' END")
)

df_with_status.groupBy("status").count().show()
df_with_status.filter(df_with_status.status == "left").createOrReplaceTempView("senior_engineers_left")
df_left = spark.sql("SELECT * FROM senior_engineers_left")

df_left.write \
    .format("jdbc") \
    .option("url", url) \
    .option("dbtable", "left_df") \
    .option("user", "yourusername") \
    .option("password", "yourpassword") \
    .mode("overwrite") \
    .save()
