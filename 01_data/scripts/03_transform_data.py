"""
This script will:
Load the training CSV
Apply transformations:
Impute missing values (e.g., median for Age)
One-hot encode Gender, EducationLevel
Rename LoanApproved → label
Save cleaned data to:
01_data/processed/cleaned_loan_data.csv

Purpose: Transform training data for XGBoost model
"""
import os
import logging
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Paths
input_csv = "01_data/processed/sample_realistic_loan_approval_dataset_train.csv"
output_csv = "01_data/processed/sample_realistic_loan_approval_dataset_cleaned.csv"

# Ensure output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

try:
    # Load data
    df = pd.read_csv(input_csv)
    logging.info("📥 Loaded training dataset")

    # Impute missing Age with median
    if 'Age' in df.columns:
        age_imputer = SimpleImputer(strategy='median')
        df['Age'] = age_imputer.fit_transform(df[['Age']])
        logging.info("🛠️  Imputed missing Age with median")

    # Drop rows with missing target
    df = df.dropna(subset=['LoanApproved'])

    # Convert target to binary: TRUE → 1, FALSE → 0
    df['label'] = df['LoanApproved'].astype(str).str.upper().map({'TRUE': 1, 'FALSE': 0})
    df = df.drop(columns=['LoanApproved'])

    # One-hot encode Gender and EducationLevel
    categorical_cols = ['Gender', 'EducationLevel']
    encoder = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')
    encoded = encoder.fit_transform(df[categorical_cols])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(categorical_cols))
    df = df.drop(columns=categorical_cols)
    df_encoded = pd.concat([df.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)

    # Save transformed data
    df_encoded.to_csv(output_csv, index=False)
    logging.info(f"✅ Transformed data saved to: {output_csv}")

except Exception as e:
    logging.error(f"❌ Transformation failed: {e}")