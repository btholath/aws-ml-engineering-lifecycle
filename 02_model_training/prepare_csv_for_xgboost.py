# File: 01_data_preparation/transform/prepare_csv_for_xgboost.py

import pandas as pd
import boto3
import os
import logging
from dotenv import load_dotenv

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ENV VARS
INPUT_CSV = os.getenv("RAW_LOAN_CSV", "./dataset/sample_realistic_loan_approval_dataset.csv")
OUTPUT_CSV = os.getenv("XGB_READY_CSV", "./dataset/sample_loan_ready_for_xgboost.csv")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_KEY = os.getenv("XGB_READY_S3_KEY", "data/sample_loan_ready_for_xgboost.csv")

# Load CSV
df = pd.read_csv(INPUT_CSV)

# Encode target column
df["LoanApproved"] = df["LoanApproved"].astype(str).str.upper().map({"TRUE": 1, "FALSE": 0})

# One-hot encode categorical features
categorical_cols = ["Gender", "EducationLevel"]
df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Drop non-numeric columns (e.g., CustomerID)
df.drop(columns=["CustomerID"], inplace=True)

# Move label column to front
cols = list(df.columns)
cols.insert(0, cols.pop(cols.index("LoanApproved")))
df = df[cols]

# Save to file (no header or index)
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False, header=False)
logging.info(f"✅ Saved preprocessed CSV to: {OUTPUT_CSV}")

# Upload to S3
s3 = boto3.client("s3")
s3.upload_file(OUTPUT_CSV, S3_BUCKET, S3_KEY)
logging.info(f"📤 Uploaded to s3://{S3_BUCKET}/{S3_KEY}")
