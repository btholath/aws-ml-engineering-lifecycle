"""
Create a training job using the realistic loan approval dataset.
"""

# File: 01_model_training/train_xgboost_loan_predictor.py

import os
import time
import logging
from dotenv import load_dotenv
import boto3
from sagemaker import image_uris

# Load .env variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Load config from .env
region = os.getenv("AWS_REGION", "us-east-1")
sagemaker_role = os.getenv("SAGEMAKER_ROLE_ARN")
bucket = os.getenv("S3_BUCKET")
training_data_key = os.getenv("TRAINING_DATA_KEY")
training_output_prefix = os.getenv("TRAINING_OUTPUT_PREFIX")

if not all([sagemaker_role, bucket, training_data_key]):
    logging.error("Missing required environment variables.")
    exit(1)

# Compose full S3 paths
training_data_s3_uri = f"s3://{bucket}/{training_data_key}"
output_s3_uri = f"s3://{bucket}/{training_output_prefix}/"

# Create a SageMaker client
sagemaker_client = boto3.client("sagemaker", region_name=region)

# Get image URI for XGBoost
xgboost_image_uri = image_uris.retrieve(framework='xgboost', region=region, version='1.7-1')
logging.info(f"Using XGBoost image URI: {xgboost_image_uri}")

# Generate a unique training job name
training_job_name = f"real-loan-predictor-xgb-{int(time.time())}"

# Define the training job parameters
training_params = {
    "TrainingJobName": training_job_name,
    "AlgorithmSpecification": {
        "TrainingImage": xgboost_image_uri,
        "TrainingInputMode": "File",
    },
    "RoleArn": sagemaker_role,
    "HyperParameters": {
        "num_round": "100",
        "eta": "0.2",
        "objective": "reg:squarederror",
        "max_depth": "6",
        "subsample": "0.8",
        "eval_metric": "rmse",
    },
    "InputDataConfig": [
    {
        "ChannelName": "train",
        "DataSource": {
            "S3DataSource": {
                "S3DataType": "S3Prefix",  # ✅ still correct for CSV
                "S3Uri": "s3://btholath-sagemaker-datawrangler-demo/data/sample_loan_fixed_for_xgboost.csv",
                "S3DataDistributionType": "FullyReplicated"
            }
        },
        "ContentType": "text/csv",
        "CompressionType": "None"
    }
]

,
    "OutputDataConfig": {"S3OutputPath": output_s3_uri},
    "ResourceConfig": {
        "InstanceType": "ml.m5.large",
        "InstanceCount": 1,
        "VolumeSizeInGB": 10,
    },
    "StoppingCondition": {"MaxRuntimeInSeconds": 3600},
}

# Start training job
try:
    logging.info("Starting SageMaker training job...")
    response = sagemaker_client.create_training_job(**training_params)
    logging.info(f"✅ Training job created: {training_job_name}")
    logging.info(f"📦 Output S3 path: {output_s3_uri}")
    logging.info(f"🔗 Job ARN: {response['TrainingJobArn']}")
except Exception as e:
    logging.error(f"❌ Failed to start training job: {e}")

