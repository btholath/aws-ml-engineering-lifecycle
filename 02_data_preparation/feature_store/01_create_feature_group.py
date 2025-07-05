"""
# 01_create_feature_group.py
Creates a Feature Group in offline and online store.

✅ Tasks:
Define schema

Enable offline + online store

Register FeatureGroup in SageMaker
"""
import os
import logging
import pandas as pd
import boto3
import time
from dotenv import load_dotenv
from sagemaker.feature_store.feature_group import FeatureGroup
from sagemaker.session import Session

# Load config
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

region = os.getenv("AWS_REGION")
bucket = os.getenv("S3_BUCKET")
role = os.getenv("SAGEMAKER_ROLE_ARN")
feature_group_name = os.getenv("FEATURE_GROUP_NAME", "loan-approval-feature-group")
s3_uri = os.getenv("S3_FEATURE_STORE_URI", f"s3://{bucket}/feature-store/")

df = pd.read_csv("01_data/processed/sample_realistic_loan_approval_dataset_ready.csv")

# Add record ID + event time
df["record_id"] = [f"{i}-{int(time.time())}" for i in range(len(df))]
df["event_time"] = pd.to_datetime("now", utc=True)

# Feature group client
session = Session(boto3.Session(region_name=region))
fg = FeatureGroup(name=feature_group_name, sagemaker_session=session)

try:
    fg.delete()
except Exception:
    pass  # FG may not exist yet

logging.info("✅ Creating Feature Group...")
fg.load_feature_definitions(data_frame=df)

fg.create(
    s3_uri=s3_uri,
    record_identifier_name="record_id",
    event_time_feature_name="event_time",
    role_arn=role,
    enable_online_store=True
)

logging.info(f"🧠 Feature Group created: {feature_group_name}")
