import datetime
import json
import boto3  
import pytz

def lambda_handler(event, context):
    print("Lambda function started")  # Added debug statement

    #get the service resource
    dynamodb = boto3.resource('dynamodb')
    ec2 = boto3.client('ec2')

    table_name = 'ec2_instance_tags'
    table = dynamodb.Table(table_name)


    response = table.scan()
    items = response['Items']
    print(f"Scanned items: {items}")  # Added debug statement


    #check if the current time matches the time in the tags
    for item in items:
        instance_id=item['instance_id']
        tag_key=item['tag_key']
        tag_value=item['tag_value']
        

        try:
            #Get the instance region and timezone
            instance = ec2.describe_instances(InstanceIds=[instance_id])
            region = instance['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone'][:-1]
            
            timezone = pytz.timezone(get_timezone(region))
            print(f"timezon is :{timezone}")
            
            # Get the current time in the instance's region
            current_time = datetime.datetime.now(timezone)
            current_time_str = current_time.strftime("%H:%M")
            print(f"Current time in region {region} =", current_time_str)


            # convert the tag value to datetime object
            tag_time = datetime.datetime.strptime(tag_value, '%H:%M')
            
            # convert the tag time to timezone-aware datetime object
            tag_time = timezone.localize(tag_time.replace(year=current_time.year, month=current_time.month, day=current_time.day))
            print(f"{tag_key} time of instance {instance_id}: {tag_time}")

            #check if the tag time has passed
            if current_time >= tag_time:
                
                #get the instance state
                state = instance['Reservations'][0]['Instances'][0]['State']['Name']
                print(f"Current Instance state: {state}")

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

def get_timezone(region):
    # A mapping of AWS regions to their respective timezones
    region_timezones = {
        'us-east-1': 'US/Eastern',
        'us-east-2': 'US/Eastern',
        'us-west-1': 'US/Pacific',
        'us-west-2': 'US/Pacific',
        'eu-west-1': 'Europe/Dublin',
        'eu-central-1': 'Europe/Berlin',
        'eu-west-2': 'Europe/London',
        'eu-west-3': 'Europe/Paris',
        'eu-north-1': 'Europe/Helsinki',
    }
    return region_timezones.get(region, 'UTC')
