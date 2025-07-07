import os
import logging
import boto3
from dotenv import load_dotenv
from pathlib import Path

# Load environment
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

region = os.getenv("AWS_REGION", "us-east-1")
role = os.getenv("SAGEMAKER_ROLE_ARN")
endpoint_name = os.getenv("XGB_INFERENCE_ENDPOINT")
model_package_group = os.getenv("MODEL_PACKAGE_GROUP")

if not role or not model_package_group or not endpoint_name:
    raise ValueError("❌ One or more required variables are missing in .env")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Boto3 client
sm_client = boto3.client("sagemaker", region_name=region)

# Get latest approved model package
response = sm_client.list_model_packages(
    ModelPackageGroupName=model_package_group,
    SortBy="CreationTime",
    SortOrder="Descending",
    MaxResults=1,
    ModelApprovalStatus="Approved"
)

if not response["ModelPackageSummaryList"]:
    raise ValueError(f"❌ No approved models found in group: {model_package_group}")

model_package_arn = response["ModelPackageSummaryList"][0]["ModelPackageArn"]
logger.info(f"✅ Using approved model package: {model_package_arn}")

# Create model
model_name = endpoint_name + "-model"
sm_client.create_model(
    ModelName=model_name,
    ExecutionRoleArn=role,
    Containers=[
        {
            "ModelPackageName": model_package_arn
        }
    ]
)
logger.info(f"🧠 Model created: {model_name}")

# Create endpoint config
config_name = endpoint_name + "-config"
sm_client.create_endpoint_config(
    EndpointConfigName=config_name,
    ProductionVariants=[
        {
            "VariantName": "AllTraffic",
            "ModelName": model_name,
            "InitialInstanceCount": 1,
            "InstanceType": "ml.m5.large"
        }
    ]
)
logger.info(f"⚙️ Endpoint config created: {config_name}")

# Deploy endpoint
try:
    sm_client.describe_endpoint(EndpointName=endpoint_name)
    logger.info(f"♻️ Updating existing endpoint: {endpoint_name}")
    sm_client.update_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=config_name
    )
except sm_client.exceptions.ClientError:
    logger.info(f"🚀 Creating new endpoint: {endpoint_name}")
    sm_client.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=config_name
    )

logger.info(f"✅ Model deployed to endpoint: {endpoint_name}")
