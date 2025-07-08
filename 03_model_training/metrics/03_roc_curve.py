import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env", override=True)

# Load predictions
predictions_path = os.getenv("XGB_VALIDATION_DATA")
if not predictions_path or not os.path.exists(predictions_path):
    raise FileNotFoundError(f"❌ Validation data not found: {predictions_path}")

df = pd.read_csv(predictions_path)

if "label" not in df.columns or "predicted_proba" not in df.columns:
    raise ValueError("❌ Columns 'label' and 'predicted_proba' must exist in the dataset.")

# Calculate ROC curve
fpr, tpr, _ = roc_curve(df["label"], df["predicted_proba"])
roc_auc = auc(fpr, tpr)

# Plot ROC
plt.figure()
plt.plot(fpr, tpr, label=f"ROC curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], "k--", label="Random guess")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend(loc="lower right")

# Ensure output directory exists
output_path = Path("03_model_training/metrics/roc_curve.png")
output_path.parent.mkdir(parents=True, exist_ok=True)

# Save plot
plt.tight_layout()
plt.savefig(output_path)
print(f"✅ ROC curve saved: {output_path}")
