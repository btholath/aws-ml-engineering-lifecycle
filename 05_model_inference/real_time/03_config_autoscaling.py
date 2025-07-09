import os
import logging
import boto3
from dotenv import load_dotenv
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

project_root = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=project_root / ".env", override=True)

app = boto3.client("application-autoscaling")
endpoint = os.getenv("XGB_INFERENCE_ENDPOINT")

app.register_scalable_target(
    ServiceNamespace='sagemaker',
    ResourceId=f"endpoint/{endpoint}/variant/AllTraffic",
    ScalableDimension="sagemaker:variant:DesiredInstanceCount",
    MinCapacity=1,
    MaxCapacity=5,
)

logger.info("✅ Autoscaling registered.")