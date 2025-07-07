"""
SHAP explanation of XGBoost model.
"""

import os
import logging
import pandas as pd
import shap
import joblib
import matplotlib.pyplot as plt
from pathlib import Path
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load project-level .env
project_root = Path(__file__).resolve().parent.parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

# Load paths from .env
model_path = os.getenv("XGB_MODEL_LOCAL", "model.joblib")
data_path = os.getenv("XGB_VALIDATION_DATA", "01_data/sample_realistic_loan_approval_dataset_valid.csv")

# Check if paths exist
if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Model file not found: {model_path}")
if not os.path.exists(data_path):
    raise FileNotFoundError(f"❌ Validation dataset not found: {data_path}")

# Load model and dataset
model = joblib.load(model_path)
df = pd.read_csv(data_path)

# Validate expected columns
if "label" not in df.columns or "predicted_label" not in df.columns:
    raise ValueError("❌ Required columns 'label' and/or 'predicted_label' not found in dataset.")

# Drop non-feature columns
X = df.drop(columns=["CustomerID", "label", "predicted_label"], errors="ignore")

logger.info("🧠 Explaining model predictions with SHAP...")
explainer = shap.Explainer(model)
shap_values = explainer(X)

# Save summary plot
shap.summary_plot(shap_values, X, show=False)
plt.title("SHAP Summary Plot")
plt.tight_layout()
output_file = "03_model_training/metrics/shap_summary.png"
plt.savefig(output_file)
logger.info(f"✅ SHAP summary plot saved to: {output_file}")
