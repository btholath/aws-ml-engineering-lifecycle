# File: 01_data_preparation/data_wrangler/upload_data_wrangler_flow.py

import os
import logging
import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, ClientError

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Load configs from .env
S3_BUCKET = os.getenv("S3_BUCKET")
S3_FLOW_PREFIX = os.getenv("S3_FLOW_PREFIX", "data-wrangler/flows")
FLOW_NAME = os.getenv("FLOW_NAME", "customer_sales_cleaning")
FLOW_OUTPUT_DIR = os.getenv("FLOW_OUTPUT_DIR", "01_data_preparation/data_wrangler")
FLOW_FILE_PATH = os.path.join(FLOW_OUTPUT_DIR, f"{FLOW_NAME}.flow")

if not S3_BUCKET or not os.path.exists(FLOW_FILE_PATH):
    logging.error("Missing S3_BUCKET in .env or .flow file not found.")
    exit(1)

s3_key = f"{S3_FLOW_PREFIX}/{FLOW_NAME}.flow"
s3_client = boto3.client("s3")

def upload_flow_to_s3():
    try:
        s3_client.upload_file(FLOW_FILE_PATH, S3_BUCKET, s3_key)
        logging.info(f"✅ Uploaded .flow to s3://{S3_BUCKET}/{s3_key}")
    except FileNotFoundError:
        logging.error("❌ Flow file not found.")
    except NoCredentialsError:
        logging.error("❌ AWS credentials not found.")
    except ClientError as e:
        logging.error(f"❌ Upload failed: {e}")

def guide_user_to_import():
    logging.info("\n📌 MANUAL STEP REQUIRED:")
    logging.info("1. Go to SageMaker Studio.")
    logging.info("2. Open Data Wrangler → 'Import Flow'.")
    logging.info(f"3. Select: s3://{S3_BUCKET}/{s3_key}")

if __name__ == "__main__":
    upload_flow_to_s3()
    guide_user_to_import()
