import os
import shap
import xgboost as xgb
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from dotenv import load_dotenv
import tarfile
import boto3

# Load environment
project_root = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=project_root / ".env", override=True)

validation_data_path = os.getenv("XGB_VALIDATION_DATA")
model_artifact = os.getenv("MODEL_ARTIFACT")
model_dir = project_root / "03_model_training/model"
tar_path = model_dir / "model.tar.gz"

# Download model from S3 and extract
if not model_artifact:
    raise ValueError("❌ MODEL_ARTIFACT not set in .env")

bucket, key = model_artifact.replace("s3://", "").split("/", 1)
model_dir.mkdir(parents=True, exist_ok=True)
boto3.client("s3").download_file(bucket, key, str(tar_path))

with tarfile.open(tar_path, "r:gz") as tar:
    tar.extractall(path=model_dir)

# Find a usable model file
booster = None
xgb_model_path = None
for file in model_dir.glob("*"):
    if file.suffix in [".json", ".bst", ".xgb", ".model", ""]:
        try:
            b = xgb.Booster()
            b.load_model(str(file))
            booster = b
            xgb_model_path = file
            print(f"✅ Loaded model from: {file}")
            break
        except Exception:
            continue

if not booster:
    print("❌ Could not load a valid XGBoost model. Exiting.")
    exit(1)

# Load validation data
if not validation_data_path or not os.path.exists(validation_data_path):
    raise FileNotFoundError(f"❌ Validation data not found: {validation_data_path}")

df = pd.read_csv(validation_data_path)
X = df.drop(columns=["CustomerID", "label", "predicted_label", "predicted_proba"], errors="ignore")

# Fallback if booster.feature_names is None
if not booster.feature_names:
    booster.feature_names = list(X.columns)
    print(f"⚠️ Booster had no feature names. Using from dataset: {booster.feature_names}")

# SHAP
explainer = shap.TreeExplainer(booster)
shap_values = explainer.shap_values(X)

# Save SHAP plot
output_path = project_root / "03_model_training/metrics/shap_summary_plot.png"
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.figure()
shap.summary_plot(shap_values, X, show=False)
plt.tight_layout()
plt.savefig(output_path)
print(f"✅ SHAP summary plot saved: {output_path}")
