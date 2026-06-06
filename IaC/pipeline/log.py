# Logging utility for EMR PySpark pipeline

import subprocess

command = "pip install pendulum"
subprocess.run(command.split())

import os
import os.path
import pendulum
import traceback


def write_log(text, bucket):
    """
    Writes a log entry to a local file and uploads it to S3.
    """

    # Determine log file path
    path = "." if os.path.isdir("logs") else "/home/hadoop"

    # Get current timestamp
    now = pendulum.now()

    # Format date for the log file name
    file_date = now.format("YYYYMMDD")

    # Format timestamp for the log entry
    log_timestamp = now.format("YYYY-MM-DD HH:mm:ss")

    # Build the full log file path
    log_file = f"{path}/{file_date}-log_spark.txt"

    # Initialize log text
    log_text = ""

    # Open the log file (create or append)
    try:
        if os.path.isfile(log_file):
            log_file_handle = open(log_file, "a")
            log_text = log_text + "\n"
        else:
            log_file_handle = open(log_file, "w")
    except Exception:
        print("Error accessing the log file.")
        raise Exception(traceback.format_exc())

    # Append timestamp and message
    log_text = log_text + "[" + log_timestamp + "] -" + text

    # Write to the local file
    log_file_handle.write(log_text)

    # Print to stdout
    print(text)

    # Close the file
    log_file_handle.close()

    # Upload to S3 bucket
    bucket.upload_file(log_file, "logs/" + file_date + "-log_spark.txt")
