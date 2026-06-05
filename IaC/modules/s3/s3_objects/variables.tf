# Infrastructure as Code for Distributed PySpark Training on Amazon EMR
# S3 Objects Variable Definitions

variable "bucket_name" {
  type        = string
  description = "S3 bucket name"
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
