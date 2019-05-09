import boto3
import urllib

s3 = boto3.client('s3')


def handler(event, context):
    bucket = 'lorne'
    asx_url = 'https://www.asx.com.au/asx/research/ASXListedCompanies.csv'
    local_path = '/tmp/asx.csv'
    key = 'hawkeye/asx.csv'
    urllib.request.urlretrieve(asx_url, '/tmp/asx.csv')

    s3.upload_file(local_path, bucket, key)



'''

import boto3
import json

print('Loading function')
dynamo = boto3.client('dynamodb')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    
    #print("Received event: " + json.dumps(event, indent=2))

    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'GET': lambda dynamo, x: dynamo.scan(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
    }

    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        return respond(None, operations[operation](dynamo, payload))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))

'''