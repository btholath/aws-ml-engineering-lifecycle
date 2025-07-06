import os
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
project_root = Path(__file__).resolve().parent.parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

# Paths
validation_file = os.getenv("XGB_VALIDATION_CSV")


if not os.path.exists(validation_file):
    raise FileNotFoundError(f"❌ Validation dataset not found: {validation_file}")

# Load validation data
df = pd.read_csv(validation_file)

# Basic assumptions
y_true = df["label"]

# For now, generate dummy predictions (you can later load real model and predict)
# Replace this block with actual model inference if needed
import numpy as np
y_pred = np.random.choice([0, 1], size=len(y_true), p=[0.5, 0.5])

# Print metrics
print("\n📊 Classification Report:")
print(classification_report(y_true, y_pred, digits=4))

print("🧾 Confusion Matrix:")
print(confusion_matrix(y_true, y_pred))
