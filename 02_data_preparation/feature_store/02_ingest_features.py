# 02_ingest_features.py
# Ingests the rows from your cleaned dataset into the Feature Store.
import os
import logging
import pandas as pd
import time
from dotenv import load_dotenv
from sagemaker.session import Session
from sagemaker.feature_store.feature_group import FeatureGroup

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

import time
import boto3

def wait_for_feature_group_active(name, timeout_secs=300, interval_secs=10):
    client = boto3.client("sagemaker")
    start = time.time()
    while time.time() - start < timeout_secs:
        status = client.describe_feature_group(FeatureGroupName=name)["FeatureGroupStatus"]
        if status == "Created":
            print(f"✅ Feature Group {name} is now ACTIVE.")
            return
        elif status == "CreateFailed":
            raise RuntimeError(f"❌ Feature Group {name} failed to create.")
        else:
            print(f"⏳ Waiting for Feature Group {name} to become ACTIVE... (current: {status})")
            time.sleep(interval_secs)
    raise TimeoutError(f"❌ Timeout: Feature Group {name} did not become ACTIVE in {timeout_secs} seconds.")


region = os.getenv("AWS_REGION")
feature_group_name = os.getenv("FEATURE_GROUP_NAME")
if not feature_group_name:
    logging.error("❌ FEATURE_GROUP_NAME is not set in the environment or .env file.")
    exit(1)

# Load dataset
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
input_csv = os.path.join(project_root, "01_data/processed/sample_realistic_loan_approval_dataset_ready.csv")
df = pd.read_csv("/workspaces/aws-ml-engineering-lifecycle/02_data_preparation/transform/01_data/processed/sample_realistic_loan_approval_dataset_ready.csv")
df["record_id"] = [f"{i}-{int(time.time())}" for i in range(len(df))]
df["event_time"] = pd.to_datetime("now", utc=True)
df["event_time"] = df["event_time"].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')  # Format for SageMaker


# Load feature group
session = Session()
fg = FeatureGroup(name=feature_group_name, sagemaker_session=session)

# Ingest records
logging.info(f"📤 Ingesting {len(df)} records to Feature Store...")
wait_for_feature_group_active("loan-approval-feature-group")
fg.ingest(data_frame=df, max_workers=3, wait=True)
logging.info("✅ Ingestion complete.")
