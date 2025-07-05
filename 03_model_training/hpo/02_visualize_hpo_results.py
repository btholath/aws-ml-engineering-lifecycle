"""
Visualize HPO results using SageMaker SDK and matplotlib.
"""
import boto3, pandas as pd, matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()
sm = boto3.client("sagemaker", region_name=os.getenv("AWS_REGION"))
tuning_job_name = os.getenv("HPO_JOB_NAME")

response = sm.list_training_jobs_for_hyper_parameter_tuning_job(
    HyperParameterTuningJobName=tuning_job_name
)
results = []
for job in response["TrainingJobSummaries"]:
    results.append({
        "JobName": job["TrainingJobName"],
        "AUC": job["FinalHyperParameterTuningJobObjectiveMetric"]["Value"]
    })

df = pd.DataFrame(results).sort_values("AUC", ascending=False)
df.plot(kind="bar", x="JobName", y="AUC", title="HPO Results: AUC Scores")
plt.tight_layout()
plt.savefig("hpo_results.png")
