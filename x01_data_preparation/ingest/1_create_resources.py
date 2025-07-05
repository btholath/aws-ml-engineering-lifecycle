# File: 01_data_preparation/ingest/1_create_resources.py

import boto3
import uuid
import os
import logging
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Read config from .env or use defaults
region = os.getenv("AWS_REGION", "us-east-1")
bucket_name = os.getenv("S3_BUCKET", f"btholath-sagemaker-datawrangler-demo")
domain_name = os.getenv("SAGEMAKER_DOMAIN", "studio-domain-demo")

# Initialize AWS clients
s3 = boto3.client("s3", region_name=region)
sagemaker = boto3.client("sagemaker", region_name=region)

def create_s3_bucket():
    try:
        if region == "us-east-1":
            response = s3.create_bucket(Bucket=bucket_name)
        else:
            response = s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
        logging.info(f"✅ Created S3 bucket: {bucket_name}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            logging.warning(f"⚠️ Bucket already exists and is owned by you: {bucket_name}")
        elif e.response["Error"]["Code"] == "BucketAlreadyExists":
            logging.warning(f"⚠️ Bucket already exists (global namespace): {bucket_name}")
        else:
            logging.error(f"❌ Bucket creation failed: {e}")

def list_studio_domains():
    try:
        domains = sagemaker.list_domains().get("Domains", [])
        if not domains:
            logging.warning("❗ No SageMaker Studio domains found.")
        for d in domains:
            logging.info(f"🧠 Found SageMaker Studio Domain: {d['DomainName']}")
        return domains
    except Exception as e:
        logging.error(f"❌ Failed to list Studio domains: {e}")
        return []

if __name__ == "__main__":
    create_s3_bucket()
    list_studio_domains()
