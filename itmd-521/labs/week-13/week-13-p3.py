from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

# Removing hard coded password - using os module to import them
import os
import sys

conf = SparkConf()
conf.set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.3.0')
conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')

conf.set('spark.hadoop.fs.s3a.access.key', os.getenv('ACCESSKEY'))
conf.set('spark.hadoop.fs.s3a.secret.key', os.getenv('SECRETKEY'))
# Configure these settings
# https://medium.com/@dineshvarma.guduru/reading-and-writing-data-from-to-minio-using-spark-8371aefa96d2
conf.set("spark.hadoop.fs.s3a.path.style.access", "true")
conf.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
# https://github.com/minio/training/blob/main/spark/taxi-data-writes.py
# https://spot.io/blog/improve-apache-spark-performance-with-the-s3-magic-committer/
conf.set('spark.hadoop.fs.s3a.committer.magic.enabled','true')
conf.set('spark.hadoop.fs.s3a.committer.name','magic')
# Internal IP for S3 cluster proxy
conf.set("spark.hadoop.fs.s3a.endpoint", "http://infra-minio-proxy-vm0.service.consul")

spark = SparkSession.builder.appName("sthupakula p3 ").config('spark.driver.host','spark-edge.service.consul').config(conf=conf).getOrCreate()


splitDF = spark.read.parquet('s3a://sthupakula/90.parquet')

#The average df calculates the average for each month of year by groupby, the where clause will strip out the temperatures below and 
# above 50
averagedf = splitDF.select(month(col('ObservationDate')).alias('Month'),year(col('ObservationDate')).alias('Year'),col('AirTemperature').alias('Temperature'))\
             .where((col('Temperature') > -50) & (col('Temperature') < 50)).groupBy('Month','Year').agg(avg('Temperature').alias('average')).orderBy('Year','Month')
#The stddf calculates the average from the averagedf for all month over the decade with groupby month
stddf = averagedf.select(col('Month'),col('average')).groupBy('Month').agg(stddev('average')).orderBy('Month')
csvdf = stddf
#Writing output to minio
stddf.write.mode("overwrite").parquet("s3a://sthupakula/part-three.parquet")
csvdf.write.mode("overwrite").option("header","true").csv("s3a://sthupakula/part-three.csv")

