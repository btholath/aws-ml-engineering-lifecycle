#!/bin/bash
set -e

DATA_FILE="/workspaces/aws-ml-engineering-lifecycle/02_data_preparation/transform/01_data/processed/sample_realistic_loan_approval_dataset_ready.csv"

if [[ ! -f "$DATA_FILE" ]]; then
  echo "⚠️ $DATA_FILE not found. Running preprocessing first..."
  cd ../transform/
  ./run_all_transform_steps.sh
  cd ../feature_store/
fi

echo "🧠 Running Feature Store setup..."

echo "🔹 Step 1: Creating Feature Group..."
python 01_create_feature_group.py

echo "⏳ Waiting 30 seconds for Feature Group to initialize..."
sleep 30

echo "🔹 Step 2: Ingesting data into Feature Group..."
python 02_ingest_features.py

echo "✅ Feature Store setup and ingestion complete."
