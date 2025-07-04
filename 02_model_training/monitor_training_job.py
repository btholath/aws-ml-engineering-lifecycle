import boto3
import time

job_name = "real-loan-predictor-xgb-1751669671"
client = boto3.client("sagemaker", region_name="us-east-1")

while True:
    response = client.describe_training_job(TrainingJobName=job_name)
    status = response["TrainingJobStatus"]
    print(f"⏱️ Status: {status}")
    if status in ["Completed", "Failed", "Stopped"]:
        print(f"✅ Final status: {status}")
        break
    time.sleep(20)
