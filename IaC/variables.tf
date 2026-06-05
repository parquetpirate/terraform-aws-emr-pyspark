# Infrastructure as Code for Distributed PySpark Training on Amazon EMR
# Variable Definitions

variable "bucket_name" {
  type        = string
  description = "S3 bucket name"
}

variable "bucket_versioning" {
  type        = string
  description = "Specifies whether bucket versioning is enabled"
}

variable "pipeline_directory" {
  type        = string
  description = "Directory containing the PySpark scripts to be uploaded"
  default     = "./pipeline"
}

variable "data_directory" {
  type        = string
  description = "Directory containing the input datasets"
  default     = "./data"
}

variable "scripts_directory" {
  type        = string
  description = "Directory containing the bootstrap and shell scripts"
  default     = "./scripts"
}

variable "emr_cluster_name" {
  type        = string
  description = "Amazon EMR cluster name"
}
