# EMR Module

Provisions an Amazon EMR cluster for distributed PySpark workloads.

## Resources

| Resource | Purpose |
|---|---|
| `aws_emr_cluster` | EMR cluster with Spark and Hadoop |
| `aws_security_group` (main) | SSH access to master node |
| `aws_security_group` (core) | Internal traffic between core nodes |

## Inputs

| Name | Type | Description |
|---|---|---|
| `emr_cluster_name` | `string` | EMR cluster name |
| `bucket_name` | `string` | S3 bucket name for scripts and logs |
| `instance_profile` | `string` | EC2 instance profile ARN |
| `service_role` | `string` | EMR service role ARN |
