#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status
set -o pipefail

echo "🚀 Starting ML environment setup..."

# Step 1: Infrastructure setup
echo "📦 [00] Creating AWS infrastructure..."
cd 00_infrastructure
./create_all_resources.sh   # Sets up IAM role, security group, S3, and Studio domain
cd ..

# Step 2: Data preparation
echo "📊 [01] Preparing raw data..."
cd 01_data

# Check if .env exists at root
if [ ! -f ../.env ]; then
  echo "❌ .env file not found in project root!"
  exit 1
fi

# Run data scripts
echo "📄 Generating + transforming data..."
# Skip 01_generate_data.py if it doesn't exist
if [ -f scripts/01_generate_data.py ]; then
  python scripts/01_generate_data.py
else
  echo "⚠️  Skipping 01_generate_data.py (not found)"
fi

python scripts/02_split_validation_data.py
python scripts/03_transform_data.py

# Upload cleaned data to S3
echo "☁️ Uploading cleaned data to S3..."
python scripts/04_upload_cleaned_to_s3.py

cd ../02_data_preparation/transform

echo "🧹 [02] Running transformation steps..."
./run_all_transform_steps.sh  # 01 to 05 steps

cd ../feature_store
echo "📊 [03] Creating and ingesting feature store groups..."
./run_all_feature_store_steps.sh

echo "✅ ML environment setup completed successfully."
