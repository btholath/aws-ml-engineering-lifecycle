#!/bin/bash

# Define base directory
PROJECT_ROOT="aws-ml-engineering-lifecycle"
mkdir -p $PROJECT_ROOT
cd $PROJECT_ROOT || exit 1

# Utility functions
create_file() {
  mkdir -p "$(dirname "$1")"
  touch "$1"
}

create_module() {
  mkdir -p "$1"
  touch "$1/__init__.py"
}

echo "🚀 Generating ML Engineering Project Structure with Python module support..."

# --- 00_infrastructure ---
create_file 00_infrastructure/01_create_s3_bucket.sh
create_file 00_infrastructure/02_create_sagemaker_domain.sh
create_file 00_infrastructure/03_create_iam_roles.sh
create_file 00_infrastructure/04_cleanup_resources.sh
create_file 00_infrastructure/05_check_resource_status.sh

# --- 01_data ---
mkdir -p 01_data/raw 01_data/processed 01_data/validation
touch 01_data/raw/.gitkeep 01_data/processed/.gitkeep 01_data/validation/.gitkeep

# --- 02_data_preparation ---
create_module 02_data_preparation/transform
create_file 02_data_preparation/transform/01_clean_data.py
create_file 02_data_preparation/transform/02_encode_features.py
create_file 02_data_preparation/transform/03_fix_booleans_and_upload.py
create_file 02_data_preparation/transform/04_validate_dataset.py
create_file 02_data_preparation/transform/05_generate_statistics.py

create_module 02_data_preparation/data_wrangler
create_file 02_data_preparation/data_wrangler/01_generate_flow.py
create_file 02_data_preparation/data_wrangler/02_upload_flow.py
create_file 02_data_preparation/data_wrangler/template.flow

create_module 02_data_preparation/feature_store
create_file 02_data_preparation/feature_store/01_create_feature_group.py
create_file 02_data_preparation/feature_store/02_ingest_features.py

# --- 03_model_training ---
create_module 03_model_training
create_file 03_model_training/01_train_xgboost.py
create_file 03_model_training/02_monitor_training.py

create_module 03_model_training/hpo
create_file 03_model_training/hpo/01_run_hpo_job.py
create_file 03_model_training/hpo/02_visualize_hpo_results.py

create_module 03_model_training/metrics
create_file 03_model_training/metrics/01_evaluate_metrics.py
create_file 03_model_training/metrics/02_confusion_matrix.py
create_file 03_model_training/metrics/03_roc_curve.py
#create_file 03_model_training/metrics/04_shap_explainer.py

# --- 04_model_registry ---
create_module 04_model_registry
create_file 04_model_registry/01_register_model.py
create_file 04_model_registry/02_approve_model.py
create_file 04_model_registry/03_deploy_from_registry.py

# --- 05_model_inference ---
create_module 05_model_inference/real_time
create_file 05_model_inference/real_time/01_deploy_endpoint.py
create_file 05_model_inference/real_time/02_invoke_endpoint.py
create_file 05_model_inference/real_time/03_config_autoscaling.py
create_file 05_model_inference/real_time/04_teardown_endpoint.py

create_module 05_model_inference/batch
create_file 05_model_inference/batch/01_batch_transform.py
create_file 05_model_inference/batch/02_fetch_results.py

create_module 05_model_inference/model_packaging
create_file 05_model_inference/model_packaging/01_create_model_artifact.py
create_file 05_model_inference/model_packaging/02_prepare_container_image.py

# --- 06_monitoring ---
create_module 06_monitoring/model_monitor
create_file 06_monitoring/model_monitor/01_setup_baseline.py
create_file 06_monitoring/model_monitor/02_configure_monitor.py
create_file 06_monitoring/model_monitor/03_log_drift_metrics.py

create_module 06_monitoring/cloudwatch
create_file 06_monitoring/cloudwatch/01_setup_alarms.sh
create_file 06_monitoring/cloudwatch/02_stream_logs.py

mkdir -p 06_monitoring/reports
touch 06_monitoring/reports/model_drift_report.ipynb
touch 06_monitoring/reports/alerting_dashboard.json

# --- 07_security_compliance ---
create_module 07_security_compliance/iam
create_file 07_security_compliance/iam/01_training_role_policy.json
create_file 07_security_compliance/iam/02_inference_role_policy.json
create_file 07_security_compliance/iam/03_attach_policies.sh

create_module 07_security_compliance/encryption
create_file 07_security_compliance/encryption/01_create_kms_key.sh

create_module 07_security_compliance/audit_logging
create_file 07_security_compliance/audit_logging/01_enable_cloudtrail.sh

create_module 07_security_compliance/pii_redaction
create_file 07_security_compliance/pii_redaction/01_scrub_sensitive_fields.py

create_module 07_security_compliance/guardrails
create_file 07_security_compliance/guardrails/01_validate_data_bias.py

# --- 08_cicd_pipeline ---
create_module 08_cicd_pipeline/github_actions
create_file 08_cicd_pipeline/github_actions/01_train_deploy.yml

create_module 08_cicd_pipeline/sagemaker_pipeline
create_file 08_cicd_pipeline/sagemaker_pipeline/01_define_pipeline.py
create_file 08_cicd_pipeline/sagemaker_pipeline/02_compile_pipeline.py

create_module 08_cicd_pipeline/eventbridge
create_file 08_cicd_pipeline/eventbridge/01_trigger_pipeline_on_event.py

create_module 08_cicd_pipeline/step_functions
create_file 08_cicd_pipeline/step_functions/01_ml_workflow_definition.json
create_file 08_cicd_pipeline/step_functions/02_deploy_workflow.py

# --- 09_tests ---
create_module 09_tests
create_file 09_tests/01_test_data_preparation.py
create_file 09_tests/02_test_model_training.py
create_file 09_tests/03_test_pipeline_definition.py
create_file 09_tests/04_test_inference.py

# --- 10_docs ---
create_module 10_docs/architecture
create_file 10_docs/architecture/01_pipeline_diagram.drawio
create_file 10_docs/architecture/02_mlops_architecture.png

create_module 10_docs/usage_guides
create_file 10_docs/usage_guides/01_run_pipeline.md
create_file 10_docs/usage_guides/02_model_registry_guide.md
create_file 10_docs/usage_guides/03_monitoring_setup.md

create_module 10_docs/notebooks
create_file 10_docs/notebooks/01_eda_visualizations.ipynb

create_module 10_docs/aws_certification_notes
create_file 10_docs/aws_certification_notes/01_ml_associate_guide.md
create_file 10_docs/aws_certification_notes/02_cli_reference.md

# Root-level README
touch README.md

echo "✅ Project structure with __init__.py created successfully."
