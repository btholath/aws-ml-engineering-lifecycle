import os
import logging
import boto3
from pathlib import Path
from dotenv import load_dotenv
from sagemaker import Session

# ----------------------------
# Load .env
# ----------------------------
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

best_training_job = os.getenv("BEST_TRAINING_JOB_NAME")
model_package_group = os.getenv("MODEL_PACKAGE_GROUP")
role = os.getenv("SAGEMAKER_ROLE_ARN")
region = os.getenv("AWS_REGION", "us-east-1")

assert best_training_job, "❌ BEST_TRAINING_JOB_NAME is not set."
assert model_package_group, "❌ MODEL_PACKAGE_GROUP is not set."
assert role, "❌ SAGEMAKER_ROLE_ARN is not set."

# ----------------------------
# Logging
# ----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# Setup clients
# ----------------------------
sm_client = boto3.client("sagemaker", region_name=region)
s3_client = boto3.client("s3", region_name=region)
session = Session()

# ----------------------------
# Get model artifact
# ----------------------------
training_job_info = sm_client.describe_training_job(TrainingJobName=best_training_job)
model_artifact = training_job_info["ModelArtifacts"]["S3ModelArtifacts"]
logger.info(f"📦 Model artifact found at: {model_artifact}")

# ----------------------------
# Validate S3 artifact exists
# ----------------------------
parsed = model_artifact.replace("s3://", "").split("/", 1)
bucket = parsed[0]
key = parsed[1]

try:
    s3_client.head_object(Bucket=bucket, Key=key)
    logger.info("✅ Model artifact exists in S3.")
except s3_client.exceptions.ClientError:
    logger.error(f"❌ S3 model artifact not found: {model_artifact}")
    exit(1)

# ----------------------------
# Ensure Model Package Group exists
# ----------------------------
try:
    sm_client.describe_model_package_group(ModelPackageGroupName=model_package_group)
    logger.info(f"✅ Model Package Group '{model_package_group}' already exists.")
except sm_client.exceptions.ResourceNotFound:
    logger.info(f"📦 Model Package Group '{model_package_group}' not found. Creating it.")
    sm_client.create_model_package_group(
        ModelPackageGroupName=model_package_group,
        ModelPackageGroupDescription="Loan approval model group"
    )

# ----------------------------
# Register model
# ----------------------------
model_package_input = {
    "ModelPackageGroupName": model_package_group,
    "ModelPackageDescription": f"Model from training job {best_training_job}",
    "InferenceSpecification": {
        "Containers": [{
            "Image": training_job_info["AlgorithmSpecification"]["TrainingImage"],
            "ModelDataUrl": model_artifact,
            "Environment": {}
        }],
        "SupportedContentTypes": ["text/csv"],
        "SupportedResponseMIMETypes": ["text/csv"],
    },
    "ModelApprovalStatus": "PendingManualApproval"
}

response = sm_client.create_model_package(**model_package_input)
model_package_arn = response["ModelPackageArn"]
logger.info(f"✅ Model registered: {model_package_arn}")
