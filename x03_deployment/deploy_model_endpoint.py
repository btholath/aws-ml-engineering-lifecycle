import boto3
import time
import logging

sagemaker = boto3.client("sagemaker", region_name="us-east-1")
model_name = f"xgb-loan-model-{int(time.time())}"
endpoint_config_name = f"{model_name}-config"
endpoint_name = f"{model_name}-endpoint"

model_data = "s3://btholath-sagemaker-datawrangler-demo/None/real-loan-predictor-xgb-1751671461/output/model.tar.gz"
role_arn = "arn:aws:iam::637423309379:role/service-role/AmazonSageMaker-ExecutionRole-20250704T144877"

container = {
    "Image": "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.7-1",
    "ModelDataUrl": model_data
}

# Create model
sagemaker.create_model(ModelName=model_name, PrimaryContainer=container, ExecutionRoleArn=role_arn)

# Create endpoint config
sagemaker.create_endpoint_config(
    EndpointConfigName=endpoint_config_name,
    ProductionVariants=[{
        "InstanceType": "ml.m5.large",
        "InitialInstanceCount": 1,
        "ModelName": model_name,
        "VariantName": "AllTraffic"
    }]
)

# Deploy endpoint
sagemaker.create_endpoint(EndpointName=endpoint_name, EndpointConfigName=endpoint_config_name)
print(f"✅ Deployment started. Endpoint name: {endpoint_name}")
