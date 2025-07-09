import os
import logging
import boto3
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

# -------------------------------
# Setup logging
# -------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------
# Load .env from project root
# -------------------------------
project_root = Path(__file__).resolve().parents[2]
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

# -------------------------------
# Config
# -------------------------------
endpoint_name = os.getenv("XGB_INFERENCE_ENDPOINT", "sagemaker-xgb-endpoint")
sample_file = os.getenv("XGB_SAMPLE_INPUT", "01_data/sample_realistic_loan_approval_dataset_valid.csv")

if not os.path.exists(sample_file):
    raise FileNotFoundError(f"❌ Input CSV not found: {sample_file}")

# -------------------------------
# Load and prepare data
# -------------------------------
df = pd.read_csv(sample_file)
logger.info(f"📊 Loaded input data: {sample_file} — shape: {df.shape}")

# Drop non-feature columns
excluded = ["CustomerID", "label", "predicted_label", "predicted_proba"]
feature_cols = [col for col in df.columns if col not in excluded]
input_df = df[feature_cols]

logger.info(f"📈 Input features shape: {input_df.shape}")
logger.info(f"🔍 Preview:\n{input_df.head(1)}")

# -------------------------------
# Invoke endpoint
# -------------------------------
runtime = boto3.client("sagemaker-runtime")

payload = ",".join(str(x) for x in input_df.iloc[0].values)
logger.info(f"📥 Invoking endpoint: {endpoint_name}")

response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType="text/csv",
    Body=payload
)

result = response["Body"].read().decode("utf-8").strip()
logger.info(f"✅ Prediction result: {result}")
