# Pipeline Scripts

PySpark scripts executed on the EMR cluster for sentiment analysis on movie reviews.

## Scripts

| File | Purpose |
|---|---|
| `terraform_aws_emr_pyspark.py` | **Main entry point** — orchestrates data processing and ML training |
| `processing.py` | Data cleaning, tokenization, feature extraction (HashingTF, TF-IDF, Word2Vec) |
| `ml.py` | Logistic Regression model training with cross-validation and accuracy evaluation |
| `log.py` | Timestamped logging to local filesystem and S3 |
| `upload_s3.py` | Upload processed DataFrames (Parquet) and trained ML models to S3 |

## Pipeline Overview

1. **Ingestion:** Load `dataset.csv` (50K movie reviews) from S3
2. **Cleaning:** Drop null values, log class balance
3. **Feature engineering:** Text cleaning → tokenization → stop word removal → HashingTF / TF-IDF / Word2Vec
4. **Training:** Logistic Regression with 2-fold cross-validation (`maxIter` ∈ {10, 15, 20})
5. **Output:** Trained models and accuracy results saved to `s3://<bucket>/output/`

## Configuration

| Variable | Source | Description |
|----------|--------|-------------|
| `S3_BUCKET_NAME` | EMR `spark-env` configuration | S3 bucket name injected at cluster creation |
| AWS credentials | EC2 instance profile | Picked up automatically by boto3 via the credential chain |

## Execution Environment Detection

The pipeline detects whether it is running on EMR by checking for the presence of a local `data/` directory. On EMR, data is read from and written to S3. Locally, filesystem paths are used.
