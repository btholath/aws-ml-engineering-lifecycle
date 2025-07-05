"""
02_split_validation_data.py to split raw data into training and validation sets.'

Loads: 01_data/raw/sample_realistic_loan_approval_dataset.csv

Splits into:
01_data/processed/sample_realistic_loan_approval_dataset_train.csv
01_data/validation/sample_realistic_loan_approval_dataset_valid.csv
Uses train_test_split from scikit-learn
"""
import os
import logging
import pandas as pd
from sklearn.model_selection import train_test_split

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Define input/output paths
raw_data_path = "01_data/raw/sample_realistic_loan_approval_dataset.csv"
train_output_path = "01_data/processed/sample_realistic_loan_approval_dataset_train.csv"
valid_output_path = "01_data/validation/sample_realistic_loan_approval_dataset_valid.csv"

# Create output folders if not exist
os.makedirs(os.path.dirname(train_output_path), exist_ok=True)
os.makedirs(os.path.dirname(valid_output_path), exist_ok=True)

try:
    # Load the raw dataset
    df = pd.read_csv(raw_data_path)

    # Split into train and validation
    train_df, valid_df = train_test_split(df, test_size=0.2, random_state=42)

    # Save the splits
    train_df.to_csv(train_output_path, index=False)
    valid_df.to_csv(valid_output_path, index=False)

    logging.info(f"✅ Training data saved to: {train_output_path}")
    logging.info(f"✅ Validation data saved to: {valid_output_path}")

except Exception as e:
    logging.error(f"❌ Failed to split dataset: {e}")
