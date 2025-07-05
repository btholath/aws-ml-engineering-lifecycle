import os
import logging
import boto3
import sagemaker
from sagemaker.estimator import Estimator
from sagemaker.tuner import HyperparameterTuner, ContinuousParameter, IntegerParameter
from sagemaker.inputs import TrainingInput
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

region = boto3.Session().region_name
role = os.getenv("SAGEMAKER_ROLE_ARN")
bucket = os.getenv("S3_BUCKET")

if not role:
    raise ValueError("❌ SAGEMAKER_ROLE_ARN is not set in the environment.")

# S3 path to dataset
s3_uri = f"s3://{bucket}/data/sample_realistic_loan_approval_dataset_ready.csv"

# XGBoost container image
image_uri = sagemaker.image_uris.retrieve("xgboost", region=region, version="1.7-1")
session = sagemaker.Session()

# Define base estimator
xgb_estimator = Estimator(
    image_uri=image_uri,
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f"s3://{bucket}/output",
    sagemaker_session=session,
    hyperparameters={
        "objective": "binary:logistic",
        "num_round": "100"
    }
)

# Define HPO search space
hyperparameter_ranges = {
    "eta": ContinuousParameter(0.01, 0.3),
    "max_depth": IntegerParameter(3, 10),
    "subsample": ContinuousParameter(0.5, 1.0),
    "min_child_weight": ContinuousParameter(1, 10),
    "alpha": ContinuousParameter(0, 2)
}

# Define HPO tuner
tuner = HyperparameterTuner(
    estimator=xgb_estimator,
    objective_metric_name="validation:logloss",
    hyperparameter_ranges=hyperparameter_ranges,
    objective_type="Minimize",
    max_jobs=5,
    max_parallel_jobs=2,
    base_tuning_job_name="xgb-hpo"
)

# Submit tuning job
#tuner.fit({"train": TrainingInput(s3_uri, content_type="csv")})
tuner.fit({
    "train": TrainingInput(s3_uri, content_type="csv"),
    "validation": TrainingInput(f"s3://{bucket}/data/validation/sample_realistic_loan_approval_dataset_ready.csv", content_type="csv")
})
logger.info("🚀 HPO job submitted")
