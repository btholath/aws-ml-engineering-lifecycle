# train.py
import os
import pandas as pd
import xgboost as xgb

if __name__ == "__main__":
    # Paths
    input_dir = os.environ.get("SM_CHANNEL_TRAIN", "/opt/ml/input/data/train")
    model_dir = os.environ.get("SM_MODEL_DIR", "/opt/ml/model")

    # Load training data
    df = pd.read_csv(os.path.join(input_dir, "sample_realistic_loan_approval_dataset_ready.csv"))

    # Drop non-numeric ID column
    if "CustomerID" in df.columns:
        df = df.drop(columns=["CustomerID"])

    # Separate features and label
    X = df.drop(columns=["label"])
    y = df["label"]

    # Train model
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    model.fit(X, y)

    # Save model
    model.save_model(os.path.join(model_dir, "xgboost-model.json"))
