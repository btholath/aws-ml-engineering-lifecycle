#!/bin/bash

# ------------------------------
# Script: run_model_registry_pipeline.sh
# Purpose: Automate model registration, approval, and deployment
# ------------------------------

set -e  # Exit immediately on error
cd "$(dirname "$0")"  # Ensure we run from the script's directory

echo "🔁 Starting Model Registry Pipeline..."

# Step 1: Register the model
echo "📦 Registering the best training job model..."
python 01_register_model.py

# Step 2: Approve the latest model version
echo "✅ Approving the latest model version..."
python 02_approve_model.py

# Step 3: Deploy the approved model to an endpoint
echo "🚀 Deploying approved model to SageMaker endpoint..."
python 03_deploy_from_registry.py

echo "✅ Model Registry Pipeline completed successfully."
