terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.38.0"
    }

    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4.2"
    }
  }

  required_version = "~> 1.2"
}

#creating a new s3 buckt 
resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "lambda-bucket-223344"
}

# Create a lambda function bucket
resource "aws_s3_bucket" "lambda_deployment_bucket" {
  bucket = "lambda-bucket-${var.environment}-334444433"
}
