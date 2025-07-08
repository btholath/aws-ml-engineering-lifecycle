import os
import shap
import xgboost as xgb
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from dotenv import load_dotenv

# Load .env
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env", override=True)

# Paths
validation_data_path = os.getenv("XGB_VALIDATION_DATA")
model_path = "03_model_training/model/xgboost_model.json"

if not validation_data_path or not os.path.exists(validation_data_path):
    raise FileNotFoundError(f"❌ Validation data not found: {validation_data_path}")
if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Model file not found: {model_path}")

# Load validation data and model
df = pd.read_csv(validation_data_path)
X = df.drop(columns=["CustomerID", "label", "predicted_label", "predicted_proba"], errors="ignore")

booster = xgb.Booster()
booster.load_model(model_path)

# Create DMatrix
dmatrix = xgb.DMatrix(X)

# SHAP
explainer = shap.TreeExplainer(booster)
shap_values = explainer.shap_values(X)

# Ensure output directory exists
output_path = Path("03_model_training/metrics/shap_summary_plot.png")
output_path.parent.mkdir(parents=True, exist_ok=True)

# SHAP summary plot
plt.figure()
shap.summary_plot(shap_values, X, show=False)
plt.tight_layout()
plt.savefig(output_path)
print(f"✅ SHAP summary plot saved: {output_path}")
