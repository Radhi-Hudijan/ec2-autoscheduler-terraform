import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'ec2_instance_tags'

    instance_id = event['detail']['requestParameters']['resourcesSet']['items'][0]['resourceId']
    tags = event['detail']['requestParameters']['tagSet']['items']

    try:
        table = dynamodb.Table(table_name)
        for tag in tags:
            if tag['key'] in ['auto:stop', 'auto:start']:
                table.put_item(
                    Item={
                        'instance_id': instance_id,
                        'tag_key': tag['key'],
                        'tag_value': tag['value']
                    }
                )

    except Exception as e:
        print(f'Error: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
