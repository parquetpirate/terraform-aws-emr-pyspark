# Infrastructure as Code for Distributed PySpark Training on Amazon EMR
# Main Script

# Storage Module
module "s3" {
  source             = "./modules/s3"
  bucket_name        = var.bucket_name
  bucket_versioning  = var.bucket_versioning
  pipeline_directory = var.pipeline_directory
  data_directory     = var.data_directory
  scripts_directory  = var.scripts_directory
}

# Security Module
module "iam" {
  source = "./modules/iam"
}

# Processing Module
module "emr" {
  source           = "./modules/emr"
  emr_cluster_name = var.emr_cluster_name
  bucket_name      = var.bucket_name
  instance_profile = module.iam.instance_profile
  service_role     = module.iam.service_role

  depends_on = [module.s3]
}
