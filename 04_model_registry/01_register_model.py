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
s3_bucket = os.getenv("S3_BUCKET")

if not (best_training_job and model_package_group and role and s3_bucket):
    raise ValueError("❌ Required environment variables are missing from .env.")

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
# Validate model artifact
# ----------------------------
artifact_path = f"output/{best_training_job}/output/model.tar.gz"
model_artifact = f"s3://{s3_bucket}/{artifact_path}"

try:
    s3_client.head_object(Bucket=s3_bucket, Key=artifact_path)
    logger.info(f"📦 Model artifact found at: {model_artifact}")
    logger.info("✅ Model artifact exists in S3.")
except s3_client.exceptions.ClientError:
    logger.error(f"❌ S3 model artifact not found: {model_artifact}")

    # Try fallback to base training job from logs
    logs_path = project_root / "03_model_training" / "logs"
    fallback_job = None
    for log_file in sorted(logs_path.glob("train-*.log"), reverse=True):
        with open(log_file) as f:
            for line in f:
                if "📦 Training Job:" in line and best_training_job not in line:
                    fallback_job = line.strip().split()[-1]
                    break
        if fallback_job:
            break

    if not fallback_job:
        raise ValueError("❌ Could not find fallback base training job in logs.")

    logger.warning(f"📌 Falling back to base training job: {fallback_job}")
    best_training_job = fallback_job
    artifact_path = f"output/{best_training_job}/output/model.tar.gz"
    model_artifact = f"s3://{s3_bucket}/{artifact_path}"

    # Update BEST_TRAINING_JOB_NAME in .env
    env_path = project_root / ".env"
    lines = env_path.read_text().splitlines()
    lines = [l for l in lines if not l.startswith("BEST_TRAINING_JOB_NAME=")]
    lines.append(f"BEST_TRAINING_JOB_NAME={best_training_job}")
    env_path.write_text("\n".join(lines) + "\n")
    logger.info(f"📌 Updated .env → BEST_TRAINING_JOB_NAME={best_training_job}")

    # Re-check fallback model
    try:
        s3_client.head_object(Bucket=s3_bucket, Key=artifact_path)
        logger.info(f"✅ Fallback model artifact exists: {model_artifact}")
    except s3_client.exceptions.ClientError:
        raise FileNotFoundError(f"❌ Fallback model artifact also not found: {model_artifact}")

# ----------------------------
# Get training job info
# ----------------------------
training_job_info = sm_client.describe_training_job(TrainingJobName=best_training_job)

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
