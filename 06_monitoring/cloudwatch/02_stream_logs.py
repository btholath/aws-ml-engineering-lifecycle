import os
import logging
import boto3
from dotenv import load_dotenv
from pathlib import Path

# Load env variables
project_root = Path(__file__).resolve().parent.parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

log_group = os.getenv("CLOUDWATCH_LOG_GROUP", "/aws/sagemaker/Endpoints/sagemaker-xgb-endpoint")

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logs = boto3.client("logs", region_name=os.getenv("AWS_REGION", "us-east-1"))

streams = logs.describe_log_streams(logGroupName=log_group, orderBy="LastEventTime", descending=True)["logStreams"]
if not streams:
    logger.warning(f"No log streams found in log group: {log_group}")
    exit(1)

stream_name = streams[0]["logStreamName"]
logger.info(f"🔍 Streaming from: {stream_name}")

events = logs.get_log_events(logGroupName=log_group, logStreamName=stream_name, startFromHead=True)
for event in events["events"]:
    print(event["message"])