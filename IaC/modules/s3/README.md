# S3 Module

Creates an S3 bucket configured for a PySpark data lake on EMR.

## Resources

| Resource | Purpose |
|---|---|
| `aws_s3_bucket` | Main bucket |
| `aws_s3_bucket_versioning` | Object versioning |
| `aws_s3_bucket_public_access_block` | Blocks all public access |
| `aws_s3_bucket_server_side_encryption_configuration` | AES256 encryption by default |
| `aws_s3_object` | Uploads pipeline scripts, datasets, and bootstrap files |

## Inputs

| Name | Type | Description |
|---|---|---|
| `bucket_name` | `string` | S3 bucket name |
| `bucket_versioning` | `string` | `Enabled` or `Suspended` |
| `pipeline_directory` | `string` | Local path to PySpark scripts |
| `data_directory` | `string` | Local path to datasets |
| `scripts_directory` | `string` | Local path to bootstrap scripts |

## Outputs

| Name | Description |
|---|---|
| `bucket_name` | S3 bucket name |
| `bucket_arn` | S3 bucket ARN |
| `bucket_id` | S3 bucket ID |
