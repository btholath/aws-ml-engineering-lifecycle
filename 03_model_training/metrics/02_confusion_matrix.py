import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
project_root = Path(__file__).resolve().parent.parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

# Load validation file path
validation_file = os.getenv("XGB_VALIDATION_CSV")  # e.g., 01_data/validation/sample_realistic_loan_approval_dataset_valid.csv
if not validation_file or not os.path.exists(validation_file):
    raise FileNotFoundError(f"❌ Validation dataset not found: {validation_file}")

# Load data
df = pd.read_csv(validation_file)

# Extract actual vs predicted labels
if "label" not in df.columns or "predicted_label" not in df.columns:
    raise ValueError("❌ Required columns 'label' and/or 'predicted_label' not found in dataset.")

y_true = df["label"]
y_pred = df["predicted_label"]

# Generate confusion matrix
cm = confusion_matrix(y_true, y_pred)
labels = ["Not Approved", "Approved"]

# Plot
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("03_model_training/metrics/confusion_matrix.png")
plt.show()

print("✅ Confusion matrix saved as: 03_model_training/metrics/confusion_matrix.png")
