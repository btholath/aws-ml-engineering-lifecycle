import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import boto3

# Load env
project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=project_root / ".env", override=True)

region = os.getenv("AWS_REGION", "us-east-1")
baseline_job_name = "baseline-job-xgb"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sm = boto3.client("sagemaker", region_name=region)

baseline_input = {
    "BaselineJobName": baseline_job_name,
    "BaselineDataset": os.getenv("XGB_VALIDATION_DATA_S3"),
    "DatasetFormat": {"Csv": {"Header": True}},
    "OutputS3Uri": os.getenv("S3_BUCKET") + "/monitoring/baseline",
    "RoleArn": os.getenv("SAGEMAKER_ROLE_ARN")
}

logger.info("🚀 Starting baseline job...")
# NOTE: Replace with create_data_quality_job_definition if preferred
response = sm.create_data_quality_job_definition(**baseline_input)
logger.info(f"✅ Baseline job created: {response}")