import os
import time
import logging
import boto3
from dotenv import load_dotenv
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from project root
project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=project_root / ".env", override=True)

region = os.getenv("AWS_REGION", "us-east-1")
role = os.getenv("SAGEMAKER_ROLE_ARN")
model_name = os.getenv("XGB_INFERENCE_ENDPOINT") + "-model"
endpoint_name = os.getenv("XGB_INFERENCE_ENDPOINT")
config_name = model_name + "-config"

sm = boto3.client("sagemaker", region_name=region)

# Wait for endpoint to finish if in progress
def wait_for_endpoint(endpoint_name, desired_status="InService", timeout=600):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = sm.describe_endpoint(EndpointName=endpoint_name)
            status = response["EndpointStatus"]
            logger.info(f"⏳ Endpoint status: {status}")
            if status == desired_status:
                return True
            elif status == "Failed":
                raise RuntimeError(f"❌ Endpoint '{endpoint_name}' failed.")
        except sm.exceptions.ClientError:
            break  # endpoint does not exist yet
        time.sleep(10)
    raise TimeoutError(f"❌ Timed out waiting for endpoint '{endpoint_name}' to become {desired_status}.")

# Create or update endpoint config
try:
    sm.describe_endpoint_config(EndpointConfigName=config_name)
    logger.info(f"♻️ Endpoint config already exists: {config_name}")
except sm.exceptions.ClientError:
    sm.create_endpoint_config(
        EndpointConfigName=config_name,
        ProductionVariants=[{
            "VariantName": "AllTraffic",
            "ModelName": model_name,
            "InitialInstanceCount": 1,
            "InstanceType": "ml.m5.large"
        }]
    )
    logger.info(f"✅ Created endpoint config: {config_name}")

# Create or update endpoint
try:
    response = sm.describe_endpoint(EndpointName=endpoint_name)
    current_config = response["EndpointConfigName"]

    if current_config == config_name:
        # Cannot update to same config; create a new one
        new_config_name = config_name + f"-{int(time.time())}"
        sm.create_endpoint_config(
            EndpointConfigName=new_config_name,
            ProductionVariants=[{
                "VariantName": "AllTraffic",
                "ModelName": model_name,
                "InitialInstanceCount": 1,
                "InstanceType": "ml.m5.large"
            }]
        )
        logger.warning(f"⚠️ Same config already in use. Created new config: {new_config_name}")
        wait_for_endpoint(endpoint_name, "InService")  # Ensure it's ready
        sm.update_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=new_config_name
        )
        logger.info(f"✅ Endpoint updated with new config: {new_config_name}")
    else:
        wait_for_endpoint(endpoint_name, "InService")
        sm.update_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=config_name
        )
        logger.info(f"✅ Endpoint updated to config: {config_name}")

except sm.exceptions.ResourceNotFound:
    sm.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=config_name
    )
    logger.info(f"🚀 Created new endpoint: {endpoint_name}")
