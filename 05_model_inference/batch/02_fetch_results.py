import os
import logging
import boto3
from dotenv import load_dotenv
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env from project root
project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=project_root / ".env", override=True)

region = os.getenv("AWS_REGION", "us-east-1")
bucket = os.getenv("S3_BUCKET")
prefix = os.getenv("XGB_BATCH_OUTPUT")

if not prefix:
    raise ValueError("❌ Environment variable XGB_BATCH_OUTPUT is not set in .env")

# Extract path inside bucket
prefix_path = prefix.replace(f"s3://{bucket}/", "")
logger.info(f"📥 Fetching batch results from: s3://{bucket}/{prefix_path}")

# Initialize S3 client
s3 = boto3.client("s3", region_name=region)

# List and download files
response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix_path)
if "Contents" not in response:
    raise FileNotFoundError("❌ No batch output files found in S3.")

download_dir = project_root / "05_model_inference" / "batch" / "results"
download_dir.mkdir(parents=True, exist_ok=True)

for obj in response["Contents"]:
    key = obj["Key"]
    filename = os.path.basename(key)
    output_file = download_dir / filename

    logger.info(f"⬇️ Downloading: {key} → {output_file}")
    s3.download_file(bucket, key, str(output_file))

logger.info(f"✅ Batch results downloaded to: {download_dir}")
