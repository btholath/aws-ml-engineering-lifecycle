import os
import boto3
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load existing env vars
load_dotenv(override=True)

# Read tuning job name
tuning_job_name = os.getenv("HPO_TUNING_JOB_NAME")
if not tuning_job_name:
    raise ValueError("❌ HPO_TUNING_JOB_NAME is not set in the environment or .env file.")

# Initialize SageMaker client
sm = boto3.client("sagemaker")

# List training jobs for the HPO tuning job
response = sm.list_training_jobs_for_hyper_parameter_tuning_job(
    HyperParameterTuningJobName=tuning_job_name,
    MaxResults=10,
    SortBy='FinalObjectiveMetricValue',
    SortOrder='Ascending'
)

# Extract results
# Parse training job results
training_jobs = response["TrainingJobSummaries"]

# Convert to pandas DataFrame for easier visualization
records = []
for job in training_jobs:
    records.append({
        "TrainingJobName": job["TrainingJobName"],
        "ObjectiveValue": job.get("FinalHyperParameterTuningJobObjectiveMetric", {}).get("Value", None),
        "Status": job["TrainingJobStatus"]
    })

df = pd.DataFrame(records)
print(df)

# Visualize results (if objective value exists)
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

# Select best (lowest objective value) completed job
best_job = df[df["Status"] == "Completed"].nsmallest(1, "ObjectiveValue")

if best_job.empty:
    raise RuntimeError("❌ No successful training jobs found in HPO results.")

best_job_name = best_job.iloc[0]["TrainingJobName"]
print(f"\n✅ Best training job: {best_job_name}")

# Update .env utility
def update_env_variable(key: str, value: str, env_file=".env"):
    lines = []
    found = False
    if os.path.exists(env_file):
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

# Update and reload .env
update_env_variable("BEST_TRAINING_JOB_NAME", best_job_name)
load_dotenv(override=True)

# Confirm
print(f"📌 Updated .env → BEST_TRAINING_JOB_NAME={best_job_name}")