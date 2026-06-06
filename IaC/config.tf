# Infrastructure as Code for Distributed PySpark Training on Amazon EMR

# Terraform version
terraform {
  required_version = "~> 1.15"

  # Provider AWS
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  # Remote state backend
  backend "s3" {
    encrypt = true
    bucket  = "terraform-aws-emr-pyspark-463032375612"
    key     = "terraform-aws-emr-pyspark.tfstate"
    region  = "us-east-2"
  }
}

# Provider Region
provider "aws" {
  region = "us-east-2"
}
