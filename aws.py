import boto3
import settings

dynamodb = boto3.resource('dynamodb',
                        region_name=settings.AWS_REGION,
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

s3 = boto3.client('s3',
                  region_name=settings.AWS_REGION,
                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
