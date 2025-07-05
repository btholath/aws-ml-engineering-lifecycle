import boto3
import logging

logging.basicConfig(level=logging.INFO)
client = boto3.client("sagemaker")

# Read training job name
with open("latest_training_job.txt", "r") as f:
    job_name = f.read().strip()

# Describe training job
response = client.describe_training_job(TrainingJobName=job_name)

# Print key status info
status = response["TrainingJobStatus"]
model_artifacts = response["ModelArtifacts"]["S3ModelArtifacts"]
logging.info(f"📊 Training job '{job_name}' status: {status}")
logging.info(f"📦 Model saved to: {model_artifacts}")
