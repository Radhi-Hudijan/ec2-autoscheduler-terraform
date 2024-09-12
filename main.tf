terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }

  required_version = ">= 0.13"
}

#creating a new s3 buckt 
resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "lambda-bucket-223344"
}

# Create a lambda function bucket
resource "aws_s3_bucket" "lambda_deployment_bucket" {
  bucket = "lambda-bucket-${var.environment}"
}
