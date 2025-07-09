#!/bin/bash
set -e
set -o pipefail

echo "🧠 Step 1: Creating model artifact"
python model_packaging/01_create_model_artifact.py

echo "📦 Step 2: (Optional) Preparing container image"
python model_packaging/02_prepare_container_image.py || echo "ℹ️ Skipped: custom container not required"

echo "🚀 Step 3: Deploying real-time endpoint"
python real_time/01_deploy_endpoint.py

echo "🧪 Step 4: Invoking real-time endpoint"
python real_time/02_invoke_endpoint.py

echo "📈 Step 5: (Optional) Configuring autoscaling"
python real_time/03_config_autoscaling.py || echo "ℹ️ Skipped: autoscaling config optional"

echo "🌀 Step 6: Starting batch transform job"
python batch/01_batch_transform.py

echo "📥 Step 7: Fetching batch results"
python batch/02_fetch_results.py

echo "🧹 Step 8: Tearing down endpoint"
python real_time/04_teardown_endpoint.py

echo "✅ Inference pipeline completed successfully!"
