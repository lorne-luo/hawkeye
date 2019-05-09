#!/usr/bin/env bash
rm package.zip
mkdir package
pip install -r requirements.txt --target package
cat $1 > package/lambda_function.py
cd package
zip -r9 "../package.zip" .
cd ..
rm -rf package
