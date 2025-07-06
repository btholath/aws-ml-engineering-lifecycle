#!/bin/bash
set -e
set -o pipefail

echo "🚀 Starting ML environment setup..."

# Step 1: Infrastructure
cd 00_infrastructure
./create_all_resources.sh
cd ..

# Step 2: Data transformation
echo "🧹 [02] Running transformation steps..."
cd 02_data_preparation/transform
./run_all_transform_steps.sh  # Generates processed files
cd ../../

# Step 3: Data splitting (needs ready.csv from above step)
echo "📊 [01] Preparing raw data..."
cd 01_data
python scripts/02_split_validation_data.py
python scripts/03_transform_data.py
python scripts/04_upload_cleaned_to_s3.py
cd ..

# Step 4: Feature Store
echo "📊 [03] Creating and ingesting feature store groups..."
cd 02_data_preparation/feature_store
./run_all_feature_store_steps.sh
cd ../../

echo "✅ ML environment setup completed successfully."
