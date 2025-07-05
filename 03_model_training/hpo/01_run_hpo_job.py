import os
import logging
from datetime import datetime

import boto3
import sagemaker
from dotenv import load_dotenv
from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput
from sagemaker.tuner import (
    HyperparameterTuner,
    ContinuousParameter,
    IntegerParameter
)

# -----------------------------
# Setup Environment & Logging
# -----------------------------
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

region = boto3.Session().region_name
role = os.getenv("SAGEMAKER_ROLE_ARN")
bucket = os.getenv("S3_BUCKET")

if not role:
    raise ValueError("❌ SAGEMAKER_ROLE_ARN is not set in the environment.")
if not bucket:
    raise ValueError("❌ S3_BUCKET is not set in the environment.")


# -----------------------------
# Utility: Update .env File
# -----------------------------
def update_env_variable(key: str, value: str, env_file=".env"):
    """Update or append a key=value pair in a .env file."""
    lines = []
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            lines = f.readlines()

    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            updated = True
            break

    if not updated:
        lines.append(f"{key}={value}\n")

    with open(env_file, "w") as f:
        f.writelines(lines)


# -----------------------------
# Create Estimator
# -----------------------------
def create_estimator(image_uri: str, role: str, bucket: str, session) -> Estimator:
    return Estimator(
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


# -----------------------------
# Create HPO Tuner
# -----------------------------
def create_tuner(estimator: Estimator) -> HyperparameterTuner:
    hyperparameter_ranges = {
        "eta": ContinuousParameter(0.01, 0.3),
        "max_depth": IntegerParameter(3, 10),
        "subsample": ContinuousParameter(0.5, 1.0),
        "min_child_weight": ContinuousParameter(1, 10),
        "alpha": ContinuousParameter(0, 2)
    }

    return HyperparameterTuner(
        estimator=estimator,
        objective_metric_name="validation:logloss",
        hyperparameter_ranges=hyperparameter_ranges,
        objective_type="Minimize",
        max_jobs=5,
        max_parallel_jobs=2,
        base_tuning_job_name="xgb-hpo"
    )


# -----------------------------
# Main HPO Logic
# -----------------------------
def main():
    tuning_job_name = f"xgb-hpo-{datetime.now().strftime('%y%m%d-%H%M')}"
    update_env_variable("HPO_TUNING_JOB_NAME", tuning_job_name)

    image_uri = sagemaker.image_uris.retrieve("xgboost", region=region, version="1.7-1")
    session = sagemaker.Session()

    estimator = create_estimator(image_uri, role, bucket, session)
    tuner = create_tuner(estimator)

    train_input = TrainingInput(
        f"s3://{bucket}/data/sample_realistic_loan_approval_dataset_ready.csv",
        content_type="csv"
    )

    validation_input = TrainingInput(
        f"s3://{bucket}/data/validation/sample_realistic_loan_approval_dataset_ready.csv",
        content_type="csv"
    )

    tuner.fit({"train": train_input, "validation": validation_input})
    logger.info(f"🚀 HPO job submitted: {tuning_job_name}")


if __name__ == "__main__":
    main()
