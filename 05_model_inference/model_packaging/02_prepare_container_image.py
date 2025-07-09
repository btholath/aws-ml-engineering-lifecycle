import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dockerfile = """
FROM python:3.9-slim
COPY xgboost-model /opt/ml/model/xgboost-model
RUN pip install xgboost pandas flask
ENV SAGEMAKER_PROGRAM serve.py
"""

path = "05_model_inference/model_packaging/Dockerfile"
with open(path, "w") as f:
    f.write(dockerfile)

logger.info(f"✅ Dockerfile created at: {path}")