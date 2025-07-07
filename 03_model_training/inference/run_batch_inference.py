import os
import pandas as pd
from dotenv import load_dotenv
import boto3
import logging
from pathlib import Path

# ----------------------------
# Setup Logging
# ----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# Load .env from project root
# ----------------------------
project_root = Path(__file__).resolve().parents[2]
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

# ----------------------------
# Load required config
# ----------------------------
validation_file = os.getenv("VALIDATION_FILE", "01_data/validation/sample_realistic_loan_approval_dataset_ready.csv")
endpoint_name = os.getenv("XGB_INFERENCE_ENDPOINT")

# ----------------------------
# Batch inference function
# ----------------------------
def predict_batch(df_features):
    runtime = boto3.client("sagemaker-runtime")
    
    def invoke_endpoint(row):
        payload = ",".join(str(x) for x in row)
        response = runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType="text/csv",
            Body=payload
        )
        prediction = float(response["Body"].read().decode("utf-8"))
        return int(prediction >= 0.5)
    
    logger.info("🚀 Running batch inference...")
    return df_features.apply(invoke_endpoint, axis=1)

# ----------------------------
# Update .env utility
# ----------------------------
def update_env_variable(key: str, value: str):
    lines = []
    found = False
    if os.path.exists(dotenv_path):
        with open(dotenv_path, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
            break
    if not found:
        lines.append(f"{key}={value}\n")

    with open(dotenv_path, "w") as f:
        f.writelines(lines)
    logger.info(f"📌 Updated .env → {key}={value}")

# ----------------------------
# Main Logic
# ----------------------------
def main():
    if not endpoint_name:
        endpoint_name = input("❓ Enter your deployed XGBoost endpoint name: ").strip()
        update_env_variable("XGB_INFERENCE_ENDPOINT", endpoint_name)

    if not os.path.exists(validation_file):
        raise FileNotFoundError(f"❌ Validation file not found: {validation_file}")

    df = pd.read_csv(validation_file)

    # Drop rows missing label column
    if "label" not in df.columns:
        raise ValueError("❌ Dataset missing required 'label' column.")

    feature_cols = [col for col in df.columns if col not in ["CustomerID", "label"]]

    df["predicted_label"] = predict_batch(df[feature_cols])

    df.to_csv(validation_file, index=False)
    logger.info(f"✅ Inference complete. Predictions saved to: {validation_file}")

if __name__ == "__main__":
    main()
