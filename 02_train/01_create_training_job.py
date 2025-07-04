"""
Create a training job using the realistic loan approval dataset.
"""

import boto3
import time
from sagemaker import image_uris

# Initialize Boto3 SageMaker client
sagemaker_client = boto3.client("sagemaker", region_name="us-east-1")

# Define Training Job Parameters
training_job_name = f"real-loan-predictor-xgboost-training-{int(time.time())}"

# S3 paths (Replace with your actual S3 bucket and paths)
s3_bucket = "btholath-sagemaker-datawrangler-demo"
training_data_s3_uri = f"s3://{s3_bucket}/data/sample_realistic_loan_approval_dataset.parquet"
output_s3_uri = f"s3://{s3_bucket}/real-loan-predictor-output/"

# SageMaker Execution Role ARN (Replace with your SageMaker role)
sagemaker_role = "arn:aws:iam::637423309379:role/service-role/AmazonSageMaker-ExecutionRole-20250704T144877"