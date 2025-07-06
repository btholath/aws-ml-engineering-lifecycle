import os
import logging
import boto3
import sagemaker
from pathlib import Path
from dotenv import load_dotenv
from sagemaker import Session
from sagemaker.inputs import TrainingInput
from sagemaker.estimator import Estimator

# ----------------------------
# Load .env from project root
# ----------------------------
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

role = os.getenv("SAGEMAKER_ROLE_ARN")
bucket = os.getenv("S3_BUCKET")
region = os.getenv("AWS_REGION", "us-east-1")

if not role:
    raise ValueError("❌ SAGEMAKER_ROLE_ARN is not set in the environment or .env file.")
print(f"Using SageMaker Role ARN: {role}")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define training input
s3_uri = f"s3://{bucket}/data/sample_realistic_loan_approval_dataset_ready.csv"
session = Session()

# XGBoost Estimator
xgb_estimator = Estimator(
    image_uri=sagemaker.image_uris.retrieve("xgboost", region, "1.7-1"),
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f"s3://{bucket}/output",
    sagemaker_session=session,
    hyperparameters={
        "objective": "binary:logistic",
        "num_round": 100,
        "max_depth": 5,
        "eta": 0.2,
    },
)

# Start training
xgb_estimator.fit({"train": TrainingInput(s3_uri, content_type="csv")})
logger.info("✅ XGBoost training job submitted")

# Save job name
latest_job_name = xgb_estimator.latest_training_job.name
logger.info(f"📦 Training Job: {latest_job_name}")

# Save to text file (optional)
with open("latest_training_job.txt", "w") as f:
    f.write(latest_job_name)

# ----------------------------
# Update .env with BEST_TRAINING_JOB_NAME
# ----------------------------
def update_env_variable(key: str, value: str, env_path: Path):
    lines = []
    found = False
    if env_path.exists():
        with open(env_path, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
            break
    if not found:
        lines.append(f"{key}={value}\n")

    with open(env_path, "w") as f:
        f.writelines(lines)

    logger.info(f"📌 Updated .env with {key}={value}")

# Update and reload
update_env_variable("BEST_TRAINING_JOB_NAME", latest_job_name, dotenv_path)
load_dotenv(dotenv_path=dotenv_path, override=True)
