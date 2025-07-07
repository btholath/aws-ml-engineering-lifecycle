import os
import logging
import boto3
from dotenv import load_dotenv
from pathlib import Path
from botocore.exceptions import ClientError

# Load .env
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

region = os.getenv("AWS_REGION", "us-east-1")
endpoint_name = os.getenv("XGB_INFERENCE_ENDPOINT")
model_package_group = os.getenv("MODEL_PACKAGE_GROUP")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sm_client = boto3.client("sagemaker", region_name=region)

# --------------------------------------------
# 1. Delete Endpoint (if exists)
# --------------------------------------------
def delete_endpoint(name):
    try:
        sm_client.describe_endpoint(EndpointName=name)
        logger.info(f"❌ Deleting endpoint: {name}")
        sm_client.delete_endpoint(EndpointName=name)
    except ClientError as e:
        if "Could not find endpoint" in str(e):
            logger.info(f"✅ Endpoint not found: {name}")
        else:
            raise

# --------------------------------------------
# 2. Delete Endpoint Config
# --------------------------------------------
def delete_endpoint_config(name):
    config_name = f"{name}-config"
    try:
        sm_client.describe_endpoint_config(EndpointConfigName=config_name)
        logger.info(f"❌ Deleting endpoint config: {config_name}")
        sm_client.delete_endpoint_config(EndpointConfigName=config_name)
    except ClientError:
        logger.info(f"✅ Endpoint config not found: {config_name}")

# --------------------------------------------
# 3. Delete Model
# --------------------------------------------
def delete_model(name):
    model_name = f"{name}-model"
    try:
        sm_client.describe_model(ModelName=model_name)
        logger.info(f"❌ Deleting model: {model_name}")
        sm_client.delete_model(ModelName=model_name)
    except ClientError:
        logger.info(f"✅ Model not found: {model_name}")

# --------------------------------------------
# 4. (Optional) Delete Model Packages
# --------------------------------------------
def delete_model_packages(group_name):
    response = sm_client.list_model_packages(
        ModelPackageGroupName=group_name,
        SortBy="CreationTime",
        SortOrder="Descending"
    )
    packages = response.get("ModelPackageSummaryList", [])
    for pkg in packages:
        arn = pkg["ModelPackageArn"]
        logger.info(f"❌ Deleting model package: {arn}")
        sm_client.delete_model_package(ModelPackageName=arn)

# --------------------------------------------
# 5. (Optional) Delete Model Package Group
# --------------------------------------------
def delete_model_package_group(group_name):
    try:
        sm_client.describe_model_package_group(ModelPackageGroupName=group_name)
        logger.info(f"❌ Deleting model package group: {group_name}")
        sm_client.delete_model_package_group(ModelPackageGroupName=group_name)
    except ClientError:
        logger.info(f"✅ Model package group not found: {group_name}")

# Execute teardown
logger.info("🔻 Tearing down SageMaker model endpoint and registry...")

delete_endpoint(endpoint_name)
delete_endpoint_config(endpoint_name)
delete_model(endpoint_name)

# Comment out if you want to retain model registry
delete_model_packages(model_package_group)
delete_model_package_group(model_package_group)

logger.info("✅ Teardown complete.")
