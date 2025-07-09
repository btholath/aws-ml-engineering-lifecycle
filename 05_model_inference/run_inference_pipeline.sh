#!/bin/bash
set -e

# Navigate to script directory to ensure relative paths work
cd "$(dirname "$0")"

echo "🚀 Step 1: Creating model artifact..."
python model_packaging/01_create_model_artifact.py

echo "📦 Step 2: Preparing container image..."
python model_packaging/02_prepare_container_image.py

echo "🌐 Step 3: Deploying real-time endpoint..."
python real_time/01_deploy_endpoint.py

echo "🧪 Step 4: Invoking endpoint with sample input..."
python real_time/02_invoke_endpoint.py

echo "📊 Step 5: Configuring endpoint autoscaling..."
python real_time/03_config_autoscaling.py

echo "📦 Step 6: Running batch transform..."
python batch/01_batch_transform.py

echo "📥 Step 7: Fetching batch inference results..."
python batch/02_fetch_results.py

echo "✅ Inference pipeline completed successfully."
