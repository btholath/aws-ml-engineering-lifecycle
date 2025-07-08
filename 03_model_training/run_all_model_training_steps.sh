#!/bin/bash
set -e
set -o pipefail

# Dry-run flag (set to 1 to simulate, 0 to run for real)
dry_run=0

# Load environment variables from root .env
source ../.env

# Create logs directory with timestamp
log_dir="../03_model_training/logs"
mkdir -p "$log_dir"
timestamp=$(date "+%Y%m%d-%H%M%S")
train_log="$log_dir/train-$timestamp.log"
echo "📁 Logging to $train_log"

if [[ "$dry_run" -eq 1 ]]; then
  echo "🧪 DRY RUN: Skipping execution."
  exit 0
fi

echo "🚀 Starting model training pipeline..."

# Step 1: Train XGBoost
echo "🧠 Step 1: Training XGBoost Model" | tee -a "$train_log"
python 01_train_xgboost.py 2>&1 | tee -a "$train_log"

# Step 2: Monitor training
echo "🔍 Step 2: Monitoring Training Job" | tee -a "$train_log"
python 02_monitor_training.py 2>&1 | tee -a "$train_log"

# Step 3: Run HPO
echo "📈 Step 3: Running Hyperparameter Optimization (HPO)" | tee -a "$train_log"
python hpo/01_run_hpo_job.py 2>&1 | tee -a "$train_log"

# Step 4: Visualize HPO Results
echo "🖼️ Step 4: Visualizing HPO Results" | tee -a "$train_log"
python hpo/02_visualize_hpo_results.py 2>&1 | tee -a "$train_log"

# Step 5: Decide model artifact source (HPO or fallback base training)
best_hpo_job=$BEST_TRAINING_JOB_NAME
s3_bucket=$S3_BUCKET
artifact_path="output/$best_hpo_job/output/model.tar.gz"

if aws s3 ls s3://$s3_bucket/$artifact_path >/dev/null 2>&1; then
    echo "✅ Valid model artifact found for HPO best job: $best_hpo_job"
else
    echo "⚠️  HPO model artifact not found. Falling back to base training job..." | tee -a "$train_log"
    base_job=$(grep '📦 Training Job:' "$log_dir"/train-*.log | grep -v "$best_hpo_job" | tail -1 | awk '{print $NF}' || true)
    if [[ -z "$base_job" ]]; then
        echo "❌ No fallback base training job found in logs. Exiting." | tee -a "$train_log"
        exit 1
    fi
    echo "📌 Updating .env → BEST_TRAINING_JOB_NAME=$base_job" | tee -a "$train_log"
    sed -i.bak "/^BEST_TRAINING_JOB_NAME=/d" ../.env
    echo "BEST_TRAINING_JOB_NAME=$base_job" >> ../.env
    export BEST_TRAINING_JOB_NAME=$base_job
    best_hpo_job=$base_job
fi

# Update MODEL_ARTIFACT in .env
new_artifact="s3://$s3_bucket/output/$best_hpo_job/output/model.tar.gz"
sed -i.bak "/^MODEL_ARTIFACT=/d" ../.env
echo "MODEL_ARTIFACT=$new_artifact" >> ../.env

# Step 6: Evaluate classification metrics
echo "📊 Step 6: Evaluating Classification Metrics" | tee -a "$train_log"
python metrics/01_evaluate_metrics.py 2>&1 | tee -a "$train_log"

# Step 7: Register model and deploy endpoint
echo "📦 Step 7: Registering model and deploying endpoint" | tee -a "$train_log"
cd ../04_model_registry
python 01_register_model.py 2>&1 | tee -a "$train_log" || {
    echo "❌ Model registration failed. Ensure MODEL_PACKAGE_GROUP exists." | tee -a "$train_log"
    exit 1
}
python 02_approve_model.py 2>&1 | tee -a "$train_log"
python 03_deploy_from_registry.py 2>&1 | tee -a "$train_log"
cd ../03_model_training

# Step 8: Batch inference
echo "🔮 Step 8: Running Batch Inference" | tee -a "$train_log"
python inference/run_batch_inference.py 2>&1 | tee -a "$train_log"

# Step 9: Generate Confusion Matrix
echo "📉 Step 9: Generating Confusion Matrix" | tee -a "$train_log"
python metrics/02_confusion_matrix.py 2>&1 | tee -a "$train_log"

# Step 10: Generate ROC Curve
echo "📈 Step 10: Generating ROC Curve" | tee -a "$train_log"
python metrics/03_roc_curve.py 2>&1 | tee -a "$train_log"

# Step 11: SHAP Explainability
echo "🧠 Step 11: Generating SHAP Explainability Visuals" | tee -a "$train_log"
python metrics/04_shap_explainer.py 2>&1 | tee -a "$train_log"

echo "✅ Model training pipeline completed." | tee -a "$train_log"
