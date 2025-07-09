import os
import logging
import boto3
from dotenv import load_dotenv
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=project_root / ".env", override=True)

region = os.getenv("AWS_REGION", "us-east-1")
bucket = os.getenv("S3_BUCKET")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s3 = boto3.client("s3", region_name=region)
prefix = "monitoring/output"

logger.info("📦 Fetching latest drift metrics...")
response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

if "Contents" not in response:
    logger.warning("❌ No monitoring outputs found.")
    exit(1)

for obj in sorted(response["Contents"], key=lambda x: x["LastModified"], reverse=True)[:3]:
    logger.info(f"📄 {obj['Key']}")