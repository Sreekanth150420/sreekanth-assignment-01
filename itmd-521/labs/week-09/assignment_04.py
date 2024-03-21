from pyspark.sql import SparkSession
from pyspark.sql.functions import desc
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Assignment 04 - MySQL Integration") \
    .config("spark.jars", "/path/to/spark/jars/mysql-connector-java-8.0.x.jar") \
    .getOrCreate()


url = "jdbc:mysql://localhost:3306/employees"
properties = {"user": "yourusername", "password": "yourpassword", "driver": "com.mysql.cj.jdbc.Driver"}


df_employees = spark.read.jdbc(url=url, table="employees", properties=properties)


print(f"Number of records in employees table: {df_employees.count()}")


df_employees.printSchema()


df_salaries = spark.read.jdbc(url=url, table="salaries", properties=properties)


df_top_salaries = df_salaries.orderBy(df_salaries.salary.desc()).limit(10000)

df_top_salaries.write.jdbc(url=url, table="aces", mode="overwrite", properties=properties)

df_top_salaries.write.option("compression", "snappy").csv("/home/vagrant/test_db/top_salaries.csv")


