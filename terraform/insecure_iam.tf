resource "aws_iam_policy" "bad_policy" {
  name        = "bad-policy"
  description = "Overly permissive IAM policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "*"
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}
