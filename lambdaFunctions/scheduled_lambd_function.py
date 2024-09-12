import datetime
import json
import boto3  


def lambda_handler(event, context):
    print("Lambda function started")  # Added debug statement

    #get the service resource
    dynamodb = boto3.resource('dynamodb')
    ec2 = boto3.client('ec2')

    table_name = 'ec2_instance_tags'
    table = dynamodb.Table(table_name)
    
    try:
        #scan the table
        response = table.scan(
            FilterExpression=Attr('tag_key').ne('auto:shutdown')
        )
        items = response['Items']
       

    except Exception as e:
        print(f'Error: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps('Error scanning the table')
        }

    #check if the current time matches the time in the tags
    for item in items:
        instance_id=item['instance_id']
        tag_key=item['tag_key']
        tag_value=item['tag_value']
        auto_shutdown=item['auto_shutdown']
        
        #check if the instance is set to auto shutdown
        if auto_shutdown:
            print(f"Instance {instance_id} is set to auto shutdown")
        
            try:
                #Get the instance region and timezone
                instance = ec2.describe_instances(InstanceIds=[instance_id])
                state = instance['Reservations'][0]['Instances'][0]['State']['Name']
                print(f"Current Instance state: {state}")
    
                # Get the current time in the instance's region
                current_time = datetime.datetime.utcnow()
                current_time_str = current_time.strftime("%H:%M")
                print(f"Current time in UTC =", current_time_str)


                # convert the tag value to datetime object in UTC
                tag_time = datetime.datetime.strptime(tag_value, '%H:%M')
                tag_time = tag_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)
                

                #check if the tag time has passed
                if current_time >= tag_time:
                    
                    #stop the instance if it is running
                    if tag_key == "auto:stop":
                        if state == 'running':
                            print(f"Stopping instance: {instance_id} at {current_time_str}")
                            ec2.stop_instances(InstanceIds=[instance_id])
                        else:
                            print(f"Instance {instance_id} is already stopped at {current_time_str}") 

                    #start the instance if it is stopped
                    elif tag_key == "auto:start":
                        if state == 'stopped':
                            print(f"Starting instance: {instance_id} at {current_time_str}")
                            ec2.start_instances(InstanceIds=[instance_id])
                        else:
                            print(f"Instance {instance_id} is already running at {current_time_str}")

            except Exception as e:
                print(f"Error processing instance {instance_id}: {e}")
                return {
                    'statusCode': 500,
                    'body': json.dumps('Internal Server Error')
                }

        else:
            print(f"Instance {instance_id} is not set to auto shutdown")
