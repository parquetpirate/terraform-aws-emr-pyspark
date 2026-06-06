# S3 upload utilities for EMR PySpark pipeline

import os
import os.path
from log import write_log


def upload_processed_data(df, path, s3_path, bucket, is_emr):
    """
    Uploads a DataFrame in Parquet format to an S3 bucket.
    """

    if is_emr:
        if len(list(bucket.objects.filter(Prefix=(s3_path)).limit(1))) > 0:
            df.write.mode("Overwrite").partitionBy("label").parquet(path)
        else:
            df.write.partitionBy("label").parquet(path)
    else:
        write_log("Log - This script runs only on an EMR cluster.", bucket)


def upload_ml_models(model, path, s3_path, bucket, is_emr):
    """
    Uploads a trained ML model to an S3 bucket.
    """

    if is_emr:
        if len(list(bucket.objects.filter(Prefix=(s3_path)).limit(1))) > 0:
            model.write().overwrite().save(path)
        else:
            model.save(path)
    else:
        write_log("Log - This script runs only on an EMR cluster.", bucket)
