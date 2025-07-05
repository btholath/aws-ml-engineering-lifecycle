import os
import logging
import boto3
import sagemaker  # ✅ this was missing
from dotenv import load_dotenv
from sagemaker import Session
from sagemaker.inputs import TrainingInput
from sagemaker.estimator import Estimator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
role = os.getenv("SAGEMAKER_ROLE_ARN")
bucket = os.getenv("S3_BUCKET")
region = os.getenv("AWS_REGION", "us-east-1")

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

# Save job name to file
with open("latest_training_job.txt", "w") as f:
    f.write(xgb_estimator.latest_training_job.name)
