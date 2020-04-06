import logging
import json


from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as psf

# TODO Create a schema for incoming resources
schema = StructType([
    StructField("crime_id", StringType(), True),
    StructField("original_crime_type_name", StringType(), True),
    StructField("report_date", StringType(), True),
    StructField("call_date", StringType(), True),
    StructField("offense_date", StringType(), True),
    StructField("call_time", StringType(), True),
    StructField("call_date_time", StringType(), True),
    StructField("disposition", StringType(), True),
    StructField("address", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("agency_id", StringType(), True),
    StructField("address_type", StringType(), True),
    StructField("common_location", StringType(), True)
])


def run_spark_job(spark):
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "udacity.sf-crime-data") \
        .option("maxOffsetPerTrigger", "200") \
        .option("startingOffsets", "earliest") \
        .load()

    df.printSchema()

    kafka_df = df.selectExpr("CAST(value AS STRING)")

    service_table = kafka_df \
        .select(psf.from_json(kafka_df.value, schema).alias("CRIME_DATA")) \
        .select("CRIME_DATA.*")

    service_table.printSchema()

    distinct_table = service_table \
        .select(service_table.call_date_time, service_table.original_crime_type_name, service_table.disposition)

    distinct_table = distinct_table.withColumn("call_timestamp", psf.to_timestamp(service_table.call_date_time))

    distinct_table.printSchema()

    agg_df = distinct_table \
        .groupBy([distinct_table.original_crime_type_name, distinct_table.disposition]).count()

    radio_code_json_filepath = "radio_code.json"
    radio_code_df = spark.read.json(radio_code_json_filepath)

    radio_code_df = radio_code_df.withColumnRenamed("disposition_code", "disposition")

    join_query = agg_df.join(radio_code_df, "disposition")

    query = join_query \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

    query.awaitTermination()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    sparkConf = SparkConf() \
        .setAppName("KafkaSparkStructuredStreaming") \
        .setMaster("spark://my-desktop:7077")

    spark = SparkSession \
        .builder \
        .config(conf=sparkConf) \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    logger.info("Spark started")

    run_spark_job(spark)

    spark.stop()
