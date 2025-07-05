#!/bin/bash
set -e

echo "🚀 Starting model training pipeline..."

echo "🧠 Step 1: Training XGBoost Model"
python3 01_train_xgboost.py

# Extract job name
job_name=$(cat latest_training_job.txt)

echo "🔍 Step 2: Monitoring Training Job"
python3 02_monitor_training.py

echo "📈 Step 3: Running Hyperparameter Optimization (HPO)"
python hpo/01_run_hpo_job.py

echo "🖼️ Step 4: Visualizing HPO Results"
python hpo/02_visualize_hpo_results.py

echo "📊 Step 5: Evaluating Classification Metrics"
python metrics/01_evaluate_metrics.py

echo "📉 Step 6: Generating Confusion Matrix"
python metrics/02_confusion_matrix.py

echo "📈 Step 7: Plotting ROC Curve"
python metrics/03_roc_curve.py

echo "🧠 Step 8: Running SHAP Explainer"
python metrics/04_shap_explainer.py

echo "✅ All training steps completed successfully."
