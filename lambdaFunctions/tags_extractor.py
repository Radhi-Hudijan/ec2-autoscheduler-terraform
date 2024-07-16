import json

def lambda_handler(event, context):
    # Extract data from the event
    # TODO: Add your code here
    
    # Process the data
    # TODO: Add your code here
    
    # Return a response
    response = {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    return response