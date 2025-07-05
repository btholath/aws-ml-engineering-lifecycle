"""
This script is part of the MLOps / Model Governance phase:

🔄 ML Lifecycle Stage: Post-training / Model Registration
Stage	                     Description
✔️ Training Completed	    Model is already trained, tested, and saved to S3
✔️ Ready for Deployment	    Now it's time to package and version the model
✅ Model Registry Phase	   Register the model so it can be tracked, approved, or deployed

Purpose of register_model.py
This script registers a trained model in Amazon SageMaker Model Registry by:
-   Creating (if not already created) a Model Package Group
-   Packaging the trained model as a versioned model entry in that group
-   Setting it to a pending approval state so it can be reviewed and deployed through MLOps pipelines


"""

# Load required modules for AWS service interaction and timestamping
import boto3
import time
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Create a Boto3 client to communicate with the SageMaker service
region = os.getenv("AWS_REGION", "us-east-1")
sagemaker = boto3.client("sagemaker", region_name=region)

# Define a reusable logical group to hold model versions (like a model registry folder)
model_package_group_name = os.getenv("MODEL_PACKAGE_GROUP", "LoanApprovalModelGroup")

# Define the model version's name and path to the .tar.gz model artifact in S3
model_name = os.getenv("MODEL_NAME", f"real-loan-predictor-xgb-{int(time.time())}")

# Provide the trained model artifact location in S3
model_artifact = os.getenv(
    "MODEL_ARTIFACT",
    f"s3://{os.getenv('S3_BUCKET')}/real-loan-predictor-output/{model_name}/output/model.tar.gz"
)

# Create Model Package Group (if not exists)
# Try to create a new model group for organizing versions (if it doesn’t already exist)
try:
    sagemaker.create_model_package_group(
        ModelPackageGroupName=model_package_group_name,
        ModelPackageGroupDescription="Loan approval prediction models"
    )
    logging.info(f"✅ Created model package group: {model_package_group_name}")
except sagemaker.exceptions.ResourceInUse:
    logging.info(f"ℹ️ Model package group already exists: {model_package_group_name}")

# Register model
# Register a specific model version with associated metadata and container info
# Set the approval state (can later be changed to Approved or Rejected)
try:
    response = sagemaker.create_model_package(
        ModelPackageGroupName=model_package_group_name,
        ModelPackageDescription="XGBoost loan predictor",
        InferenceSpecification={
            "Containers": [{
                "Image": "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.7-1",
                "ModelDataUrl": model_artifact
            }],
            "SupportedContentTypes": ["text/csv"],
            "SupportedResponseMIMETypes": ["text/csv"]
        },
        ModelApprovalStatus="PendingManualApproval"
    )

    # Log the registered model ARN for tracking and auditing
    logging.info(f"✅ Model registered: {response['ModelPackageArn']}")

except Exception as e:
    logging.error(f"❌ Failed to register model: {e}")