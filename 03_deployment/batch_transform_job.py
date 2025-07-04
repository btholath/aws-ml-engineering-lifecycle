# File: 03_model_inference/batch_transform_job.py

import os
import time
import boto3
import logging
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Config from .env
region = os.getenv("AWS_REGION", "us-east-1")
bucket = os.getenv("S3_BUCKET")
role_arn = os.getenv("SAGEMAKER_ROLE_ARN")

# Input/Output paths
transform_input_key = os.getenv("XGB_FIXED_S3_KEY")  # same as used for training
transform_output_key = "batch-output/"

# Model name - must match the deployed or trained model
model_name = f"xgb-loan-model-batch-{int(time.time())}"
model_name = "xgb-loan-model-1751672068"
transform_job_name = f"xgb-loan-batch-transform-{int(time.time())}"

# Initialize SageMaker client
sagemaker = boto3.client("sagemaker", region_name=region)

# Construct S3 URIs
transform_input_s3 = f"s3://{bucket}/{transform_input_key}"
transform_output_s3 = f"s3://{bucket}/{transform_output_key}"

# Submit batch transform job
try:
    sagemaker.create_transform_job(
        TransformJobName=transform_job_name,
        ModelName=model_name,  # You must create or point to an existing model
        TransformInput={
            "DataSource": {
                "S3DataSource": {
                    "S3DataType": "S3Prefix",
                    "S3Uri": transform_input_s3
                }
            },
            "ContentType": "text/csv",
            "SplitType": "Line"
        },
        TransformOutput={
            "S3OutputPath": transform_output_s3
        },
        TransformResources={
            "InstanceType": "ml.m5.large",
            "InstanceCount": 1
        }
    )

    logging.info(f"✅ Batch transform job started: {transform_job_name}")
    logging.info(f"📤 Input: {transform_input_s3}")
    logging.info(f"📁 Output will be saved to: {transform_output_s3}")

except Exception as e:
    logging.error(f"❌ Failed to start batch transform: {e}")
