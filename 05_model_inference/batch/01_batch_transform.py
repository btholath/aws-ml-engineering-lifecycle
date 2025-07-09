import os
import time
import logging
import boto3
from dotenv import load_dotenv
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env from project root
project_root = Path(__file__).resolve().parent.parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

region = os.getenv("AWS_REGION", "us-east-1")
model_name = os.getenv("XGB_BATCH_MODEL_NAME", "sagemaker-xgb-endpoint-model")
s3_input = os.getenv("XGB_VALIDATION_S3_INPUT", "s3://btholath-sagemaker-datawrangler-demo/data/sample_realistic_loan_approval_dataset_ready.csv")
s3_output = os.getenv("XGB_BATCH_OUTPUT_PREFIX", "s3://btholath-sagemaker-datawrangler-demo/batch/output/")
instance_type = os.getenv("BATCH_INSTANCE_TYPE", "ml.m5.large")

sm = boto3.client("sagemaker", region_name=region)

job_name = f"batch-transform-{int(time.time())}"

logger.info(f"🚀 Starting batch transform job: {job_name}")
sm.create_transform_job(
    TransformJobName=job_name,
    ModelName=model_name,
    TransformInput={
        "DataSource": {
            "S3DataSource": {
                "S3DataType": "S3Prefix",
                "S3Uri": s3_input
            }
        },
        "ContentType": "text/csv",
        "SplitType": "Line"
    },
    TransformOutput={
        "S3OutputPath": s3_output
    },
    TransformResources={
        "InstanceType": instance_type,
        "InstanceCount": 1
    }
)

logger.info(f"✅ Batch transform job submitted: {job_name}")

# Add this after job submission in 01_batch_transform.py
logger.info("⏳ Waiting for batch transform job to complete...")
waiter = sm.get_waiter("transform_job_completed_or_stopped")
waiter.wait(TransformJobName=job_name)
logger.info(f"✅ Batch transform job completed: {job_name}")
