import os
import logging
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from dotenv import load_dotenv
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env from project root
project_root = Path(__file__).resolve().parent.parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

# Load paths from .env
model_path = os.getenv("XGB_MODEL_LOCAL", "model.joblib")
data_path = os.getenv("XGB_VALIDATION_DATA", "01_data/sample_realistic_loan_approval_dataset_valid.csv")

# Validate file paths
if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Model file not found: {model_path}")
if not os.path.exists(data_path):
    raise FileNotFoundError(f"❌ Validation dataset not found: {data_path}")

# Load data and model
df = pd.read_csv(data_path)
model = joblib.load(model_path)

# Check required columns
if "label" not in df.columns:
    raise ValueError("❌ 'label' column is required in validation dataset.")

X_test = df.drop(columns=["CustomerID", "label", "predicted_label"], errors="ignore")
y_test = df["label"]
y_scores = model.predict_proba(X_test)[:, 1]

# Compute ROC
fpr, tpr, _ = roc_curve(y_test, y_scores)
roc_auc = auc(fpr, tpr)

# Plot
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend(loc="lower right")
plt.tight_layout()

output_file = "03_model_training/metrics/roc_curve.png"
plt.savefig(output_file)
logger.info(f"✅ ROC curve saved to: {output_file}")
