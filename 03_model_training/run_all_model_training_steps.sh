#!/bin/bash
set -e
set -o pipefail

echo "🚀 Starting model training pipeline..."

# Step 1: Train XGBoost
echo "🧠 Step 1: Training XGBoost Model"
python 01_train_xgboost.py

# Step 2: Monitor training
echo "🔍 Step 2: Monitoring Training Job"
python 02_monitor_training.py

# Step 3: Run HPO
echo "📈 Step 3: Running Hyperparameter Optimization (HPO)"
python hpo/01_run_hpo_job.py

# Step 4: Visualize HPO Results and update .env with best job
echo "🖼️ Step 4: Visualizing HPO Results"
python hpo/02_visualize_hpo_results.py

# Step 5: Evaluate classification metrics using best model
echo "📊 Step 5: Evaluating Classification Metrics"
python metrics/01_evaluate_metrics.py

# Step 6: Batch inference using deployed endpoint
echo "🔮 Step 6: Running Batch Inference"
python inference/run_batch_inference.py

# Step 7: Generate Confusion Matrix
echo "📉 Step 7: Generating Confusion Matrix"
python metrics/02_confusion_matrix.py

# Step 8: Generate ROC Curve
echo "📈 Step 8: Generating ROC Curve"
python metrics/03_roc_curve.py

# Step 9: SHAP Explainability
echo "🧠 Step 9: Generating SHAP Explainability Visuals"
python metrics/04_shap_explainer.py

echo "✅ Model training pipeline completed."
