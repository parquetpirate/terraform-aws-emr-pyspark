# IAM Module

Creates IAM roles and instance profile required by Amazon EMR.

## Resources

| Resource | Purpose |
|---|---|
| `aws_iam_role` (`iam_emr_service_role`) | Role assumed by the EMR service — attached to `AmazonElasticMapReduceRole` |
| `aws_iam_role` (`iam_emr_profile_role`) | Role assumed by EC2 instances in the cluster — attached to `AmazonElasticMapReduceforEC2Role` |
| `aws_iam_role_policy_attachment` (×2) | Attaches AWS-managed policies to the respective roles |
| `aws_iam_instance_profile` | Instance profile linking the EC2 role to EMR cluster nodes |

## Trust Relationships

| Role | Trusted Service |
|---|---|
| `iam_emr_service_role` | `elasticmapreduce.amazonaws.com` |
| `iam_emr_profile_role` | `ec2.amazonaws.com` |

## Outputs

| Name | Description |
|---|---|
| `service_role` | EMR service role ARN |
| `instance_profile` | EC2 instance profile ARN |
