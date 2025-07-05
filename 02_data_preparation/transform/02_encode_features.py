"""
Script: 02_encode_features.py
Purpose: One-hot encode categorical columns such as Gender and EducationLevel
"""

import os
import pandas as pd
import logging
from dotenv import load_dotenv
from sklearn.preprocessing import OneHotEncoder

# Load .env and configure logging
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# File paths
input_csv = "01_data/processed/sample_realistic_loan_approval_dataset_cleaned.csv"
output_csv = "01_data/processed/sample_realistic_loan_approval_dataset_encoded.csv"

# Ensure output folder exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

try:
    # Load dataset
    df = pd.read_csv(input_csv)
    logging.info(f"📥 Loaded cleaned dataset: {input_csv}")

    # Columns to encode
    cat_cols = ["Gender", "EducationLevel"]
    existing_cols = [col for col in cat_cols if col in df.columns]

    if not existing_cols:
        logging.warning("⚠️ No categorical columns found for encoding.")
        df.to_csv(output_csv, index=False)
        logging.info(f"📤 Dataset saved without encoding: {output_csv}")
    else:
        encoder = OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")
        encoded = encoder.fit_transform(df[existing_cols])

        # Sanitize column names for SageMaker Feature Store compatibility
        encoded_columns = encoder.get_feature_names_out(existing_cols)
        cleaned_columns = [
            col.replace("'", "").replace(" ", "_").replace("__", "_") for col in encoded_columns
        ]
        encoded_df = pd.DataFrame(encoded, columns=cleaned_columns)

        df = df.drop(columns=existing_cols)
        df = pd.concat([df.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)

        logging.info(f"✅ One-hot encoded columns: {existing_cols}")
        df.to_csv(output_csv, index=False)
        logging.info(f"📤 Encoded dataset saved: {output_csv}")

except Exception as e:
    logging.error(f"❌ Failed to encode dataset: {e}")
