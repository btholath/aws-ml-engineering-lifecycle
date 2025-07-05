import os
import boto3
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load .env file
load_dotenv()

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
