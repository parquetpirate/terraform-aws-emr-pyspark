# Main PySpark entry point for distributed training on Amazon EMR

import os
import boto3
import traceback
from pyspark.sql import SparkSession
from log import write_log
from processing import clean_transform_data
from ml import train_ml_models

# Bucket name from environment (set by EMR or Terraform)
BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "")

# AWS credentials are picked up from the EMR instance profile automatically

print("\nLog - Initializing processing.")

# Create S3 resource to access the bucket
s3_resource = boto3.resource("s3")
bucket = s3_resource.Bucket(BUCKET_NAME)

# Write log
write_log("Log - Bucket found.", bucket)

# Write log
write_log("Log - Initializing Apache Spark.", bucket)

# Create Spark session and log errors
try:
    spark = SparkSession.builder.appName("terraform-aws-emr-pyspark").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
except Exception:
    write_log("Log - Spark initialization failed.", bucket)
    write_log(traceback.format_exc(), bucket)
    raise

# Write log
write_log("Log - Spark initialized.", bucket)

# Determine execution environment (local vs EMR)
is_emr = False if os.path.isdir("data/") else True

# Data cleaning and transformation block
try:
    HTFfeaturizedData, TFIDFfeaturizedData, W2VfeaturizedData = (
        clean_transform_data(spark, bucket, BUCKET_NAME, is_emr)
    )
except Exception:
    write_log("Log - Data cleaning and transformation failed.", bucket)
    write_log(traceback.format_exc(), bucket)
    spark.stop()
    raise

# Machine learning model training block
try:
    train_ml_models(
        spark,
        HTFfeaturizedData,
        TFIDFfeaturizedData,
        W2VfeaturizedData,
        bucket,
        BUCKET_NAME,
        is_emr,
    )
except Exception:
    write_log("Log - ML model training failed.", bucket)
    write_log(traceback.format_exc(), bucket)
    spark.stop()
    raise

# Write log
write_log("Log - Models created and saved to S3.", bucket)

# Write log
write_log("Log - Processing completed successfully.", bucket)

# Stop Spark session
spark.stop()
