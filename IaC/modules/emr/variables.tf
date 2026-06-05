# EMR Module — Input Variables

variable "emr_cluster_name" {
  type        = string
  description = "Amazon EMR cluster name"
}

variable "bucket_name" {
  type        = string
  description = "S3 bucket name for scripts and logs"
}

variable "instance_profile" {
  type        = string
  description = "EC2 instance profile ARN"
}

variable "service_role" {
  type        = string
  description = "EMR service role ARN"
}
