#!/usr/bin/env bash

cat $1 > lambda_function.py
zip -ur lambda.zip lambda_function.py
rm -rf lambda_function.py
aws s3 cp lambda.zip s3://lorne/lambda/lambda.zip
echo 'https://s3-ap-southeast-2.amazonaws.com/lorne/lambda/lambda.zip'