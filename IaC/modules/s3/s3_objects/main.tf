# Infrastructure as Code for Distributed PySpark Training on Amazon EMR
# S3 Work Folders

# python_scripts
resource "aws_s3_object" "python_scripts" {
  for_each = fileset("${var.pipeline_directory}/", "**")
  bucket   = var.bucket_name
  key      = "pipeline/${each.value}"
  source   = "${var.pipeline_directory}/${each.value}"
  etag     = filemd5("${var.pipeline_directory}/${each.value}")
}

# raw_data
resource "aws_s3_object" "raw_data" {
  for_each = fileset("${var.data_directory}/", "**")
  bucket   = var.bucket_name
  key      = "data/${each.value}"
  source   = "${var.data_directory}/${each.value}"
  etag     = filemd5("${var.data_directory}/${each.value}")
}

# transformed_data
resource "aws_s3_object" "transformed_data" {
  bucket = var.bucket_name
  key    = "data/"
}

# logs
resource "aws_s3_object" "logs" {
  bucket = var.bucket_name
  key    = "logs/"
}

# output
resource "aws_s3_object" "output" {
  bucket = var.bucket_name
  key    = "output/"
}

# bash_scripts
resource "aws_s3_object" "bash_scripts" {
  for_each = fileset("${var.scripts_directory}/", "**")
  bucket   = var.bucket_name
  key      = "scripts/${each.value}"
  source   = "${var.scripts_directory}/${each.value}"
  etag     = filemd5("${var.scripts_directory}/${each.value}")
}
