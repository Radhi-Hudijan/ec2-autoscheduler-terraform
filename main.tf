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

resource "aws_s3_bucket" "auto_schedule" {
  bucket = "auto-schedule-bucket-2233433"
}