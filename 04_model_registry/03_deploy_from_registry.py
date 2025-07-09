import os
import time
import logging
import boto3
from dotenv import load_dotenv
from pathlib import Path

# ----------------------------
# Load environment variables
# ----------------------------
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

region = os.getenv("AWS_REGION", "us-east-1")
role = os.getenv("SAGEMAKER_ROLE_ARN")
endpoint_name = os.getenv("XGB_INFERENCE_ENDPOINT")
model_package_group = os.getenv("MODEL_PACKAGE_GROUP")

if not role or not model_package_group or not endpoint_name:
    raise ValueError("❌ One or more required variables are missing in .env")

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# SageMaker client
# ----------------------------
sm_client = boto3.client("sagemaker", region_name=region)

# ----------------------------
# Get latest approved model package
# ----------------------------
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

# ----------------------------
# Create SageMaker Model
# ----------------------------
model_name = endpoint_name + "-model"
try:
    sm_client.describe_model(ModelName=model_name)
    logger.info(f"♻️ Model already exists: {model_name}")
except sm_client.exceptions.ClientError:
    sm_client.create_model(
        ModelName=model_name,
        ExecutionRoleArn=role,
        Containers=[{"ModelPackageName": model_package_arn}]
    )
    logger.info(f"🧠 Model created: {model_name}")

# ----------------------------
# Create Endpoint Config
# ----------------------------
endpoint_config_name = endpoint_name + "-config"
try:
    sm_client.describe_endpoint_config(EndpointConfigName=endpoint_config_name)
    logger.info(f"♻️ Endpoint config already exists: {endpoint_config_name}")
except sm_client.exceptions.ClientError:
    sm_client.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=[{
            "VariantName": "AllTraffic",
            "ModelName": model_name,
            "InitialInstanceCount": 1,
            "InstanceType": "ml.m5.large"
        }]
    )
    logger.info(f"⚙️ Endpoint config created: {endpoint_config_name}")

# ----------------------------
# Deploy or update Endpoint
# ----------------------------
import botocore

try:
    existing_endpoint = sm_client.describe_endpoint(EndpointName=endpoint_name)
    existing_config_name = existing_endpoint["EndpointConfigName"]

    if existing_config_name == endpoint_config_name:
        # Cannot update with the same config name, create a new one
        new_config_name = f"{endpoint_config_name}-{int(time.time())}"
        sm_client.create_endpoint_config(
            EndpointConfigName=new_config_name,
            ProductionVariants=[{
                "VariantName": "AllTraffic",
                "ModelName": model_name,
                "InitialInstanceCount": 1,
                "InstanceType": "ml.m5.large"
            }]
        )
        logger.warning(f"♻️ Created new endpoint config: {new_config_name}")
        sm_client.update_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=new_config_name
        )
        logger.info(f"✅ Endpoint updated with new config: {new_config_name}")
    else:
        sm_client.update_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=endpoint_config_name
        )
        logger.info(f"✅ Endpoint updated with config: {endpoint_config_name}")

except botocore.exceptions.ClientError as error:
    error_code = error.response["Error"]["Code"]
    if error_code == "ValidationException" and "Could not find endpoint" in str(error):
        sm_client.create_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=endpoint_config_name
        )
        logger.info(f"🚀 Created new endpoint: {endpoint_name}")
    else:
        raise

logger.info(f"✅ Model deployed to endpoint: {endpoint_name}")
