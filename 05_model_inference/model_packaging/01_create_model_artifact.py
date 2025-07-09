import os
import logging
import boto3
from pathlib import Path
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load project-level .env
project_root = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=project_root / ".env", override=True)

model_artifact_s3 = os.getenv("MODEL_ARTIFACT")
if not model_artifact_s3:
    raise ValueError("❌ MODEL_ARTIFACT not set in .env")

# Parse S3 path
if not model_artifact_s3.startswith("s3://"):
    raise ValueError(f"❌ Invalid S3 URI: {model_artifact_s3}")

bucket, key = model_artifact_s3.replace("s3://", "").split("/", 1)

# Prepare local path
local_model_dir = project_root / "03_model_training/model"
local_model_dir.mkdir(parents=True, exist_ok=True)
local_model_path = local_model_dir / "xgboost-model"

# Download using boto3
logger.info(f"📥 Downloading model from: {model_artifact_s3}")
boto3.client("s3").download_file(bucket, key, str(local_model_path))
logger.info(f"✅ Model saved to: {local_model_path}")
