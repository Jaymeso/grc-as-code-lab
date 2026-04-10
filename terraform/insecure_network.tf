resource "aws_security_group" "public_ssh" {
  name        = "public-ssh-sg"
  description = "Security group with open SSH access"

  ingress {
    description = "Open SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
