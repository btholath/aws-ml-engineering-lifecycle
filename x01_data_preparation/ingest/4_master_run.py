# Script: 4_master_run.py
# Purpose: Orchestrate full setup and instructions

import subprocess

print("🚀 Running Step 1: Create AWS Resources")
subprocess.run(["python3", "1_create_resources.py"])

print("🚀 Running Step 2: Upload Dataset")
subprocess.run(["python3", "2_upload_dataset.py"])

print("🧠 Step 3: Setup Data Wrangler - follow instructions")
subprocess.run(["python3", "3_setup_data_wrangler_flow.py"])
