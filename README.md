# Terraform AWS EMR PySpark

Infrastructure as Code for provisioning an Amazon EMR cluster to run distributed PySpark workloads.

## Architecture

- **S3** — Data lake, scripts, and pipeline storage
- **IAM** — Instance profiles and service roles for EMR
- **EMR** — Managed Spark cluster for PySpark training jobs

## Prerequisites

- [Terraform ~> 1.15](https://developer.hashicorp.com/terraform/downloads)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- AWS credentials configured (`aws configure`)

## Quick Start

```bash
# Build the Docker image (optional)
docker build -t terraform-image:emr-pyspark .

# Start the container with the IaC folder mounted
docker run -dit --name emr-pyspark -v ./IaC:/iac terraform-image:emr-pyspark /bin/bash

# Or run Terraform directly on your machine
cd IaC
cp terraform.tfvars.example terraform.tfvars   # edit with your values
terraform init
terraform plan
terraform apply
```

## Project Structure

```
.
├── Dockerfile                  # Docker image with Terraform & AWS CLI
├── IaC/
│   ├── config.tf               # Terraform backend & provider config
│   ├── main.tf                 # Root module — S3, IAM, EMR
│   ├── variables.tf            # Input variable declarations
│   ├── terraform.tfvars.example # Example environment config
│   └── modules/                # Child modules (s3, iam, emr)
└── README.md
```
