import os
import boto3
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from pathlib import Path

# ----------------------------
# Load .env from project root
# ----------------------------
project_root = Path(__file__).resolve().parent.parent.parent  # go up to root
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# ----------------------------
# Read tuning job name
# ----------------------------
tuning_job_name = os.getenv("HPO_TUNING_JOB_NAME")
if not tuning_job_name:
    raise ValueError("❌ HPO_TUNING_JOB_NAME is not set in the .env file.")

# ----------------------------
# Initialize SageMaker client
# ----------------------------
sm = boto3.client("sagemaker")

# ----------------------------
# List training jobs for HPO job
# ----------------------------
response = sm.list_training_jobs_for_hyper_parameter_tuning_job(
    HyperParameterTuningJobName=tuning_job_name,
    MaxResults=10,
    SortBy='FinalObjectiveMetricValue',
    SortOrder='Ascending'
)

# ----------------------------
# Convert to DataFrame
# ----------------------------
training_jobs = response["TrainingJobSummaries"]
records = [
    {
        "TrainingJobName": job["TrainingJobName"],
        "ObjectiveValue": job.get("FinalHyperParameterTuningJobObjectiveMetric", {}).get("Value", None),
        "Status": job["TrainingJobStatus"]
    }
    for job in training_jobs
]

df = pd.DataFrame(records)
print(df)

# ----------------------------
# Plot HPO results
# ----------------------------
if not df["ObjectiveValue"].isnull().all():
    plt.figure(figsize=(10, 6))
    plt.barh(df["TrainingJobName"], df["ObjectiveValue"], color="skyblue")
    plt.xlabel("Objective Metric (logloss)")
    plt.ylabel("Training Job")
    plt.title(f"Top HPO Results for: {tuning_job_name}")
    plt.tight_layout()
    plt.show()
else:
    print("⚠️ No completed training jobs with objective values found.")

# ----------------------------
# Get best job
# ----------------------------
best_job = df[df["Status"] == "Completed"].nsmallest(1, "ObjectiveValue")
if best_job.empty:
    raise RuntimeError("❌ No successful training jobs found in HPO results.")

best_job_name = best_job.iloc[0]["TrainingJobName"]
print(f"\n✅ Best training job: {best_job_name}")

# ----------------------------
# Update .env file at project root
# ----------------------------
def update_env_variable(key: str, value: str, env_file=env_path):
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

update_env_variable("BEST_TRAINING_JOB_NAME", best_job_name)

# ----------------------------
# Reload to confirm
# ----------------------------
load_dotenv(dotenv_path=env_path, override=True)
print(f"📌 Updated .env → BEST_TRAINING_JOB_NAME={best_job_name}")
