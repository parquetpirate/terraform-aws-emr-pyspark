# Pipeline Scripts

PySpark scripts that run on the EMR cluster for sentiment analysis ML training.

## Scripts

| File | Purpose |
|---|---|
| `terraform_aws_emr_pyspark.py` | Main entry point — orchestrates the full pipeline |
| `processing.py` | Data cleaning, tokenization, feature extraction (TF-IDF, Word2Vec) |
| `ml.py` | Logistic Regression model training and cross-validation |
| `log.py` | Local + S3 logging utility |
| `upload_s3.py` | S3 upload helpers for Parquet datasets and ML models |

## Configuration

- **Bucket name**: Set via `S3_BUCKET_NAME` environment variable
- **AWS credentials**: Picked up automatically from the EMR instance profile (no hardcoded keys)
