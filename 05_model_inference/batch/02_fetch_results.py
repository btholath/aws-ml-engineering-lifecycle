import os
import logging
import boto3
from dotenv import load_dotenv
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

project_root = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=project_root / ".env", override=True)

s3 = boto3.client("s3")
bucket = os.getenv("S3_BUCKET")
output_prefix = os.getenv("XGB_BATCH_OUTPUT").split("/", 3)[-1]
local_path = "batch_output.csv"

logger.info("📥 Downloading batch transform results...")
s3.download_file(bucket, f"{output_prefix}/data.csv.out", local_path)
logger.info(f"✅ Batch results saved to: {local_path}")