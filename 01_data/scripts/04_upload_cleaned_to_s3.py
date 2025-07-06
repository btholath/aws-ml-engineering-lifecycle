"""
Script: 04_upload_cleaned_to_s3.py
Purpose: Upload processed and validation loan datasets to S3
"""

import os
import logging
import boto3
from dotenv import load_dotenv

# Load environment variables from project root .env
load_dotenv(override=True)

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Load S3 config
bucket = os.getenv("S3_BUCKET")
region = os.getenv("AWS_REGION", "us-east-1")
if not bucket:
    raise ValueError("❌ S3_BUCKET is not set in .env.")

# Files to upload (local path => s3 key)
files_to_upload = {
    # Processed
    "01_data/processed/sample_realistic_loan_approval_dataset_cleaned.csv": "data/sample_realistic_loan_approval_dataset_cleaned.csv",
    "01_data/processed/sample_realistic_loan_approval_dataset_encoded.csv": "data/sample_realistic_loan_approval_dataset_encoded.csv",
    "01_data/processed/sample_realistic_loan_approval_dataset_ready.csv": "data/sample_realistic_loan_approval_dataset_ready.csv",
    "01_data/processed/sample_realistic_loan_approval_dataset_train.csv": "data/sample_realistic_loan_approval_dataset_train.csv",

    # Validation
    "01_data/validation/sample_realistic_loan_approval_dataset_ready.csv": "data/validation/sample_realistic_loan_approval_dataset_ready.csv",
    "01_data/validation/sample_realistic_loan_approval_dataset_ready_validation.csv": "data/validation/sample_realistic_loan_approval_dataset_ready_validation.csv",
    "01_data/validation/sample_realistic_loan_approval_dataset_valid.csv": "data/validation/sample_realistic_loan_approval_dataset_valid.csv",
}

# Initialize S3 client
s3 = boto3.client("s3", region_name=region)

# Upload each file
for local_file, s3_key in files_to_upload.items():
    if os.path.exists(local_file):
        try:
            s3.upload_file(local_file, bucket, s3_key)
            logging.info(f"✅ Uploaded {local_file} to s3://{bucket}/{s3_key}")
        except Exception as e:
            logging.error(f"❌ Failed to upload {local_file} to s3://{bucket}/{s3_key}: {e}")
    else:
        logging.warning(f"⚠️ File not found, skipping: {local_file}")
