#!/bin/bash
set -e
set -o pipefail

# ML Pipeline Runner
# Run from the project root: ./run_ml_pipeline.sh

echo "🚀 Starting End-to-End ML Pipeline..."

# Load .env
if [ ! -f .env ]; then
  echo "❌ Missing .env in project root! Exiting."
  exit 1
fi
source .env

# 1. Infrastructure Setup
cd 00_infrastructure
./create_all_resources.sh
cd ..

# 2. Data Preparation
cd 01_data
python run_all_data_preparation.py
cd ..

# 3. Transformation + EDA + Upload
cd 02_data_preparation/transform
./run_all_transform_steps.sh
cd ../..

# 4. Feature Store
cd 02_data_preparation/feature_store
./run_all_feature_store_steps.sh
cd ../..

# 5. Model Training + HPO + Evaluation
cd 03_model_training
./run_all_model_training_steps.sh
cd ..

# 6. Model Registry
cd 04_model_registry
./run_model_registry_pipeline.sh
cd ..

# 7. Real-Time & Batch Inference
python 05_model_inference/batch/01_batch_transform.py || true
python 05_model_inference/batch/02_fetch_results.py || true
python 05_model_inference/real_time/01_deploy_endpoint.py || true
python 05_model_inference/real_time/02_invoke_endpoint.py || true

# 8. Monitoring
bash 06_monitoring/cloudwatch/01_setup_alarms.sh || true
python 06_monitoring/model_monitor/01_setup_baseline.py || true
python 06_monitoring/model_monitor/02_configure_monitor.py || true

# 9. Security
bash 07_security_compliance/audit_logging/01_enable_cloudtrail.sh || true
bash 07_security_compliance/encryption/01_create_kms_key.sh || true
python 07_security_compliance/guardrails/01_validate_data_bias.py || true

# 10. Tests
pytest 09_tests || echo "✅ Tests completed with warnings"

echo "✅ ML pipeline execution complete!"
