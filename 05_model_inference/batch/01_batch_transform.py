import os
import logging
import boto3
from dotenv import load_dotenv
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
project_root = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=project_root / ".env", override=True)

sagemaker = boto3.client("sagemaker", region_name=os.getenv("AWS_REGION"))
model_name = os.getenv("XGB_REGISTERED_MODEL_NAME")
s3_input = os.getenv("XGB_VALIDATION_DATA_S3")
s3_output = os.getenv("XGB_BATCH_OUTPUT", f"s3://{os.getenv('S3_BUCKET')}/batch-transform-output")

job_name = f"batch-transform-{model_name}"
logger.info(f"🚀 Starting batch transform job: {job_name}")

response = sagemaker.create_transform_job(
    TransformJobName=job_name,
    ModelName=model_name,
    TransformInput={{
        "DataSource": {{"S3DataSource": {{"S3DataType": "S3Prefix", "S3Uri": s3_input}}}},
        "ContentType": "text/csv",
        "SplitType": "Line"
    }},
    TransformOutput={{"S3OutputPath": s3_output}},
    TransformResources={{"InstanceType": "ml.m5.large", "InstanceCount": 1}},
)

logger.info(f"✅ Batch transform job submitted: {job_name}")