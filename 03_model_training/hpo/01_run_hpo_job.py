"""
Run SageMaker hyperparameter tuning job for XGBoost.
"""
from sagemaker.tuner import HyperparameterTuner, IntegerParameter, ContinuousParameter
from sagemaker.xgboost.estimator import XGBoost
import os, logging
from dotenv import load_dotenv
import sagemaker

load_dotenv()
logging.basicConfig(level=logging.INFO)

session = sagemaker.Session()
bucket = os.getenv("S3_BUCKET")
role = os.getenv("SAGEMAKER_ROLE_ARN")
region = os.getenv("AWS_REGION")

xgb = XGBoost(
    entry_point="train.py",
    framework_version="1.3-1",
    role=role,
    instance_type="ml.m5.large",
    output_path=f"s3://{bucket}/hpo-output",
    sagemaker_session=session,
)

hyperparameter_ranges = {
    "max_depth": IntegerParameter(3, 10),
    "eta": ContinuousParameter(0.1, 0.5),
    "gamma": ContinuousParameter(0, 5),
}

tuner = HyperparameterTuner(
    estimator=xgb,
    objective_metric_name="validation:auc",
    hyperparameter_ranges=hyperparameter_ranges,
    metric_definitions=[{"Name": "validation:auc", "Regex": "auc:([0-9\\.]+)"}],
    max_jobs=10,
    max_parallel_jobs=2,
)

s3_uri = f"s3://{bucket}/data/sample_realistic_loan_approval_dataset_ready.csv"
tuner.fit({"train": sagemaker.inputs.TrainingInput(s3_uri, content_type="csv")})
logging.info("🚀 HPO job submitted")
