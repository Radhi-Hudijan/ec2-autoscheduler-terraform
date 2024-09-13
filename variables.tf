variable "region" {
  description = "The region in which the resources will be created."
  default     = "eu-west-1"

}

variable "environment" {
  description = "The environment in which the resources will be created."
  default     = "dev"
}

variable "account_id" {
  description = "The account ID in which the resources will be created."
  default     = "533267081597"
}

variable "dynamodb_table_name" {
  description = "The name of the DynamoDB table."
  default     = "ec2_instance_tags"
}
