# Script: 1_create_resources.py
# Purpose: Create S3 bucket and SageMaker Studio domain if not exists

import boto3
import uuid

region = 'us-east-1'
s3 = boto3.client('s3', region_name=region)
sagemaker = boto3.client('sagemaker', region_name=region)

bucket_name = f"sagemaker-datawrangler-demo-{uuid.uuid4().hex[:6]}"
domain_name = "studio-domain-demo"

def create_s3_bucket():
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
        print(f"✅ Created S3 bucket: {bucket_name}")
    except s3.exceptions.BucketAlreadyExists:
        print(f"⚠️ Bucket already exists: {bucket_name}")

def list_studio_domains():
    domains = sagemaker.list_domains()
    for d in domains.get('Domains', []):
        print(f"🧠 SageMaker Studio Domain found: {d['DomainName']}")
    return domains.get('Domains', [])

if __name__ == "__main__":
    create_s3_bucket()
    list_studio_domains()
