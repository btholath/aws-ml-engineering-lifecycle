"""
Your Dataset Structure
Column	        Type	        Notes
CustomerID	    String	        ❌ Drop it (non-numeric)
Age	            Numeric	        ✅ OK
Gender	        Categorical	    ❌ Encode
EducationLevel	Categorical	    ❌ Encode
Income	        Numeric	        ✅ OK
LoanApproved	Boolean	        ❌ Convert to 1/0, move to front

Drop CustomerID
Convert LoanApproved to 1 (TRUE) and 0 (FALSE)
One-hot encode Gender and EducationLevel
Move LoanApproved to the first column
Remove headers
Save to CSV
Upload to S3
"""

# File: 01_data_preparation/transform/prepare_loan_dataset_for_xgboost.py

import pandas as pd
import boto3
import os
import logging
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ENV vars
RAW_CSV = os.getenv("RAW_LOAN_CSV", "./dataset/sample_realistic_loan_approval_dataset.csv")
OUTPUT_CSV = os.getenv("XGB_READY_CSV", "./dataset/sample_loan_ready_for_xgboost.csv")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_KEY = os.getenv("XGB_READY_S3_KEY", "data/sample_loan_ready_for_xgboost.csv")

# Load CSV
df = pd.read_csv(RAW_CSV)

# Step 1: Drop non-numeric column
df.drop(columns=["CustomerID"], inplace=True)

# Step 2: Encode label TRUE/FALSE → 1/0
df["LoanApproved"] = df["LoanApproved"].astype(str).str.upper().map({"TRUE": 1, "FALSE": 0})

# Step 3: One-hot encode categorical features
df = pd.get_dummies(df, columns=["Gender", "EducationLevel"], drop_first=True)

# Step 4: Move label to first column
cols = list(df.columns)
cols.insert(0, cols.pop(cols.index("LoanApproved")))
df = df[cols]

# Step 5: Save as numeric-only CSV, no header or index
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False, header=False)
logging.info(f"✅ CSV ready for XGBoost: {OUTPUT_CSV}")

# Step 6: Upload to S3
s3 = boto3.client("s3")
s3.upload_file(OUTPUT_CSV, S3_BUCKET, S3_KEY)
logging.info(f"📤 Uploaded to S3: s3://{S3_BUCKET}/{S3_KEY}")
