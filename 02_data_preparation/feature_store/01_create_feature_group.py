"""
Script: 01_create_feature_group.py
Purpose: Creates a SageMaker Feature Group for loan approval data (if not already existing)

cleanup
aws sagemaker delete-feature-group --feature-group-name loan-approval-feature-group --region us-east-1

"""

import os
import time
import logging
import pandas as pd
import boto3
import botocore
from dotenv import load_dotenv
from sagemaker.feature_store.feature_group import FeatureGroup
from sagemaker.session import Session

# Load .env config
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Config
region = os.getenv("AWS_REGION", "us-east-1")
bucket = os.getenv("S3_BUCKET")
sagemaker_role_arn = os.getenv("SAGEMAKER_ROLE_ARN")
feature_group_name = os.getenv("FEATURE_GROUP_NAME", "loan-approval-feature-group")
input_csv = "/workspaces/aws-ml-engineering-lifecycle/02_data_preparation/transform/01_data/processed/sample_realistic_loan_approval_dataset_ready.csv"
s3_uri = os.getenv("S3_FEATURE_STORE_URI", f"s3://{bucket}/feature-store/")

# AWS clients
sagemaker_boto = boto3.client("sagemaker", region_name=region)
session = Session(boto_session=boto3.Session(region_name=region))
fg = FeatureGroup(name=feature_group_name, sagemaker_session=session)

try:
    # Load dataset
    df = pd.read_csv(input_csv)
    logging.info(f"📥 Loaded dataset: {input_csv}")

    # Add ID and event_time columns
    df["record_id"] = [f"{i}-{int(time.time())}" for i in range(len(df))]
    df["event_time"] = pd.to_datetime("now", utc=True)

    # Convert event_time to ISO string to satisfy Feature Store constraint
    df["event_time"] = df["event_time"].astype(str)

    # Check if feature group exists
    try:
        sagemaker_boto.describe_feature_group(FeatureGroupName=feature_group_name)
        logging.info(f"⚠️ Feature Group '{feature_group_name}' already exists. Skipping creation.")
    except botocore.exceptions.ClientError as e:
        if "ResourceNotFound" in str(e):
            logging.info("✅ Creating Feature Group...")

            # Load feature definitions (strip invalid chars)
            sanitized_columns = {col: col.replace("'", "").replace(" ", "_") for col in df.columns}
            df.rename(columns=sanitized_columns, inplace=True)

            fg.load_feature_definitions(data_frame=df)
            fg.create(
                s3_uri=s3_uri,
                record_identifier_name="record_id",
                event_time_feature_name="event_time",
                role_arn=sagemaker_role_arn,
                enable_online_store=False,
            )
            logging.info(f"🧠 Feature Group created: {feature_group_name}")
        else:
            raise

except Exception as ex:
    logging.error(f"❌ Failed to create Feature Group: {ex}")
