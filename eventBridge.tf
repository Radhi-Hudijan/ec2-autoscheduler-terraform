# create EventBridge rule to trigger the lambda functions

#Rule to listen to tag changes and trigger the tags_extractor lambda function
resource "aws_cloudwatch_event_rule" "tag_change_rule" {
  name        = "tag_change_rule"
  description = "Rule to listen to tag changes and trigger the tags_extractor lambda function"
  event_pattern = jsondecode(
    {

      "source" : ["aws.ec2"],
      "detail-type" : ["AWS API Call via CloudTrail"],
      "detail" : {
        "eventSource" : ["ec2.amazonaws.com"],
        "eventName" : ["CreateTags", "ModifyTags"]
      }

    }
  )
}

# Create a target for the EventBridge rule
resource "aws_cloudwatch_event_target" "tag_change_target" {
  rule      = aws_cloudwatch_event_rule.tag_change_rule.name
  target_id = "tags_extractor"
  arn       = aws_lambda_function.tags_extractor.arn
}

# Add permissions to the lambda function to allow EventBridge to trigger it
resource "aws_lambda_permission" "allow_eventbridge_trigger" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.tags_extractor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.tag_change_rule.arn
}



# Create the second EventBridge rule to trigger the Time Triggered Lambda function every 2 minutes

resource "aws_cloudwatch_event_rule" "time_trigger_rule" {
  name                = "time_trigger_rule"
  description         = "Rule to trigger the Time Triggered Lambda function every 2 minutes"
  schedule_expression = "rate(2 minutes)"
}

# Create a target for the EventBridge rule
resource "aws_cloudwatch_event_target" "time_trigger_target" {
  rule      = aws_cloudwatch_event_rule.time_trigger_rule.name
  target_id = "time_triggered_lambda"
  arn       = aws_lambda_function.time_triggered_lambda.arn
}

# Add permissions to the lambda function to allow EventBridge to trigger it
resource "aws_lambda_permission" "allow_eventbridge_trigger_time" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.time_triggered_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.time_trigger_rule.arn
}

