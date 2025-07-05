"""
ploads your .flow file to a specific S3 prefix for use in Studio.

✅ Tasks Performed:
Upload .flow to s3://<bucket>/<prefix>/<FLOW_NAME>.flow
"""
# 02_upload_flow.py

import os
import logging
import boto3
from dotenv import load_dotenv

# Load .env
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

region = os.getenv("AWS_REGION")
bucket = os.getenv("S3_BUCKET")
prefix = os.getenv("S3_FLOW_PREFIX", "data-wrangler/flows/")
flow_name = os.getenv("FLOW_NAME", "data_wrangler_flow")
local_file = f"02_data_preparation/data_wrangler/{flow_name}.flow"
s3_key = f"{prefix}{flow_name}.flow"

# Upload to S3
s3 = boto3.client("s3", region_name=region)

try:
    s3.upload_file(local_file, bucket, s3_key)
    logging.info(f"✅ Flow uploaded to: s3://{bucket}/{s3_key}")
except Exception as e:
    logging.error(f"❌ Upload failed: {e}")
