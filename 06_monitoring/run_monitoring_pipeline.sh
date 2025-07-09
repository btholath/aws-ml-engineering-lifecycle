#!/bin/bash

set -e

echo "🧪 Step 1: Setting up CloudWatch Alarms..."
bash ./cloudwatch/01_setup_alarms.sh

echo "📡 Step 2: Streaming latest CloudWatch logs..."
python3 ./cloudwatch/02_stream_logs.py || echo "⚠️ Could not stream logs (may require endpoint activity)."

echo "🧠 Step 3: Setting up Model Baseline..."
python3 ./model_monitor/01_setup_baseline.py

echo "📅 Step 4: Configuring Model Monitor..."
python3 ./model_monitor/02_configure_monitor.py

echo "📊 Step 5: Logging Drift Metrics..."
python3 ./model_monitor/03_log_drift_metrics.py

echo "✅ Monitoring pipeline completed successfully."
