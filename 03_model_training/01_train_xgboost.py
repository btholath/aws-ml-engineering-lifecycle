"""
Train XGBoost model on SageMaker using cleaned dataset from S3.
"""
import boto3, sagemaker
import os, logging
from sagemaker.inputs import TrainingInput
from sagemaker.xgboost.estimator import XGBoost
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

session = sagemaker.Session()
role = os.getenv("SAGEMAKER_ROLE_ARN")
bucket = os.getenv("S3_BUCKET")
region = os.getenv("AWS_REGION", "us-east-1")
s3_uri = f"s3://{bucket}/data/sample_realistic_loan_approval_dataset_ready.csv"

xgb_estimator = XGBoost(
    entry_point="train.py",  # Use custom training script if needed
    framework_version="1.3-1",
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f"s3://{bucket}/real-loan-predictor-output",
    sagemaker_session=session,
    hyperparameters={
        "max_depth": 5,
        "eta": 0.2,
        "objective": "binary:logistic",
        "num_round": 100,
    },
)

xgb_estimator.fit({"train": TrainingInput(s3_uri, content_type="csv")})
logging.info("✅ XGBoost training job submitted")
