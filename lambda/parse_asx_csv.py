import boto3
import csv
from urllib.parse import unquote_plus

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    download_path = '/tmp/copy.csv'

    if key != 'hawkeye/asx.csv':
        return 'SKIP'

    s3.download_file(bucket, key, download_path)
    # s3.upload_file(download_path, bucket, 'hawkeye/asx_copy.csv')

    industry_table = dynamodb.Table('industry')
    company_table = dynamodb.Table('company')
    industry_set = set()

    with open(download_path) as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        headers = next(reader)
        for row in reader:
            name = row[0]
            code = row[1]
            industry = row[2]
            industry_set.add(industry)

            # company_table.put_item(
            #     Item={
            #         'code': code,
            #         'name': name,
            #         'industry': industry,
            #         'last_active': datetime.now().strftime('%Y-%m-%d'),
            #     })
        for i in industry_set:
            industry_table.put_item(
                Item={
                    'name': i,
                })
        return 'DONE'
