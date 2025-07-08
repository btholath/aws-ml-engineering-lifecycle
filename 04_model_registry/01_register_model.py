import os
import logging
import boto3
from pathlib import Path
from dotenv import load_dotenv
from sagemaker import Session

# Load .env
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

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Boto3/SageMaker
sm_client = boto3.client("sagemaker", region_name=region)
session = Session()

# Get model artifact S3 path
training_job_info = sm_client.describe_training_job(TrainingJobName=best_training_job)
model_artifact = training_job_info["ModelArtifacts"]["S3ModelArtifacts"]
logger.info(f"📦 Model artifact found at: {model_artifact}")

# Ensure Model Package Group exists or create it
try:
    sm_client.describe_model_package_group(ModelPackageGroupName=model_package_group)
    logger.info(f"✅ Model Package Group '{model_package_group}' already exists.")
except sm_client.exceptions.ClientError as e:
    if "does not exist" in str(e):
        logger.info(f"📦 Creating Model Package Group '{model_package_group}'...")
        sm_client.create_model_package_group(
            ModelPackageGroupName=model_package_group,
            ModelPackageGroupDescription="Model group for loan approval classification models"
        )
        logger.info(f"✅ Created Model Package Group '{model_package_group}'")
    else:
        raise e

# Register model package
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
logger.info("END_OF_01_register_model.py")