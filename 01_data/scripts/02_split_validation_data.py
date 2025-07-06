import os
import pandas as pd
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
import boto3
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env from project root
project_root = Path(__file__).resolve().parent.parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

# Read environment variables
s3_bucket = os.getenv("S3_BUCKET")
input_file = os.getenv("XGB_READY_CSV")
train_file = os.getenv("XGB_FIXED_CSV")
valid_file_local = "01_data/validation/sample_realistic_loan_approval_dataset_valid.csv"
valid_file_expected = "01_data/validation/sample_realistic_loan_approval_dataset_ready.csv"
s3_key = "data/validation/sample_realistic_loan_approval_dataset_ready.csv"

def main():
    # Validate input path
    if not input_file or not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found or not set: {os.path.abspath(input_file or '')}")

    df = pd.read_csv(input_file)
    train_df, valid_df = train_test_split(df, test_size=0.2, random_state=42)

    # Ensure output folders exist
    os.makedirs(os.path.dirname(train_file), exist_ok=True)
    os.makedirs(os.path.dirname(valid_file_local), exist_ok=True)

    # Save train and validation sets
    train_df.to_csv(train_file, index=False)
    valid_df.to_csv(valid_file_local, index=False)
    valid_df.to_csv(valid_file_expected, index=False)

    logger.info(f"✅ Saved training set to {train_file}")
    logger.info(f"✅ Saved validation set to {valid_file_local} and {valid_file_expected}")

    # Upload to S3
    if s3_bucket:
        try:
            s3 = boto3.client("s3")
            s3.upload_file(valid_file_expected, s3_bucket, s3_key)
            logger.info(f"📤 Uploaded validation set to s3://{s3_bucket}/{s3_key}")
        except Exception as e:
            logger.error(f"❌ Failed to upload to S3: {e}")
    else:
        logger.warning("⚠️ No S3_BUCKET found in .env. Skipping upload.")

if __name__ == "__main__":
    main()
