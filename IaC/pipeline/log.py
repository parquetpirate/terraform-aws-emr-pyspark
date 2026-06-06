# Logging utility for EMR PySpark pipeline

import os
import pendulum


def write_log(text, bucket):
    """
    Writes a log entry to a local file and uploads it to S3.
    """

    # Determine log file path
    logs_dir = "/home/hadoop/logs"
    path = logs_dir if os.path.isdir(logs_dir) else "/home/hadoop"

    # Get current timestamp
    now = pendulum.now()

    # Format date for the log file name
    file_date = now.format("YYYYMMDD")

    # Format timestamp for the log entry
    log_timestamp = now.format("YYYY-MM-DD HH:mm:ss")

    # Build the full log file path
    log_file = f"{path}/{file_date}-log_spark.txt"

    # Initialize log text
    mode = "a" if os.path.isfile(log_file) else "w"

    # Append timestamp and message
    log_text = f"\n[{log_timestamp}] -{text}" if mode == "a" else f"[{log_timestamp}] -{text}"

    # Write to the local file
    with open(log_file, mode) as log_file_handle:
        log_file_handle.write(log_text)

    # Print to stdout
    print(text)

    # Upload to S3 bucket
    bucket.upload_file(log_file, "logs/" + file_date + "-log_spark.txt")
