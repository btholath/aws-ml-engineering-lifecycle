import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import confusion_matrix
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env", override=True)

# Load prediction data
predictions_path = os.getenv("XGB_VALIDATION_DATA")
if not predictions_path or not os.path.exists(predictions_path):
    raise FileNotFoundError(f"❌ Validation data not found: {predictions_path}")

df = pd.read_csv(predictions_path)
if "label" not in df.columns or "predicted_label" not in df.columns:
    raise ValueError("❌ Columns 'label' and 'predicted_label' must exist in the dataset.")

# Compute confusion matrix
cm = confusion_matrix(df["label"], df["predicted_label"])
labels = ["Not Approved", "Approved"]

# Plot
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

# Ensure output directory exists
output_path = Path("03_model_training/metrics/confusion_matrix.png")
output_path.parent.mkdir(parents=True, exist_ok=True)

# Save plot
plt.tight_layout()
plt.savefig(output_path)
print(f"✅ Confusion matrix saved: {output_path}")
