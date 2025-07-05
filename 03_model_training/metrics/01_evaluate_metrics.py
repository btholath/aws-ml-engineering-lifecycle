"""
Evaluate model metrics (accuracy, precision, recall, etc.)
"""
import pandas as pd
from sklearn.metrics import classification_report
import joblib, logging

logging.basicConfig(level=logging.INFO)
df = pd.read_csv("test_data.csv")  # Replace with S3 or test dataset
X_test = df.drop(columns=["label"])
y_test = df["label"]

model = joblib.load("model.joblib")  # Local or download from S3
y_pred = model.predict(X_test)

logging.info("\n" + classification_report(y_test, y_pred))
