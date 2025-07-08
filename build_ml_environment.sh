#!/bin/bash
set -e
set -o pipefail

# --------------------------------------
# Full ML Pipeline Build Script
# --------------------------------------

REGION=$(aws configure get region)
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
echo "🌍 Region: $REGION | AWS Account: $ACCOUNT_ID"

# Load environment
ENV_FILE=".env"
if [[ -f "$ENV_FILE" ]]; then
  echo "✅ Found .env file"
  source "$ENV_FILE"
else
  echo "❌ .env file not found. Exiting."
  exit 1
fi

# Ensure MODEL_PACKAGE_GROUP is set in .env
MODEL_PACKAGE_GROUP_KEY="MODEL_PACKAGE_GROUP"
DEFAULT_MODEL_PACKAGE_GROUP="loanapprovalmodelgroup"

if grep -q "^$MODEL_PACKAGE_GROUP_KEY=" "$ENV_FILE"; then
  echo "✅ MODEL_PACKAGE_GROUP already defined in .env"
else
  echo "📌 Adding $MODEL_PACKAGE_GROUP_KEY=$DEFAULT_MODEL_PACKAGE_GROUP to $ENV_FILE"
  echo "$MODEL_PACKAGE_GROUP_KEY=$DEFAULT_MODEL_PACKAGE_GROUP" >> "$ENV_FILE"
  export MODEL_PACKAGE_GROUP=$DEFAULT_MODEL_PACKAGE_GROUP
fi

# Print critical .env variables
echo "🔍 Loaded .env variables:"
grep -E '^(SAGEMAKER_ROLE_ARN|S3_BUCKET|AWS_REGION|BEST_TRAINING_JOB_NAME|MODEL_PACKAGE_GROUP)=' "$ENV_FILE"

# --------------------------------------
# Step 0: Infrastructure provisioning
# --------------------------------------
echo "🔧 Step 0: Creating infrastructure resources..."
cd 00_infrastructure
./create_all_resources.sh

# Auto-create Model Package Group if not exists
echo "📦 Ensuring Model Package Group '$MODEL_PACKAGE_GROUP' exists..."
aws sagemaker describe-model-package-group \
  --model-package-group-name "$MODEL_PACKAGE_GROUP" \
  --region "$REGION" >/dev/null 2>&1 || {
    echo "📦 Creating Model Package Group: $MODEL_PACKAGE_GROUP"
    aws sagemaker create-model-package-group \
      --model-package-group-name "$MODEL_PACKAGE_GROUP" \
      --model-package-group-description "Loan approval model registry" \
      --region "$REGION"
}
cd ..

# --------------------------------------
# Step 1: Data preparation
# --------------------------------------
echo "📦 Step 1: Preparing data..."
python 01_data/run_all_data_preparation.py

# --------------------------------------
# Step 2: Transformation + EDA + Feature Store
# --------------------------------------
echo "🧹 Step 2: Running data transformation & EDA..."
cd 02_data_preparation/transform
./run_all_transform_steps.sh
cd ../feature_store
./run_all_feature_store_steps.sh
cd ../../

# --------------------------------------
# Step 3: Training + HPO
# --------------------------------------
echo "🧠 Step 3: Model training & HPO..."
cd 03_model_training
./run_all_model_training_steps.sh
cd ..

# --------------------------------------
# Step 4: Register & Deploy
# --------------------------------------
echo "📋 Step 4: Model registration & endpoint deployment..."
cd 04_model_registry
./run_model_registry_pipeline.sh
cd ..

# --------------------------------------
# Step 5: Batch inference
# --------------------------------------
echo "🔮 Step 5: Running batch inference on validation set..."
python 03_model_training/inference/run_batch_inference.py

# --------------------------------------
# Step 6: Evaluation metrics
# --------------------------------------
echo "📊 Step 6: Generating evaluation reports..."
python 03_model_training/metrics/01_evaluate_metrics.py
python 03_model_training/metrics/02_confusion_matrix.py
python 03_model_training/metrics/03_roc_curve.py
python 03_model_training/metrics/04_shap_explainer.py

echo "✅ Full ML pipeline executed successfully!"
