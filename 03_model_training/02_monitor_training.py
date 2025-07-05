"""
Monitor and log SageMaker training job status.
"""
import boto3, logging
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
client = boto3.client("sagemaker", region_name=os.getenv("AWS_REGION"))

job_name = os.getenv("TRAINING_JOB_NAME")

response = client.describe_training_job(TrainingJobName=job_name)
status = response["TrainingJobStatus"]
logging.info(f"🔍 Training Job '{job_name}' Status: {status}")
