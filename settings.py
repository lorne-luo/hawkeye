import os

AWS_REGION = "ap-southeast-2"  # The AWS region where your Kinesis Analytics application isconfigured.
AWS_ACCESS_KEY_ID = "AKIAJNODSIX65K7WJ6XA"  # Your AWS Access Key ID
AWS_SECRET_ACCESS_KEY = "+HPJhnAs0axrH//YzrELDdPlHu1Jpk3zZP4RfKPy"

ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')

try:
    from local import *
except ImportError:
    pass
