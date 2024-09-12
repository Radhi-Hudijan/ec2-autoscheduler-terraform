import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    ec2 = boto3.client('ec2')
    table_name = 'ec2_instance_tags'

    instance_id = event['detail']['requestParameters']['resourcesSet']['items'][0]['resourceId']
    tags = event['detail']['requestParameters']['tagSet']['items']
    print(f"Tags from event: {tags}")

    try:
        table = dynamodb.Table(table_name)
    
        #get all the instance tags
        instance_tags = ec2.describe_tags(
            Filters=[
                {
                    'Name': 'resource-id',
                    'Values': [instance_id]
                }
            ]
        )
        print(f"Instance tags: {instance_tags}")
        auto_shutdown = False

        # Check if 'auto:shutdown' exists and is set to true
        for tag in instance_tags['Tags']:
            if tag['Key'] == 'auto:shutdown' and tag['Value'].lower() == 'true':
                auto_shutdown = True

        
            for tag in tags:
                if tag['key'] in ['auto:stop', 'auto:start']:
                    # check if the tag is already present in the table
                    response = table.get_item(
                        Key={
                            'instance_id': instance_id,
                            'tag_key': tag['key']
                            }
                        )
                    if 'Item' in response:
                        # update the tag value
                        table.update_item(
                            Key={
                                'instance_id': instance_id,
                                'tag_key': tag['key'],
                            },
                            UpdateExpression='SET tag_value = :val, auto_shutdown = :auto_shutdown',
                            ExpressionAttributeValues={
                                ':val': tag['value'],
                                ':auto_shutdown': auto_shutdown
                            }
                        )
                    else:
                        # add the tag to the table  
                        table.put_item(
                            Item={
                                'instance_id': instance_id,
                                'tag_key': tag['key'],
                                'tag_value': tag['value'],
                                'auto_shutdown': auto_shutdown
                            }
                        )
      

                
    except Exception as e:
        print(f'Error: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
