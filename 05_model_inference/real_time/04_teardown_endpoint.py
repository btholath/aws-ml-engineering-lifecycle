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
endpoint = os.getenv("XGB_INFERENCE_ENDPOINT")

sm.delete_endpoint(EndpointName=endpoint)
logger.info(f"🧹 Deleted endpoint: {endpoint}")