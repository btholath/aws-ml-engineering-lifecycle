import os
import time
import logging
import boto3
from dotenv import load_dotenv
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env from project root
project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=project_root / ".env", override=True)

region = os.getenv("AWS_REGION", "us-east-1")
endpoint_name = os.getenv("XGB_INFERENCE_ENDPOINT")

if not endpoint_name:
    raise ValueError("❌ XGB_INFERENCE_ENDPOINT is not set in .env")

sm = boto3.client("sagemaker", region_name=region)
app = boto3.client("application-autoscaling", region_name=region)

# Wait for endpoint to be in service
def wait_for_endpoint_ready(endpoint, timeout=600):
    logger.info(f"⏳ Waiting for endpoint '{endpoint}' to become InService...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        status = sm.describe_endpoint(EndpointName=endpoint)["EndpointStatus"]
        logger.info(f"📍 Current endpoint status: {status}")
        if status == "InService":
            logger.info(f"✅ Endpoint is ready: {endpoint}")
            return
        elif status == "Failed":
            raise RuntimeError(f"❌ Endpoint '{endpoint}' creation failed.")
        time.sleep(10)
    raise TimeoutError(f"❌ Timeout: Endpoint '{endpoint}' did not become InService in time.")

wait_for_endpoint_ready(endpoint_name)

# Register scalable target
resource_id = f"endpoint/{endpoint_name}/variant/AllTraffic"
scalable_dimension = "sagemaker:variant:DesiredInstanceCount"

logger.info("📈 Registering scalable target...")
app.register_scalable_target(
    ServiceNamespace="sagemaker",
    ResourceId=resource_id,
    ScalableDimension=scalable_dimension,
    MinCapacity=1,
    MaxCapacity=3
)

# Define autoscaling policy
logger.info("⚙️ Putting scaling policy...")
app.put_scaling_policy(
    PolicyName="Invocations-ScalingPolicy",
    ServiceNamespace="sagemaker",
    ResourceId=resource_id,
    ScalableDimension=scalable_dimension,
    PolicyType="TargetTrackingScaling",
    TargetTrackingScalingPolicyConfiguration={
        "TargetValue": 70.0,
        "PredefinedMetricSpecification": {
            "PredefinedMetricType": "SageMakerVariantInvocationsPerInstance"
        },
        "ScaleInCooldown": 300,
        "ScaleOutCooldown": 300
    }
)

logger.info("✅ Autoscaling configuration applied successfully.")
