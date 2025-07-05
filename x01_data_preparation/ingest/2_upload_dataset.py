# File: 01_data_preparation/ingest/2_upload_dataset.py

import boto3
import os
import logging
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, ClientError

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Configuration from .env
bucket_name = os.getenv("S3_BUCKET")
raw_file = os.getenv("RAW_CSV_PATH")
clean_file = os.getenv("CLEAN_CSV_PATH")
s3_raw_key = os.getenv("S3_RAW_KEY")
s3_clean_key = os.getenv("S3_CLEAN_KEY")

s3 = boto3.client("s3")

def upload_file(local_path, s3_key):
    if not os.path.exists(local_path):
        logging.error(f"❌ File does not exist: {local_path}")
        return
    try:
        s3.upload_file(local_path, bucket_name, s3_key)
        logging.info(f"✅ Uploaded {local_path} to s3://{bucket_name}/{s3_key}")
    except NoCredentialsError:
        logging.error("❌ AWS credentials not found.")
    except ClientError as e:
        logging.error(f"❌ Failed to upload: {e}")

if __name__ == "__main__":
    logging.info("📤 Uploading raw dataset...")
    upload_file(raw_file, s3_raw_key)

    logging.info("📤 Uploading cleaned dataset...")
    upload_file(clean_file, s3_clean_key)
