# S3 Module

Creates and configures an S3 bucket serving as the data lake for the PySpark EMR pipeline.

## Resources

| Resource | Purpose |
|---|---|
| `aws_s3_bucket` | Main storage bucket with globally unique name |
| `aws_s3_bucket_versioning` | Object versioning enabled for data protection |
| `aws_s3_bucket_public_access_block` | Blocks all public access (ACLs, policies, cross-account) |
| `aws_s3_bucket_server_side_encryption_configuration` | SSE-AES256 encryption applied to all objects by default |
| `aws_s3_object` (pipeline scripts) | Uploads `pipeline/*.py` to `s3://<bucket>/pipeline/` |
| `aws_s3_object` (raw data) | Uploads `data/dataset.csv` to `s3://<bucket>/data/` |
| `aws_s3_object` (bootstrap scripts) | Uploads `scripts/bootstrap.sh` to `s3://<bucket>/scripts/` |
| `aws_s3_object` (folder markers) | Creates `logs/`, `output/`, `data/` placeholder objects |

## Inputs

| Name | Type | Description |
|---|---|---|
| `bucket_name` | `string` | S3 bucket name (must be globally unique) |
| `bucket_versioning` | `string` | `Enabled` or `Suspended` |
| `pipeline_directory` | `string` | Local path to PySpark scripts |
| `data_directory` | `string` | Local path to input datasets |
| `scripts_directory` | `string` | Local path to bootstrap and shell scripts |

## Outputs

This module currently does not export outputs. Bucket references in other modules use the `bucket_name` variable directly.
