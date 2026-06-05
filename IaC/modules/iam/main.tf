# Infrastructure as Code for Distributed PySpark Training on Amazon EMR
# IAM Config

# IAM ROLE for EMR Service
resource "aws_iam_role" "iam_emr_service_role" {

  name = "iam_emr_service_role"

  assume_role_policy = <<-POLICY
  {
  "Version": "2012-10-17",
  "Statement": [
      {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
          "Service": "elasticmapreduce.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }
  POLICY
}

resource "aws_iam_role_policy_attachment" "emr_service" {
  role       = aws_iam_role.iam_emr_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole"
}

# IAM Role For EC2 Instance Profile
resource "aws_iam_role" "iam_emr_profile_role" {

  name = "iam_emr_profile_role"

  assume_role_policy = <<-POLICY
  {
  "Version": "2012-10-17",
  "Statement": [
      {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }
  POLICY
}

resource "aws_iam_role_policy_attachment" "emr_ec2" {
  role       = aws_iam_role.iam_emr_profile_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforEC2Role"
}

resource "aws_iam_instance_profile" "emr_profile" {
  name = "emr_profile"
  role = aws_iam_role.iam_emr_profile_role.name
}
