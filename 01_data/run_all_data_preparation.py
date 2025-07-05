"""
Script: run_all_data_preparation.py
Purpose: Run all data preparation steps sequentially
"""

import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

scripts = [
    "01_data/scripts/02_split_validation_data.py",
    "01_data/scripts/03_transform_data.py",
    "01_data/scripts/04_upload_cleaned_to_s3.py"
]

for script in scripts:
    logging.info(f"🚀 Running: {script}")
    result = subprocess.run(["python", script], capture_output=True, text=True)
    if result.returncode == 0:
        logging.info(f"✅ Success: {script}")
    else:
        logging.error(f"❌ Failed: {script}")
        logging.error(result.stderr)
        break