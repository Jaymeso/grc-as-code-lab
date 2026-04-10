resource "aws_instance" "legacy_metadata_instance" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  metadata_options {
    http_tokens = "optional"
  }

  tags = {
    Name = "legacy-metadata-instance"
  }
}
