# Script: 2_upload_dataset.py
# Purpose: Upload dataset to S3

import boto3

bucket_name = 'your-existing-or-created-bucket-name'
s3_key = 'data/cleaned_sample_sales_dataset.csv'
local_file = 'datasets/cleaned_sample_sales_dataset.csv'

s3 = boto3.client('s3')

def upload_dataset():
    s3.upload_file(local_file, bucket_name, s3_key)
    print(f"✅ Uploaded {local_file} to s3://{bucket_name}/{s3_key}")

if __name__ == "__main__":
    upload_dataset()
