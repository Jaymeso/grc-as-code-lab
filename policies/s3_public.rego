package security

deny contains msg if {
  input.resource_type == "aws_s3_bucket"
  input.acl == "public-read"
  msg := "Public S3 buckets are not allowed"
}
