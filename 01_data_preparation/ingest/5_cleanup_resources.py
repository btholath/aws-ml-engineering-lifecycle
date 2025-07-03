# Script: 5_cleanup_resources.py
# Purpose: Clean up S3 bucket created for the demo

import boto3

bucket_name = 'btholath-sagemaker-datawrangler-demo'
s3 = boto3.resource('s3')

def cleanup_bucket():
    bucket = s3.Bucket(bucket_name)
    print(f"🧹 Deleting contents from bucket: {bucket_name}")
    bucket.objects.all().delete()
    bucket.delete()
    print(f"✅ Deleted bucket: {bucket_name}")

if __name__ == "__main__":
    cleanup_bucket()
