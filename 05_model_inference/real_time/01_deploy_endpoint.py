import os
import logging
import boto3
from dotenv import load_dotenv
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

project_root = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=project_root / ".env", override=True)

sm = boto3.client("sagemaker", region_name=os.getenv("AWS_REGION"))
model_name = os.getenv("XGB_REGISTERED_MODEL_NAME")
endpoint_config_name = f"{model_name}-config"
endpoint_name = f"{model_name}-endpoint"

logger.info(f"🧠 Creating endpoint config: {endpoint_config_name}")
sm.create_endpoint_config(
    EndpointConfigName=endpoint_config_name,
    ProductionVariants=[{
        "VariantName": "AllTraffic",
        "ModelName": model_name,
        "InstanceType": "ml.m5.large",
        "InitialInstanceCount": 1
    }]
)

logger.info(f"🚀 Deploying endpoint: {endpoint_name}")
sm.create_endpoint(EndpointName=endpoint_name, EndpointConfigName=endpoint_config_name)
logger.info(f"✅ Endpoint deployment started: {endpoint_name}")