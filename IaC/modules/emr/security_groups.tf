# EMR Module — Security Groups

# Main node security group
resource "aws_security_group" "main_security_group" {

  name        = "emr-main-security-group"
  description = "Allow inbound traffic for EMR main node."

  revoke_rules_on_delete = true

  # Inbound SSH from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Core node security group
resource "aws_security_group" "core_security_group" {

  name        = "emr-core-security-group"
  description = "Allow inbound and outbound traffic for EMR core nodes."

  revoke_rules_on_delete = true

  # Inbound traffic within the security group
  ingress {
    from_port = "0"
    to_port   = "0"
    protocol  = "-1"
    self      = true
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
