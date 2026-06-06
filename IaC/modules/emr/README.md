# EMR Module

Provisions an Amazon EMR cluster configured for distributed PySpark machine learning workloads.

## Resources

| Resource | Purpose |
|---|---|
| `aws_emr_cluster` | EMR 7.13.0 cluster with Spark and Hadoop |
| `aws_security_group` (main) | SSH access to the master node |
| `aws_security_group` (core) | Internal communication between core nodes |

## Cluster Configuration

| Setting | Value |
|---------|-------|
| Release | `emr-7.13.0` |
| Applications | Hadoop, Spark |
| Master instance | `m5.4xlarge` (1 node) |
| Core instances | `m5.2xlarge` (2 nodes) |
| Termination protection | Disabled |
| Auto-termination | Enabled (after all steps complete) |

## Cluster Steps

| # | Name | Action | On Failure |
|---|------|--------|------------|
| 1 | Copy pipeline scripts to EC2 | `aws s3 cp s3://<bucket>/pipeline /home/hadoop/pipeline/ --recursive` | Terminate cluster |
| 2 | Copy log files to EC2 | `aws s3 cp s3://<bucket>/logs /home/hadoop/logs --recursive` | Terminate cluster |
| 3 | Run PySpark job | `spark-submit /home/hadoop/pipeline/terraform_aws_emr_pyspark.py` | Continue |

## Spark Configuration

- Python interpreter: `/home/hadoop/conda/bin/python` (Miniconda via bootstrap)
- Dynamic allocation: enabled
- Network timeout: 800s
- Heartbeat interval: 60s
- `S3_BUCKET_NAME` environment variable injected to both driver and executors

## Security Groups

| Group | Inbound Rule | Outbound Rule |
|-------|-------------|---------------|
| Main (`emr-main-security-group`) | SSH port 22 from `0.0.0.0/0` | All traffic to `0.0.0.0/0` |
| Core (`emr-core-security-group`) | All traffic from self | All traffic to `0.0.0.0/0` |

## Inputs

| Name | Type | Description |
|---|---|---|
| `emr_cluster_name` | `string` | Amazon EMR cluster name |
| `bucket_name` | `string` | S3 bucket name for scripts, data, and logs |
| `instance_profile` | `string` | EC2 instance profile ARN (from IAM module) |
| `service_role` | `string` | EMR service role ARN (from IAM module) |
