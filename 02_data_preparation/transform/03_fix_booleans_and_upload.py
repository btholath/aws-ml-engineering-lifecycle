"""
create s3 bucket
aws s3 mb s3://btholath-sagemaker-datawrangler-demo --region us-east-1

Script: 03_fix_booleans_and_upload.py
Purpose: Convert TRUE/FALSE to 1/0 for LoanApproved → label and upload to S3 for training
"""

import os
import logging
import boto3
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Config
region = os.getenv("AWS_REGION", "us-east-1")
bucket = os.getenv("S3_BUCKET")
local_input = "01_data/processed/sample_realistic_loan_approval_dataset_encoded.csv"
local_output = "01_data/processed/sample_realistic_loan_approval_dataset_ready.csv"
s3_key = "data/sample_realistic_loan_approval_dataset_ready.csv"

# Ensure directory exists
os.makedirs(os.path.dirname(local_output), exist_ok=True)

try:
    # Load encoded dataset
    df = pd.read_csv(local_input)
    logging.info(f"📥 Loaded encoded dataset: {local_input}")

    # Fix target column
    if 'LoanApproved' in df.columns:
        df['label'] = df['LoanApproved'].astype(str).str.upper().map({'TRUE': 1, 'FALSE': 0})
        df.drop(columns=['LoanApproved'], inplace=True)
        logging.info("✅ Converted 'LoanApproved' → 'label' [1/0]")
    elif 'label' not in df.columns:
        logging.warning("⚠️ No 'LoanApproved' or 'label' column found")

    # Save to local final file
    df.to_csv(local_output, index=False)
    logging.info(f"📤 Final dataset saved: {local_output}")

    # Upload to S3
    s3 = boto3.client("s3", region_name=region)
    s3.upload_file(local_output, bucket, s3_key)
    logging.info(f"✅ Uploaded to S3: s3://{bucket}/{s3_key}")

except Exception as e:
    logging.error(f"❌ Failed to fix booleans and upload: {e}")