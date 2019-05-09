from datetime import datetime

import boto3
from urllib.parse import unquote_plus
import pandas as pd
import numpy

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    download_path = '/tmp/copy.csv'

    s3.download_file(bucket, key, download_path)
    # s3.upload_file(download_path, bucket, 'hawkeye/asx_copy2.csv')

    df = pd.read_csv(download_path, skiprows=1)
    company_table = dynamodb.Table('company')

    for i in range(len(df)):
        name = df.iloc[i]['Company name']
        code = df.iloc[i]['ASX code']
        industry = df.iloc[i]['GICS industry group']

        company_table.put_item(
            Item={
                'code': code,
                'name': name,
                'industry': industry,
                'last_active': datetime.now().strftime('%Y-%m-%d'),
            })

    for i in df['GICS industry group'].unique():
        industry_table = dynamodb.Table('company')
        industry_table.put_item(
            Item={
                'name': i,
            })
