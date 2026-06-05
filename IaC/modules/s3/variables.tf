# S3 Module — Input Variables

variable "bucket_name" {
  type        = string
  description = "S3 bucket name"
}

variable "bucket_versioning" {
  type        = string
  description = "S3 bucket versioning state: Enabled or Suspended"
}

variable "pipeline_directory" {
  type        = string
  description = "Local path to PySpark scripts"
}

variable "data_directory" {
  type        = string
  description = "Local path to input datasets"
}

variable "scripts_directory" {
  type        = string
  description = "Local path to bootstrap and shell scripts"
}
