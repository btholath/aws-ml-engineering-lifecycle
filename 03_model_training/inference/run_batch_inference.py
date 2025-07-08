import os
import logging
import boto3
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import time
from sklearn.model_selection import train_test_split

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env from project root
project_root = Path(__file__).resolve().parent.parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

# Read environment variables
input_file = os.getenv("XGB_READY_CSV", "01_data/processed/sample_realistic_loan_approval_dataset_ready.csv")
validation_output = os.getenv("XGB_VALIDATION_DATA", "01_data/sample_realistic_loan_approval_dataset_valid.csv")
endpoint_name = os.getenv("XGB_INFERENCE_ENDPOINT")
s3_bucket = os.getenv("S3_BUCKET")

# For saving .env updates
def update_env_variable(key: str, value: str, env_file=".env"):
    env_path = project_root / env_file
    lines = []
    if env_path.exists():
        lines = env_path.read_text().splitlines()

    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            updated = True
            break
    if not updated:
        lines.append(f"{key}={value}")

    env_path.write_text("\n".join(lines) + "\n")
    logger.info(f"📌 Updated .env → {key}={value}")


# Perform batch inference
def predict_batch(df_features, endpoint_name: str):
    runtime = boto3.client("sagemaker-runtime")

    def invoke_endpoint(row):
        payload = ",".join(str(x) for x in row)
        response = runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType="text/csv",
            Body=payload
        )
        prediction = float(response['Body'].read().decode("utf-8"))
        return int(prediction >= 0.5)

    logger.info("🚀 Running batch inference on validation data...")
    return df_features.apply(invoke_endpoint, axis=1)

def wait_until_endpoint_in_service(endpoint_name, timeout=600):
    sm = boto3.client("sagemaker", region_name=os.getenv("AWS_REGION", "us-east-1"))
    start = time.time()
    while time.time() - start < timeout:
        status = sm.describe_endpoint(EndpointName=endpoint_name)["EndpointStatus"]
        if status == "InService":
            return True
        elif status == "Failed":
            raise RuntimeError(f"Endpoint {endpoint_name} creation failed.")
        time.sleep(10)
    raise TimeoutError(f"Timed out waiting for endpoint: {endpoint_name}")


def main():
    if not endpoint_name:
        raise ValueError("❌ XGB_INFERENCE_ENDPOINT is not set in .env")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"❌ Input dataset not found: {input_file}")

    df = pd.read_csv(input_file)
    train_df, valid_df = train_test_split(df, test_size=0.2, random_state=42)

    # Save split files (optional)
    os.makedirs(os.path.dirname(validation_output), exist_ok=True)

    # Select only feature columns
    feature_cols = [c for c in valid_df.columns if c not in ["CustomerID", "label"]]
    valid_df["predicted_label"] = predict_batch(valid_df[feature_cols], endpoint_name)

    # Save locally
    valid_df.to_csv(validation_output, index=False)
    logger.info(f"✅ Saved validation results with predictions: {validation_output}")

    # Upload to S3 if bucket is configured
    if s3_bucket:
        s3_key = "data/inference/sample_loan_predictions.csv"
        try:
            boto3.client("s3").upload_file(validation_output, s3_bucket, s3_key)
            logger.info(f"📤 Uploaded to S3: s3://{s3_bucket}/{s3_key}")
        except Exception as e:
            logger.error(f"❌ Upload failed: {e}")

    # Update .env (redundant if already set)
    update_env_variable("XGB_VALIDATION_DATA", validation_output)

if __name__ == "__main__":
    wait_until_endpoint_in_service(endpoint_name)
    main()
