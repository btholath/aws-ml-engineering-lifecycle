import os
import shap
import xgboost as xgb
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from dotenv import load_dotenv
import tarfile
import boto3

# -----------------------------
# Load .env variables
# -----------------------------
project_root = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=project_root / ".env", override=True)

# -----------------------------
# Configs
# -----------------------------
validation_data_path = os.getenv("XGB_VALIDATION_DATA")
model_artifact = os.getenv("MODEL_ARTIFACT")  # s3://.../model.tar.gz
local_model_dir = project_root / "03_model_training/model"
local_model_path = local_model_dir / "xgboost_model.json"
downloaded_tar_path = local_model_dir / "model.tar.gz"

# -----------------------------
# Check validation data
# -----------------------------
if not validation_data_path or not os.path.exists(validation_data_path):
    raise FileNotFoundError(f"❌ Validation data not found: {validation_data_path}")

# -----------------------------
# Download and extract model
# -----------------------------
if not local_model_path.exists():
    print(f"📦 Model file not found locally. Downloading from S3: {model_artifact}")
    local_model_dir.mkdir(parents=True, exist_ok=True)

    s3 = boto3.client("s3")
    parsed = model_artifact.replace("s3://", "").split("/", 1)
    bucket, key = parsed[0], parsed[1]

    # Download model.tar.gz
    s3.download_file(bucket, key, str(downloaded_tar_path))

    # Extract xgboost-model and rename
    with tarfile.open(downloaded_tar_path, "r:gz") as tar:
        tar.extractall(path=local_model_dir)
        extracted_model = local_model_dir / "xgboost-model"
        if not extracted_model.exists():
            raise FileNotFoundError("❌ Extracted xgboost-model not found in artifact.")
        extracted_model.rename(local_model_path)
    print(f"✅ Model extracted and saved as: {local_model_path}")

# -----------------------------
# Load data and model
# -----------------------------
df = pd.read_csv(validation_data_path)
X = df.drop(columns=["CustomerID", "label", "predicted_label", "predicted_proba"], errors="ignore")

booster = xgb.Booster()
booster.load_model(str(local_model_path))

# -----------------------------
# SHAP explainability
# -----------------------------
dmatrix = xgb.DMatrix(X)
explainer = shap.TreeExplainer(booster)
shap_values = explainer.shap_values(X)

# Save plot
output_path = project_root / "03_model_training/metrics/shap_summary_plot.png"
output_path.parent.mkdir(parents=True, exist_ok=True)

plt.figure()
shap.summary_plot(shap_values, X, show=False)
plt.tight_layout()
plt.savefig(output_path)
print(f"✅ SHAP summary plot saved: {output_path}")
