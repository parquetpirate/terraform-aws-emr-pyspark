# EMR Module — Cluster Resources

resource "aws_emr_cluster" "cluster" {

  # Cluster name
  name = var.emr_cluster_name

  # EMR release version
  release_label = "emr-7.13.0"

  # Applications
  applications = ["Hadoop", "Spark"]

  # Termination protection
  termination_protection = false

  # Keep cluster alive when no steps remain
  keep_job_flow_alive_when_no_steps = false

  # Log URI
  log_uri = "s3://${var.bucket_name}/logs/"

  # EMR service role
  service_role = var.service_role

  # EC2 instance attributes
  ec2_attributes {
    instance_profile                  = var.instance_profile
    emr_managed_master_security_group = aws_security_group.main_security_group.id
    emr_managed_slave_security_group  = aws_security_group.core_security_group.id
  }

  # Master instance type
  master_instance_group {
    instance_type = "m5.xlarge"
  }

  core_instance_group {
    instance_type  = "m5.xlarge"
    instance_count = 2
  }

  # Bootstrap action — installs Python and additional packages
  bootstrap_action {
    name = "Install Python packages"
    path = "s3://${var.bucket_name}/scripts/bootstrap.sh"
  }

  # Cluster steps
  # 1 - Copy pipeline scripts from S3 to EC2 instances. Terminate on failure.
  # 2 - Copy log files from S3 to EC2 instances. Terminate on failure.
  # 3 - Run PySpark job. Keep cluster alive on failure.

  step = [
    {
      name              = "Copy pipeline scripts to EC2"
      action_on_failure = "TERMINATE_CLUSTER"

      hadoop_jar_step = [
        {
          jar        = "command-runner.jar"
          args       = ["aws", "s3", "cp", "s3://${var.bucket_name}/pipeline", "/home/hadoop/pipeline/", "--recursive"]
          main_class = ""
          properties = {}
        }
      ]
    },
    {
      name              = "Copy log files to EC2"
      action_on_failure = "TERMINATE_CLUSTER"

      hadoop_jar_step = [
        {
          jar        = "command-runner.jar"
          args       = ["aws", "s3", "cp", "s3://${var.bucket_name}/logs", "/home/hadoop/logs", "--recursive"]
          main_class = ""
          properties = {}
        }
      ]
    },
    {
      name              = "Run PySpark job"
      action_on_failure = "CONTINUE"

      hadoop_jar_step = [
        {
          jar        = "command-runner.jar"
          args       = ["spark-submit", "/home/hadoop/pipeline/terraform_aws_emr_pyspark.py"]
          main_class = ""
          properties = {}
        }
      ]
    }
  ]

  # Spark configuration
  configurations_json = <<EOF
  [
    {
      "Classification": "spark-defaults",
        "Properties": {
        "spark.pyspark.python": "/home/hadoop/conda/bin/python",
        "spark.dynamicAllocation.enabled": "true",
        "spark.network.timeout": "800s",
        "spark.executor.heartbeatInterval": "60s"
        }
    },
    {
      "Classification": "spark-env",
        "Properties": {
        "spark.executorEnv.S3_BUCKET_NAME": "${var.bucket_name}",
        "spark.yarn.appMasterEnv.S3_BUCKET_NAME": "${var.bucket_name}"
        }
    }
  ]
  EOF
}
