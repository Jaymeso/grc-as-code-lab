resource "aws_s3_bucket" "bad_bucket" {
  bucket = "grc-test-public-bucket"
}

resource "aws_s3_bucket_logging" "bad_bucket_logging" {
  bucket        = aws_s3_bucket.bad_bucket.id
  target_bucket = aws_s3_bucket.bad_bucket.id
  target_prefix = "access-logs/bad-bucket/"
}
