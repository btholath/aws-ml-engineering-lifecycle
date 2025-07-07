#!/bin/bash
set -e
set -o pipefail

# --------------------------------------
# Full ML Pipeline Build Script
# --------------------------------------

REGION=$(aws configure get region)
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
echo "🌍 Region: $REGION | AWS Account: $ACCOUNT_ID"

echo "🔧 Step 0: Creating infrastructure resources..."
cd 00_infrastructure
./create_all_resources.sh
cd ..

echo "📦 Step 1: Preparing data..."
python 01_data/run_all_data_preparation.py

echo "🧹 Step 2: Running data transformation & EDA..."
cd 02_data_preparation/transform
./run_all_transform_steps.sh
cd ../feature_store
./run_all_feature_store_steps.sh
cd ../../

echo "🧠 Step 3: Model training & HPO..."
cd 03_model_training
./run_all_model_training_steps.sh
cd ..

echo "📋 Step 4: Model registration & endpoint deployment..."
cd 04_model_registry
./run_model_registry_pipeline.sh
cd ..

echo "🔮 Step 5: Running batch inference on validation set..."
python 03_model_training/inference/run_batch_inference.py

echo "📊 Step 6: Generating evaluation reports..."
python 03_model_training/metrics/01_evaluate_metrics.py
python 03_model_training/metrics/02_confusion_matrix.py
python 03_model_training/metrics/03_roc_curve.py
python 03_model_training/metrics/04_shap_explainer.py

echo "✅ Full ML pipeline executed successfully!"
