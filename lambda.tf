# lambda functions

# Create a zip file for the lambda function
data "archive_file" "tags_extractor_lambda" {
  type        = "zip"
  source_file = "${path.module}/lambdaFunctions/tags_extractor.py"
  output_path = "${path.module}/lambdaFunctions/tags_extractor.zip"
}

# Create an S3 bucket for the lambda function
resource "aws_s3_object" "tag_lambda_bucket" {
  bucket = aws_s3_bucket.lambda_deployment_bucket.bucket
  key    = "tags_extractor.zip"
  source = data.archive_file.tags_extractor_lambda.output_path
}

# Create a lambda function
resource "aws_lambda_function" "tags_extractor" {
  function_name = "tags_extractor"
  s3_bucket     = aws_s3_bucket.lambda_deployment_bucket.bucket
  s3_key        = aws_s3_object.tag_lambda_bucket.key
  role          = aws_iam_role.lambda_exec.arn
  handler       = "tags_extractor.lambda_handler"
  runtime       = "python3.7"
  timeout       = 30
  memory_size   = 128
}

# Create a log group for the lambda function
resource "aws_cloudwatch_log_group" "tags_extractor" {
  name              = "/aws/lambda/tags_extractor"
  retention_in_days = 7

}


#create a policy document for the lambda function
data "aws_iam_policy_document" "assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# Create a role for the lambda function
resource "aws_iam_role" "lambda_exec" {
  name               = "lambda_exec"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}


# Create an IAM Policy for Lambda to access EC2, DynamoDB, and CloudWatch Logs
data "aws_iam_policy_document" "lambda_policy" {
  statement {
    actions = [
      "ec2:DescribeTags",
      "ec2:DescribeInstances",
      "ec2:StartInstances",
      "ec2:StopInstances"
    ]
    resources = ["*"]
  }

  statement {
    actions = [
      "dynamodb:PutItem",
      "dynamodb:GetItem",
      "dynamodb:UpdateItem",
      "dynamodb:Scan",
      "dynamodb:Query"
    ]
    resources = ["arn:aws:dynamodb:${var.region}:${var.account_id}:table/ec2_instance_tags"]
  }

  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["*"]
  }
}

# Create the IAM policy
resource "aws_iam_policy" "lambda_exec" {
  name   = "lambda_exec_policy"
  policy = data.aws_iam_policy_document.lambda_policy.json
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "lambda_exec" {
  policy_arn = aws_iam_policy.lambda_exec.arn
  role       = aws_iam_role.lambda_exec.name
}


# create the Time Triggered Lambda

# Create a zip file for the lambda function
data "archive_file" "time_triggered_lambda" {
  type        = "zip"
  source_file = "${path.module}/lambdaFunctions/scheduled_lambd_function.py"
  output_path = "${path.module}/lambdaFunctions/scheduled_lambd_function.zip"
}

# Create an S3 bucket for the lambda function
resource "aws_s3_object" "time_triggered_lambda_bucket" {
  bucket = aws_s3_bucket.lambda_deployment_bucket.bucket
  key    = "scheduled_lambd_function.zip"
  source = data.archive_file.time_triggered_lambda.output_path
}

# Create a lambda function
resource "aws_lambda_function" "time_triggered_lambda" {
  function_name = "scheduled_lambda"
  s3_bucket     = aws_s3_bucket.lambda_deployment_bucket.bucket
  s3_key        = aws_s3_object.time_triggered_lambda_bucket.key
  role          = aws_iam_role.lambda_exec.arn
  handler       = "scheduled_lambd_function.lambda_handler"
  runtime       = "python3.7"
  timeout       = 30
  memory_size   = 128
}

# Create a log group for the lambda function
resource "aws_cloudwatch_log_group" "time_triggered_lambda" {
  name              = "/aws/lambda/scheduled_lambda"
  retention_in_days = 7

}
