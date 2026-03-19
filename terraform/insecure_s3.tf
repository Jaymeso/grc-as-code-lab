resource "aws_s3_bucket" "bad_bucket" {
  bucket = "grc-test-public-bucket"
acl = "public-read"
}
