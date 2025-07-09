import os
import logging
import boto3
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

project_root = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=project_root / ".env", override=True)

runtime = boto3.client("sagemaker-runtime", region_name=os.getenv("AWS_REGION"))
endpoint = os.getenv("XGB_INFERENCE_ENDPOINT")

df = pd.read_csv("sample.csv")
logger.info(f"📥 Invoking endpoint: {endpoint}")

for i, row in df.iterrows():
    payload = ",".join(map(str, row.values))
    response = runtime.invoke_endpoint(
        EndpointName=endpoint,
        ContentType="text/csv",
        Body=payload
    )
    prediction = response["Body"].read().decode("utf-8")
    logger.info(f"Row {i}: {prediction}")