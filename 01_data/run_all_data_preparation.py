"""
Script: run_all_data_preparation.py
Purpose: Run all data preparation steps sequentially and update project root .env
"""

import subprocess
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# List of scripts to run
scripts = [
    "/workspaces/aws-ml-engineering-lifecycle/01_data/scripts/02_split_validation_data.py",
    "/workspaces/aws-ml-engineering-lifecycle/01_data/scripts/03_transform_data.py",
    "/workspaces/aws-ml-engineering-lifecycle/01_data/scripts/04_upload_cleaned_to_s3.py"
]

# Load and locate project .env
project_root = Path(__file__).resolve().parent
while project_root != project_root.parent:
    if (project_root / ".env").exists():
        break
    project_root = project_root.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

# Run each script and stop on failure
for script in scripts:
    logging.info(f"🚀 Running: {script}")
    result = subprocess.run(["python", script], capture_output=True, text=True)
    if result.returncode == 0:
        logging.info(f"✅ Success: {script}")
    else:
        logging.error(f"❌ Failed: {script}")
        logging.error(result.stderr)
        break
else:
    # All scripts ran successfully – update .env
    def update_env_variable(key: str, value: str, env_file: Path):
        lines = []
        found = False
        if env_file.exists():
            with open(env_file, "r") as f:
                lines = f.readlines()

        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}\n"
                found = True
                break
        if not found:
            lines.append(f"{key}={value}\n")

        with open(env_file, "w") as f:
            f.writelines(lines)

    update_env_variable("LAST_RUN_DATA_SCRIPTS", ",".join(scripts), dotenv_path)
    logging.info(f"📌 Updated .env → LAST_RUN_DATA_SCRIPTS={','.join(scripts)}")
