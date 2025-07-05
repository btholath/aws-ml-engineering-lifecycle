#!/bin/bash
set -e

echo "🚀 Running all data transformation steps..."

echo "🔹 Step 1: Cleaning raw data..."
python 01_clean_data.py

echo "🔹 Step 2: Encoding categorical features..."
python 02_encode_features.py

echo "🔹 Step 3: Fixing booleans and uploading to S3..."
python 03_fix_booleans_and_upload.py

echo "🔹 Step 4: Validating final dataset..."
python 04_validate_dataset.py

echo "🔹 Step 5: Generating statistics and histograms..."
python 05_generate_statistics.py

echo "✅ All data transformation steps completed successfully!"
