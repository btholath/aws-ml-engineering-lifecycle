import boto3
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
sagemaker = boto3.client("sagemaker", region_name="us-east-1")

job_name = "real-loan-predictor-xgb-1751671461"
def monitor_job():
    while True:
        response = sagemaker.describe_training_job(TrainingJobName=job_name)
        status = response["TrainingJobStatus"]
        logging.info(f"Status: {status}")
        if status in ["Completed", "Failed", "Stopped"]:
            logging.info(f"Final Status: {status}")
            break
        time.sleep(30)

if __name__ == "__main__":
    monitor_job()
