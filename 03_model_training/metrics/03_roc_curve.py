import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import logging

# -----------------------------------------
# Setup logging
# -----------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------------------
# Load environment variables
# -----------------------------------------
project_root = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=project_root / ".env", override=True)

predictions_path = os.getenv("XGB_VALIDATION_DATA")
if not predictions_path or not os.path.exists(predictions_path):
    raise FileNotFoundError(f"❌ Validation data not found: {predictions_path}")
logger.info(f"📥 Loaded validation results: {predictions_path}")

# -----------------------------------------
# Load predictions
# -----------------------------------------
df = pd.read_csv(predictions_path)

if "label" not in df.columns or "predicted_proba" not in df.columns:
    raise ValueError("❌ Columns 'label' and 'predicted_proba' must exist in the dataset.")
logger.info("✅ Required columns found: 'label' and 'predicted_proba'")

# -----------------------------------------
# Calculate ROC curve and AUC
# -----------------------------------------
fpr, tpr, _ = roc_curve(df["label"], df["predicted_proba"])
roc_auc = auc(fpr, tpr)
logger.info(f"📊 AUC Score: {roc_auc:.4f}")

# -----------------------------------------
# Plot ROC curve
# -----------------------------------------
plt.figure()
plt.plot(fpr, tpr, label=f"ROC curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], "k--", label="Random guess")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Receiver Operating Characteristic (ROC) Curve")
plt.legend(loc="lower right")

# -----------------------------------------
# Save plot
# -----------------------------------------
output_path = project_root / "03_model_training" / "metrics" / "roc_curve.png"
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.tight_layout()
plt.savefig(output_path)
logger.info(f"✅ ROC curve saved: {output_path}")
