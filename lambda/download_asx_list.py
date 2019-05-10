import boto3
import json
import urllib

s3 = boto3.client('s3')


def respond(err, res=""):
    body = res
    return {
        'statusCode': '400' if err else '200',
        'body': json.dumps({'details': str(err)}) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    '''
    download asx csv to S3
    '''
    method = event['httpMethod'].upper()
    if method not in ['POST']:
        return respond(ValueError('Unsupported method "{}"'.format(method)))

    bucket = 'lorne'
    asx_url = 'https://www.asx.com.au/asx/research/ASXListedCompanies.csv'
    local_path = '/tmp/asx.csv'
    key = 'hawkeye/asx/asx.csv'
    urllib.request.urlretrieve(asx_url, '/tmp/asx.csv')

    s3.upload_file(local_path, bucket, key)

    return respond(None, {'success': True, 'details': None})
