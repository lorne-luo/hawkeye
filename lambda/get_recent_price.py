from __future__ import print_function

import os
import base64
import csv
import json
import boto3
from alpha_vantage.timeseries import TimeSeries


s3 = boto3.client('s3')
bucket = 'lorne'
ts = TimeSeries(key=os.environ.get('ALPHA_VANTAGE_API_KEY'), output_format='csv', indexing_type='date', retries=3)


def download_price(code):
    print(f'download price for {code}')
    tmp_file = f'/tmp/{code}.csv'
    key = f'hawkeye/recent_price/{code}.csv'
    price, meta_data = ts.get_daily_adjusted(symbol=f'{code}.AUS')

    with open(tmp_file, mode='w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in price:
            writer.writerow(i)

    s3.upload_file(tmp_file, bucket, key)


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    result=[]
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['kinesis']['data'])
        payload = payload.decode('utf-8')
        print(payload)
        data = json.loads(payload)
        code = data.get('code')

        if code:
            download_price(code)
        result.append(code)
    return result  # 'Successfully processed {} records.'.format(len(event['Records']))

