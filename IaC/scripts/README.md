# Bootstrap Scripts

Shell scripts executed during EMR cluster provisioning as bootstrap actions.

## Scripts

| File | Purpose |
|---|---|
| `bootstrap.sh` | Installs Miniconda, Python packages, and creates working directories |

## What `bootstrap.sh` Does

1. Downloads and installs Miniconda to `$HOME/conda`
2. Adds conda to `PATH` in `.bashrc`
3. Installs Python packages via pip:
   - `findspark` — Spark integration
   - `boto3` — AWS SDK for S3 access
   - `numpy` — Numerical computing
   - `pendulum` — Datetime handling
   - `python-dotenv` — Environment variable management
   - `scikit-learn` — Machine learning utilities
4. Creates working directories: `$HOME/pipeline/`, `$HOME/logs/`

## Execution

This script runs as an EMR bootstrap action on every cluster node before Spark services start. It is referenced in the EMR module's `aws_emr_cluster` resource at `s3://<bucket>/scripts/bootstrap.sh`.
