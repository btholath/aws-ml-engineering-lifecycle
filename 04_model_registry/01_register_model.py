import os
import logging
import boto3
from pathlib import Path
from dotenv import load_dotenv
from sagemaker import Session
from sagemaker.model import Model

# ----------------------------
# Load .env from project root
# ----------------------------
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

best_training_job = os.getenv("BEST_TRAINING_JOB_NAME")
model_package_group = os.getenv("MODEL_PACKAGE_GROUP")
role = os.getenv("SAGEMAKER_ROLE_ARN")
region = os.getenv("AWS_REGION", "us-east-1")

if not best_training_job:
    raise ValueError("❌ BEST_TRAINING_JOB_NAME is not set in .env.")
if not model_package_group:
    raise ValueError("❌ MODEL_PACKAGE_GROUP is not set in .env.")
if not role:
    raise ValueError("❌ SAGEMAKER_ROLE_ARN is not set in .env.")

# ----------------------------
# Setup logging
# ----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# Setup Boto3 and SageMaker SDK
# ----------------------------
sm_client = boto3.client("sagemaker", region_name=region)
session = Session()

# ----------------------------
# Get model artifact S3 path from the training job
# ----------------------------
training_job_info = sm_client.describe_training_job(TrainingJobName=best_training_job)
model_artifact = training_job_info["ModelArtifacts"]["S3ModelArtifacts"]
logger.info(f"📦 Model artifact found at: {model_artifact}")

# ----------------------------
# Register model
# ----------------------------
model_package_input = {
    "ModelPackageGroupName": model_package_group,
    "ModelPackageDescription": f"XGBoost model from training job {best_training_job}",
    "InferenceSpecification": {
        "Containers": [
            {
                "Image": training_job_info["AlgorithmSpecification"]["TrainingImage"],
                "ModelDataUrl": model_artifact,
                "Environment": {}
            }
        ],
        "SupportedContentTypes": ["text/csv"],
        "SupportedResponseMIMETypes": ["text/csv"],
    },
    "ModelApprovalStatus": "PendingManualApproval"
}

response = sm_client.create_model_package(**model_package_input)
model_package_arn = response["ModelPackageArn"]
logger.info(f"✅ Model registered: {model_package_arn}")
