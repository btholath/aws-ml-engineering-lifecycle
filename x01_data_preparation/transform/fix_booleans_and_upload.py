# File: 01_data_preparation/transform/fix_booleans_and_upload.py

import pandas as pd
import os
import boto3
import logging
from dotenv import load_dotenv

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ENV
CSV_IN = os.getenv("XGB_READY_CSV", "./dataset/sample_loan_ready_for_xgboost.csv")
CSV_OUT = os.getenv("XGB_FIXED_CSV", "./dataset/sample_loan_fixed_for_xgboost.csv")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_KEY = os.getenv("XGB_FIXED_S3_KEY", "data/sample_loan_fixed_for_xgboost.csv")

# Load CSV
df = pd.read_csv(CSV_IN, header=None)

# 🔁 Convert all boolean columns to int
df = df.astype({col: 'int' for col in df.select_dtypes(include=['bool']).columns})

# ✅ Check: All numeric
if not df.dtypes.apply(lambda dt: pd.api.types.is_numeric_dtype(dt)).all():
    logging.error("❌ Not all columns are numeric.")
    exit(1)

# Save as numeric-only CSV
os.makedirs(os.path.dirname(CSV_OUT), exist_ok=True)
df.to_csv(CSV_OUT, index=False, header=False)
logging.info(f"✅ Fixed and saved: {CSV_OUT}")

# Upload to S3
boto3.client("s3").upload_file(CSV_OUT, S3_BUCKET, S3_KEY)
logging.info(f"📤 Uploaded to: s3://{S3_BUCKET}/{S3_KEY}")
