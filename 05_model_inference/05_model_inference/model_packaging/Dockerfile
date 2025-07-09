
FROM python:3.9-slim
COPY xgboost-model /opt/ml/model/xgboost-model
RUN pip install xgboost pandas flask
ENV SAGEMAKER_PROGRAM serve.py
