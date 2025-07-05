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

region = os.getenv("AWS_REGION")
feature_group_name = os.getenv("FEATURE_GROUP_NAME")

# Load dataset
df = pd.read_csv("01_data/processed/sample_realistic_loan_approval_dataset_ready.csv")
df["record_id"] = [f"{i}-{int(time.time())}" for i in range(len(df))]
df["event_time"] = pd.to_datetime("now", utc=True)

# Load feature group
session = Session()
fg = FeatureGroup(name=feature_group_name, sagemaker_session=session)

# Ingest records
logging.info(f"📤 Ingesting {len(df)} records to Feature Store...")
fg.ingest(data_frame=df, max_workers=3, wait=True)
logging.info("✅ Ingestion complete.")
