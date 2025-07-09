import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import boto3

# Load env
project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=project_root / ".env", override=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

region = os.getenv("AWS_REGION", "us-east-1")
endpoint_name = os.getenv("XGB_INFERENCE_ENDPOINT")
role = os.getenv("SAGEMAKER_ROLE_ARN")

sm = boto3.client("sagemaker", region_name=region)

logger.info("⚙️ Configuring Model Monitor...")
monitor_name = "xgb-monitor"
monitor_input = {
    "MonitoringScheduleName": monitor_name,
    "MonitoringScheduleConfig": {
        "ScheduleConfig": {"ScheduleExpression": "cron(0 * ? * * *)"},  # Hourly
        "MonitoringJobDefinition": {
            "BaselineConfig": {
                "ConstraintsResource": {"S3Uri": f"s3://{os.getenv('S3_BUCKET')}/monitoring/baseline/constraints.json"}
            },
            "MonitoringInputs": [{
                "EndpointInput": {
                    "EndpointName": endpoint_name,
                    "LocalPath": "/opt/ml/processing/input"
                }
            }],
            "MonitoringOutputConfig": {
                "MonitoringOutputs": [{
                    "S3Output": {
                        "S3Uri": f"s3://{os.getenv('S3_BUCKET')}/monitoring/output",
                        "LocalPath": "/opt/ml/processing/output"
                    }
                }]
            },
            "MonitoringResources": {
                "ClusterConfig": {
                    "InstanceCount": 1,
                    "InstanceType": "ml.m5.large",
                    "VolumeSizeInGB": 20
                }
            },
            "RoleArn": role,
            "StoppingCondition": {"MaxRuntimeInSeconds": 1800}
        }
    }
}

response = sm.create_monitoring_schedule(**monitor_input)
logger.info(f"✅ Monitoring schedule created: {monitor_name}")