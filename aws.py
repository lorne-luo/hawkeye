import boto3
import settings


dynamodb = boto3.resource('dynamodb',
                          region_name=settings.AWS_REGION,
                          aws_access_key_id=settings.AWS_ACCESS_ID,
                          aws_secret_access_key=settings.AWS_ACCESS_KEY)
