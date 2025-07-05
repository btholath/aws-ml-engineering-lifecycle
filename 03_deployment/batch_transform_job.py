"""
Purpose of batch_transform_job.py
This script automates the Batch Inference step using Amazon SageMaker. It takes a trained model and performs predictions on a large dataset stored in Amazon S3, saving the prediction results back to S3 — without the need for deploying a real-time endpoint.

Where This Fits in the ML Lifecycle
ML Phase: ✅ Post-training → Model Inference / Model Serving

Stage	                            Description
✔️ Model trained	               Model artifacts are saved in S3
✔️ Model deployed or registered    A model is available for inference
✅ Batch Inference	              Used when real-time prediction is not required (e.g. reports, re-scoring datasets, etc.)
"""

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


# AWS and model config from .env
region = os.getenv("AWS_REGION", "us-east-1")
bucket = os.getenv("S3_BUCKET")
role_arn = os.getenv("SAGEMAKER_ROLE_ARN")
model_name = os.getenv("MODEL_NAME")  # Must be created beforehand

# # Batch transform config
# Input/Output paths
transform_input_key = os.getenv("XGB_FIXED_S3_KEY", "data/sample_loan_fixed_for_xgboost.csv")
transform_output_key = os.getenv("BATCH_OUTPUT_PREFIX", "batch-output/")

# Model name - must match the deployed or trained model
# Must match an existing SageMaker model created from training
model_name = f"xgb-loan-model-batch-{int(time.time())}"
model_name = "xgb-loan-model-1751672068"

# Generate unique transform job name
transform_job_name = f"xgb-loan-batch-transform-{int(time.time())}"

# Initialize SageMaker client
sagemaker = boto3.client("sagemaker", region_name=region)

# Construct S3 URIs
# Points to the dataset to be predicted on (.csv file in S3)
# S3 folder where SageMaker will write the prediction results
transform_input_s3 = f"s3://{bucket}/{transform_input_key}"
transform_output_s3 = f"s3://{bucket}/{transform_output_key}"

# Submit batch transform job
# Launches a SageMaker Batch Transform job, specifying model, input/output locations, format, and instance type
try:
    sagemaker.create_transform_job(
        TransformJobName=transform_job_name,
        ModelName=model_name,
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

    logging.info("✅ Batch transform job started successfully.")
    logging.info(f"🔢 Job Name: {transform_job_name}")
    logging.info(f"📤 Input Location: {transform_input_s3}")
    logging.info(f"📁 Output Location: {transform_output_s3}")

except Exception as e:
    logging.error(f"❌ Failed to start batch transform: {e}")