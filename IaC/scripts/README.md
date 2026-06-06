# Bootstrap Scripts

Shell scripts executed during EMR cluster provisioning.

## Scripts

| File | Purpose |
|---|---|
| `bootstrap.sh` | Installs Miniconda, Python packages (boto3, numpy, scikit-learn, etc.) and creates working directories |

## Execution

This script runs as an EMR bootstrap action on every cluster node before Spark starts.
