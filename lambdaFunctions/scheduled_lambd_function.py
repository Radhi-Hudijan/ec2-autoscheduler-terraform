import datetime
import json
import boto3

def lambda_handler(event, context):
    #get the service resource
    dynamodb = boto3.resource('dynamodb')
    ec2 = boto3.client('ec2')

    table_name = 'ec2_instance_tags'
    table = dynamodb.Table(table_name)

    response = table.scan()
    items = response['Items']

    current_time = datetime.datetime.now().strftime("%H:%M")
    
    #check if the current time matches the time in the tags
    for item in items:
        if item['tag_key'] == 'auto:stop' and item['tag_value'] == current_time:
            instance_id = item['instance_id']
            ec2.stop_instances(InstanceIds=[instance_id])
            print(f"Instance {instance_id} stopped at {current_time}")
        elif item['tag_key'] == 'auto:start' and item['tag_value'] == current_time:
            instance_id = item['instance_id']
            ec2.start_instances(InstanceIds=[instance_id])
            print(f"Instance {instance_id} started at {current_time}")
