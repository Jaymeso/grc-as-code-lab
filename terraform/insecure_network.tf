resource "aws_security_group" "public_ssh" {
  name        = "public-ssh-sg"
  description = "Security group with restricted SSH access"

  ingress {
    description = "Restricted SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/24"]
  }
}
