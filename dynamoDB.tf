#create dynamoDB table to store ec2 instance tags

resource "aws_dynamodb_table" "ec2_instance_tags" {
  name         = var.dynamodb_table_name
  billing_mode = "PROVISIONED"
  hash_key     = "instance_id"
  range_key    = "tag_key"

  attribute {
    name = "instance_id"
    type = "S"
  }

  attribute {
    name = "tag_key"
    type = "S"
  }

  read_capacity  = 5
  write_capacity = 5

  server_side_encryption {
    enabled = true
  }

  tags = {
    Name = var.dynamodb_table_name
  }

}
