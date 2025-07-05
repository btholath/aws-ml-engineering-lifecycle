"""
Script: 01_clean_data.py
Purpose: Clean the raw loan dataset by handling missing values and dropping unusable records.
"""

import os
import pandas as pd
import logging
from dotenv import load_dotenv
from sklearn.impute import SimpleImputer

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# File paths
raw_csv = os.getenv("RAW_LOAN_CSV", "/workspaces/aws-ml-engineering-lifecycle/01_data/raw/sample_realistic_loan_approval_dataset.csv")
output_csv = "01_data/processed/sample_realistic_loan_approval_dataset_cleaned.csv"

# Create output directory if needed
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

try:
    df = pd.read_csv(raw_csv)
    logging.info(f"📥 Loaded raw dataset: {raw_csv}")

    # Impute missing Age values with median
    if "Age" in df.columns:
        age_imputer = SimpleImputer(strategy="median")
        df["Age"] = age_imputer.fit_transform(df[["Age"]])
        logging.info("✅ Imputed missing 'Age' with median")

    # Drop rows with missing LoanApproved (target)
    if "LoanApproved" in df.columns:
        before = len(df)
        df = df.dropna(subset=["LoanApproved"])
        after = len(df)
        logging.info(f"🧹 Dropped rows with missing LoanApproved: {before - after} rows removed")

    # Save cleaned dataset
    df.to_csv(output_csv, index=False)
    logging.info(f"✅ Cleaned dataset saved: {output_csv}")

except Exception as e:
    logging.error(f"❌ Failed to clean dataset: {e}")