import os
import logging
import boto3
from dotenv import load_dotenv
from pathlib import Path

# Setup project root and load .env
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

region = os.getenv("AWS_REGION", "us-east-1")
model_package_group = os.getenv("MODEL_PACKAGE_GROUP")

if not model_package_group:
    raise ValueError("❌ MODEL_PACKAGE_GROUP is not set in .env.")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Boto3 client
sm_client = boto3.client("sagemaker", region_name=region)

# Get the latest model package
response = sm_client.list_model_packages(
    ModelPackageGroupName=model_package_group,
    SortBy="CreationTime",
    SortOrder="Descending",
    MaxResults=1
)

if not response["ModelPackageSummaryList"]:
    raise ValueError(f"❌ No model packages found in group: {model_package_group}")

latest_model_package_arn = response["ModelPackageSummaryList"][0]["ModelPackageArn"]
logger.info(f"🆕 Latest model package: {latest_model_package_arn}")

# Approve the model
sm_client.update_model_package(
    ModelPackageArn=latest_model_package_arn,
    ModelApprovalStatus="Approved",
    ApprovalDescription="Auto-approved via pipeline."
)

logger.info(f"✅ Approved model package: {latest_model_package_arn}")
