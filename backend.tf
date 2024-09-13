terraform {
  backend "s3" {
    bucket = "lambda-bucket-223344"
    key    = "terraform.tfstate"
    region = "eu-west-1"
  }
}
