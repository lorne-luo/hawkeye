import base64
import json
from random import random

import boto3
import config.settings.local as settings


BATCH_LIMIT = 25

dynamodb = boto3.resource('dynamodb',
                          region_name=settings.AWS_REGION,
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

s3 = boto3.client('s3',
                  region_name=settings.AWS_REGION,
                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

kinesis = boto3.client('kinesis', region_name=settings.AWS_REGION,
                       aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)


def dynamodb_batch_push(table, items):
    print(f'Push {len(items)} items to table {table}.')

    request = [{
        'PutRequest': {
            'Item': item
        }
    } for item in items]

    i = 0
    while i < len(request):
        dynamodb.batch_write_item(RequestItems={
            table: request[i:i + BATCH_LIMIT]
        })
        i += BATCH_LIMIT
        print(f'Table {table} request #{int(i/BATCH_LIMIT)}')


def kinesis_put_records(stream_name, items):
    get_partition_key = lambda x: x.get('PartitionKey') or str(random())
    records = [{'Data': bytes(json.dumps(item), 'utf-8'), 'PartitionKey': get_partition_key(item)} for item in items]
    print(base64.b64encode(bytes(json.dumps(items[0]), 'utf-8')))
    kinesis.put_records(StreamName=stream_name, Records=records)
