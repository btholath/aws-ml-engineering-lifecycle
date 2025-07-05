"""
Script: 04_upload_cleaned_to_s3.py
Purpose: Upload cleaned loan dataset to S3
"""

import os
import logging
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Load config
bucket = os.getenv("S3_BUCKET")
region = os.getenv("AWS_REGION", "us-east-1")
local_cleaned_csv = "01_data/processed/sample_realistic_loan_approval_dataset_cleaned.csv"
s3_key = "data/sample_realistic_loan_approval_dataset_cleaned.csv"

# Upload to S3
try:
    s3 = boto3.client("s3", region_name=region)
    s3.upload_file(local_cleaned_csv, bucket, s3_key)
    logging.info(f"✅ Uploaded {local_cleaned_csv} to s3://{bucket}/{s3_key}")
except Exception as e:
    logging.error(f"❌ Failed to upload to S3: {e}")