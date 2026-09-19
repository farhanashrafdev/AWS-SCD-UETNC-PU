# Placeholder Terraform for the demo. Nothing here is ever applied to a
# real AWS account. This file exists only so the deterministic security
# gate (scripts/security_gate.py) has realistic infrastructure code to scan.
#
# Do NOT run `terraform init` or `terraform apply` against this file.

resource "aws_security_group" "demo_ssh" {
  name        = "demo-ssh-access"
  description = "Placeholder security group for the DevSecOps demo"

  ingress {
    description = "SSH access restricted to the demo VPC"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
