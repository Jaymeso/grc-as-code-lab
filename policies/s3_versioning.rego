package security

deny contains msg if {
  input.resource_type == "aws_s3_bucket"
  input.versioning_enabled == false
  msg := "S3 buckets must have versioning enabled"
}


