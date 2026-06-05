# IAM Module

Creates IAM roles and instance profile for Amazon EMR.

## Resources

| Resource | Purpose |
|---|---|
| `aws_iam_role` (emr_service) | Role assumed by the EMR service |
| `aws_iam_role` (emr_profile) | Role assumed by EC2 instances in the cluster |
| `aws_iam_role_policy_attachment` (x2) | Attaches AWS-managed EMR policies |
| `aws_iam_instance_profile` | Instance profile for EMR cluster nodes |

## Outputs

| Name | Description |
|---|---|
| `service_role` | EMR service role ARN |
| `instance_profile` | EC2 instance profile ARN |
