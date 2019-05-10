import boto3
import settings

BATCH_LIMIT = 25

dynamodb = boto3.resource('dynamodb',
                          region_name=settings.AWS_REGION,
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

s3 = boto3.client('s3',
                  region_name=settings.AWS_REGION,
                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)


def dynamodb_batch_push(table, items):
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
