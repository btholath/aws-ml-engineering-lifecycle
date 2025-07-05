"""
Script: 04_validate_dataset.py
Purpose: Ensure that the final training dataset is valid before training:
- All columns are numeric
- No missing values
- Target column 'label' is binary
"""

import os
import logging
import pandas as pd
from dotenv import load_dotenv

# Load environment
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# File path
dataset_path = "01_data/processed/sample_realistic_loan_approval_dataset_ready.csv"

try:
    df = pd.read_csv(dataset_path)
    logging.info("📄 Dataset loaded for validation.")

    # Check for missing values
    null_counts = df.isnull().sum()
    total_nulls = null_counts.sum()
    if total_nulls > 0:
        logging.warning("⚠️ Dataset contains missing values:")
        logging.warning(null_counts[null_counts > 0])
    else:
        logging.info("✅ No missing values found.")

    # Check data types
    non_numeric = df.select_dtypes(exclude=["number"]).columns.tolist()
    if non_numeric:
        logging.warning(f"⚠️ Non-numeric columns found: {non_numeric}")
    else:
        logging.info("✅ All columns are numeric.")

    # Check target column
    if "label" in df.columns:
        unique_vals = df["label"].dropna().unique()
        if set(unique_vals).issubset({0, 1}):
            logging.info("✅ Target column 'label' is binary and valid.")
        else:
            logging.error(f"❌ 'label' column contains unexpected values: {unique_vals}")
    else:
        logging.error("❌ Missing required 'label' column.")

except Exception as e:
    logging.error(f"❌ Validation failed: {e}")